import numpy as np

from forwardSolver.scripts.geometry_generation.geometry_generation import (
    GeometricModel,
    GeometricModel2D,
    GeometricModel3D,
)
from forwardSolver.scripts.geometry_generation.geometry_interface import (  # noqa: F403
    add_box,
    add_cylindroid,
    cut_objects,
    extrude_2D_objects,
    intersect_objects,
    translate_objects,
)
from forwardSolver.scripts.params.forward_solver_params import ForwardSolverParams
from forwardSolver.scripts.utils.logging import get_logger

logger = get_logger(__name__)


class GeometryP3000(GeometricModel):
    """GeometricModel subclass with P3000-005 specific methods. Initialise with ForwardSolverParams.
    By default ForwardSolverParams.factory("P3000-005") will be assumed"""

    def __init__(self, params: ForwardSolverParams = None):
        if params:
            self.params = params
        else:
            self.params = ForwardSolverParams.factory("P3000-005")

    def add_P3000_005_board(self, rounded_radius: float = 0) -> tuple:
        """Method adding 2D geometry of the P3000-005 board

        Returns:
            tuple: ([inner_shapes tags], [electrodes tags], ground_plate tag)
        """
        inner_shapes, electrodes = [], []
        inner_shapes.append(
            self.add_inner_shape(
                shape="rectangle",
                centre=(
                    0,
                    -(1 / 6) * self.params.geometry.domain_height
                    + (1 / 2) * self.params.geometry.pcb_substrate_height,
                    0,
                ),
                width=self.params.geometry.pcb_substrate_width,
                height=self.params.geometry.pcb_substrate_height,
                permittivity=self.params.geometry.permittivity_pcb_substrate,
                description="fixedRegions",
            )
        )

        # Create mylar layer
        inner_shapes.append(
            self.add_inner_shape(
                shape="rectangle",
                centre=(
                    0,
                    -(1 / 6) * self.params.geometry.domain_height
                    + self.params.geometry.pcb_substrate_height
                    + self.params.geometry.mylar_gap
                    + (1 / 2) * self.params.geometry.mylar_thickness,
                    0,
                ),
                width=self.params.geometry.pcb_substrate_width,
                height=self.params.geometry.mylar_thickness,
                permittivity=self.params.geometry.permittivity_mylar,
                description="fixedRegions",
            )
        )

        # Create plastic layer
        inner_shapes.append(
            self.add_inner_shape(
                shape="rectangle",
                centre=(
                    0,
                    -(1 / 6) * self.params.geometry.domain_height
                    + self.params.geometry.pcb_substrate_height
                    + self.params.geometry.mylar_gap
                    + self.params.geometry.mylar_thickness
                    + (1 / 2) * self.params.geometry.plastic_thickness,
                    0,
                ),
                width=self.params.geometry.pcb_substrate_width,
                height=self.params.geometry.plastic_thickness,
                permittivity=self.params.geometry.permittivity_plastic,
                description="fixedRegions",
            )
        )

        # Add electrodes
        electrode_board_centres = self._compute_electrode_centres_005_board(
            self.params.geometry.number_electrodes,
            self.params.geometry.electrode_separation,
            -(1 / 6) * self.params.geometry.domain_height
            + self.params.geometry.pcb_substrate_height
            + (1 / 2) * self.params.geometry.electrode_height,
        )

        for i, point in enumerate(electrode_board_centres):
            electrodes.append(
                self.add_boundary(
                    shape="rounded_rectangle",
                    centre=(point[0], point[1], 0),
                    width=self.params.geometry.electrode_width,
                    height=self.params.geometry.electrode_height,
                    description="electrodes",
                    rounded_radius=rounded_radius,
                )
            )

        # Add ground plate
        ground_plate = self.add_boundary(
            shape="rectangle",
            centre=(
                0,
                -(1 / 6) * self.params.geometry.domain_height
                + self.params.geometry.pcb_substrate_height
                + (1 / 2) * self.params.geometry.electrode_height
                - self.params.geometry.ground_plate_depth
                + (1 / 2) * self.params.geometry.ground_plate_thickness,
                0,
            ),
            width=self.params.geometry.pcb_substrate_width,
            height=self.params.geometry.ground_plate_thickness,
            description="grounds",
        )

        return inner_shapes, electrodes, ground_plate

    @staticmethod
    def _compute_electrode_centres_005_board(
        N_electrodes: int,
        electrode_separation: float,
        y_offset: float,
    ) -> tuple:
        """Function to compute the polar coordinates of the electrode centres

        Args:
            N_electrodes (int): number of electrodes
            electrode_separation(float): gap between electrodes centre to centre
            y_offset (float): y coordinate of the electrode centre

        Returns:
            list: list of tuples with centre points of the electrodes
        """
        electrode_center_points = []
        for i in range(N_electrodes):
            electrode_center_x = -(int(N_electrodes / 2) * electrode_separation) + (
                i * electrode_separation
            )
            electrode_center_y = y_offset
            electrode_center_points.append((electrode_center_x, electrode_center_y))
        return electrode_center_points


class GeometryP30002D(GeometryP3000, GeometricModel2D):
    def __init__(self, params: ForwardSolverParams = None):
        GeometryP3000.__init__(self, params=params)
        GeometricModel2D.__init__(self)

    def add_rectangular_pixelation(
        self,
        pixel_permittivity: np.ndarray,
        columns: int = None,
        rows: int = None,
        material_width: float = None,
        material_height: float = None,
        y_offset: float = 0,
    ) -> list:
        """Add a matrix of pixels representing a material.

        Args:
            pixel_permittivity (np.ndarray): matrix of pixel permittivities
            columns (int, optional): number of columns.
                Defaults to None (reassigned as self.params.pixels.num_pixel_columns)
            rows (int, optional): number of rows.
                Defaults to None (reassigned as self.params.pixels.num_pixel_rows)
            material_width (float, optional): pixelated region width (mm).
                Defaults to None (reassigned as self.params.geometry.material_width)
            material_height (float, optional): pixelated region heigth (mm).
                Defaults to None (reassigned as self.params.geometry.material_height)
            y_offset (float, optional): offset between board and pixels. Defaults to 0.

        Returns:
            list: tags of pixel objects
        """
        pixel_tags = []
        N_pixels_x = columns if columns else self.params.pixels.num_pixel_columns
        N_pixels_y = rows if rows else self.params.pixels.num_pixel_rows

        pixel_material_width = (
            material_width if material_width else self.params.geometry.material_width
        )
        pixel_material_height = (
            material_height if material_height else self.params.geometry.material_height
        )

        # Compute pixel widths and height
        pixel_width = pixel_material_width / N_pixels_x
        pixel_height = pixel_material_height / N_pixels_y
        # Compute coordinates of the pixel centres
        centres = [
            (
                -pixel_width * (N_pixels_x / 2 - i - 1 / 2),
                y_offset + (j + 1 / 2) * pixel_height,
            )
            for j in range(N_pixels_y)
            for i in range(N_pixels_x)
        ]
        # Draw the rectangle pixels
        index_list = [(i, j) for i in range(N_pixels_x) for j in range(N_pixels_y)]
        for point, idx in list(zip(centres, index_list)):
            pixel_tags.append(
                self.add_inner_shape(
                    shape="rectangle",
                    centre=(point[0], point[1], 0),
                    width=pixel_width,
                    height=pixel_height,
                    permittivity=pixel_permittivity[idx[0], idx[1]],
                    description="pixels",
                    sub_info=f"p_{idx[0]}_{idx[1]}",
                )
            )
        return pixel_tags


class GeometryP30003D(GeometryP3000, GeometricModel3D):
    """Class for P3000-005 3D generation"""

    def __init__(self, params: ForwardSolverParams = None):
        GeometryP3000.__init__(self, params)
        GeometricModel3D.__init__(self)
        # set_custom_setting(name="Geometry.OCCBoundsUseStl", value=1)

    def add_P3000_005_board(self, rounded_radius: float = 0):
        """Method adding 3D geometry of the P3000-005 board"""

        # check current boundary index and permittivity tag values
        start_permittivity_tag_value = self._permittivity_tag_value
        start_boundary_tag_value = self._boundary_tag_value

        # create a temporary model, enabling extrusion of 2D section of P3000
        model_2D = GeometryP30002D()
        init_permittivity_tag_value = model_2D._permittivity_tag_value
        init_boundary_tag_value = model_2D._boundary_tag_value

        model_2D.add_domain(shape="rectangle", width=500, height=500)
        inner_shapes, electrodes, ground_plate = model_2D.add_P3000_005_board(
            rounded_radius=rounded_radius
        )

        # add cylinder for cutting the extruded base shape
        cylinder = add_cylindroid(
            radius=self.params.geometry.base_radius,
            height=300,
        )

        # extrude and cut base elements and ground plate, reassign tags
        for shape in inner_shapes + [ground_plate]:
            volume = self._intersect_cylinder(cylinder, shape)
            shape.geo_tag = volume

        # cut the ground plate to correct shape
        box = add_box(
            width=2 * self.params.geometry.base_radius,
            height=300,
            # TODO: Verify this measurement
            depth=self.params.geometry.electrode_length,
        )
        intersection = intersect_objects(
            [ground_plate.geo_tag],
            [box],
            remove_object=True,
            remove_tool=True,
            dim=self.dim,
        )
        ground_plate.geo_tag = intersection[0][0][1]

        # extrude and translate electrodes, reassign tags
        for boundary in electrodes:
            extrusions_list = extrude_2D_objects(
                [boundary.geo_tag],
                dz=self.params.geometry.electrode_length,
            )
            extrusion = [(dim, tag) for (dim, tag) in extrusions_list if dim == 3][0][1]
            translate_objects(
                tags=[extrusion], dz=-self.params.geometry.electrode_length / 2
            )
            boundary.geo_tag = extrusion

        # reassign definitions of inner regions, boundaries and class params
        self.inner_regions += inner_shapes
        self.boundaries += electrodes + [ground_plate]
        self._permittivity_tag_value = (
            init_permittivity_tag_value
            - model_2D._permittivity_tag_value
            + start_permittivity_tag_value
        )
        self._boundary_tag_value = (
            init_boundary_tag_value
            - model_2D._boundary_tag_value
            + start_boundary_tag_value
        )

        # add top ground plates
        # etched on top of pcb substrate
        copper_base = add_box(
            centre=(
                0,
                -(1 / 6) * self.params.geometry.domain_height
                + self.params.geometry.pcb_substrate_height
                - (1 / 2) * self.params.geometry.top_ground_layer_thickness,
                0,
            ),
            width=self.params.geometry.pcb_substrate_width,
            depth=self.params.geometry.pcb_substrate_width,
            height=self.params.geometry.top_ground_layer_thickness,
        )

        # intersect copper plate and the cylinder
        copper_round = intersect_objects(
            [copper_base],
            [cylinder],
            remove_object=True,
            remove_tool=False,
            dim=self.dim,
        )[0][0][1]

        # add box in the elcetrode area
        box = add_box(
            width=10 * self.params.geometry.base_radius,
            height=1000,
            # TODO: Verify this measurement
            depth=self.params.geometry.electrode_length * 1.05,
        )

        # remove the electrode area from the copper disk
        copper_elements = cut_objects(
            [copper_round],
            [box],
            remove_object=True,
            remove_tool=True,
            dim=self.dim,
        )

        # add the two segments as boundaries
        for element in copper_elements[0]:
            self.add_boundary(
                shape="from_volume",
                object_tag=element[1],
                description="grounds",
            )

    def _intersect_cylinder(self, cylinder: int, shape: int, dist: float = None) -> int:
        """Extrude a shape and intersect with a cylinder volume

        Args:
            cylinder (int): cylinder volume to cut extrusion with
            shape (int): tag of surface to be extruded
            dist (float, optional): extrusion from centre distance. If not provided,
                base radius is used. Defaults to None.

        Returns:
            int: resulting volume tag
        """
        if not dist:
            dist = self.params.geometry.base_radius
        extrusions_list = extrude_2D_objects(
            [shape.geo_tag],
            dz=dist * 2,
        )
        extrusion = [tag for (dim, tag) in extrusions_list if dim == 3][0]

        translate_objects(tags=[extrusion], dz=-dist)

        intersection = intersect_objects(
            [extrusion],
            [cylinder],
            remove_object=True,
            remove_tool=False,
            dim=self.dim,
        )
        return intersection[0][0][1]

    def add_cuboid_pixelation(
        self,
        pixel_permittivity: np.ndarray,
        columns: int = None,
        rows: int = None,
        layers: int = None,
        material_width: float = None,
        material_height: float = None,
        material_length: float = None,
        y_offset: float = 0,
    ) -> list:
        """Add a matrix of pixels representing a material.

        Args:
            pixel_permittivity (np.ndarray): matrix of pixel permittivities
            columns (int, optional): number of columns.
                Defaults to None (reassigned as self.params.pixels.num_pixel_columns)
            rows (int, optional): number of rows.
                Defaults to None (reassigned as self.params.pixels.num_pixel_rows)
            material_width (float, optional): pixelated region width (mm).
                Defaults to None (reassigned as self.params.geometry.material_width)
            material_height (float, optional): pixelated region heigth (mm).
                Defaults to None (reassigned as self.params.geometry.material_height)
            material_length (float, optional): pixelated region heigth (mm).
                Defaults to None (reassigned as self.params.geometry.material_height)
            y_offset (float, optional): offset between board and pixels. Defaults to 0.

        Returns:
            list: tags of pixel objects
        """
        pixel_objects = []
        N_pixels_x = columns if columns else self.params.pixels.num_pixel_columns
        N_pixels_y = rows if rows else self.params.pixels.num_pixel_rows
        N_pixels_z = layers if layers else self.params.pixels.num_pixel_layers

        pixel_material_width = (
            material_width if material_width else self.params.geometry.material_width
        )
        pixel_material_height = (
            material_height if material_height else self.params.geometry.material_height
        )
        pixel_material_length = (
            material_length if material_length else self.params.geometry.material_length
        )
        # Compute pixel widths and height
        pixel_width = pixel_material_width / N_pixels_x
        pixel_height = pixel_material_height / N_pixels_y
        pixel_length = pixel_material_length / N_pixels_z
        # Compute coordinates of the pixel centres
        centres = [
            (
                -pixel_width * (N_pixels_x / 2 - i - 1 / 2),
                y_offset + (j + 1 / 2) * pixel_height,
                pixel_length * (N_pixels_z / 2 - k - 1 / 2),
            )
            for i in range(N_pixels_x)
            for j in range(N_pixels_y)
            for k in range(N_pixels_z)
        ]

        # Draw the rectangle pixels
        index_list = [
            (i, j, k)
            for i in range(N_pixels_x)
            for j in range(N_pixels_y)
            for k in range(N_pixels_z)
        ]
        for point, idx in list(zip(centres, index_list)):
            pixel_objects.append(
                self.add_inner_shape(
                    shape="box",
                    centre=(point[0], point[1], point[2]),
                    width=pixel_width,
                    height=pixel_height,
                    depth=pixel_length,
                    permittivity=pixel_permittivity[idx[0], idx[1], idx[2]],
                    description="pixels",
                    sub_info=f"p_{idx[0]}_{idx[1]}_{idx[2]}",
                )
            )
        return pixel_objects
