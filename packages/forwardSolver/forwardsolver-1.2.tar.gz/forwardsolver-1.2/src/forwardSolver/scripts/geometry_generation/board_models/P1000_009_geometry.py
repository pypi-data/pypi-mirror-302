import numpy as np

from forwardSolver.scripts.geometry_generation.geometry_generation import (
    GeometricModel2D,
)
from forwardSolver.scripts.geometry_generation.geometry_interface import (
    add_circular_arc,
    add_line,
    add_loop,
    add_point,
)
from forwardSolver.scripts.geometry_generation.geometry_utils import (
    cartesian_to_polar2D,
    compute_chord_length,
    compute_cord_angle,
    polar2D_to_cartesian,
)
from forwardSolver.scripts.params.forward_solver_params import ForwardSolverParams
from forwardSolver.scripts.utils.logging import get_logger

logger = get_logger(__name__)


class GeometryP10002D(GeometricModel2D):
    """GeometricModel subclass with P1000-009 specific methods. Initialise with ForwardSolverParams.
    By default ForwardSolverParams.factory("P1000-009") will be assumed"""

    def __init__(self, params: ForwardSolverParams = None):
        super(GeometryP10002D, self).__init__()
        if params:
            self.params = params
        else:
            self.params = ForwardSolverParams.factory("P1000-009")

    def add_P1000_009_board(self):
        """
        Function to draw P1000-009 board.

        """
        # compute derived parameters

        N_electrodes = self.params.geometry.number_electrodes
        electrode_width = self.params.geometry.electrode_width  # mm
        electrode_gap = (
            self.params.geometry.electrode_separation - electrode_width
        )  # mm

        radius_inner_frame = (
            self.params.geometry.curvature_radius + self.params.geometry.board_height
        )  # mm
        radius_frame_dimples = self.params.geometry.curvature_radius  # mm

        # compute width of board based on electrodes
        electrode_span_width = (
            (N_electrodes - 1) * electrode_gap
            + N_electrodes * electrode_width
            + self.params.geometry.board_left_extra_width
            + self.params.geometry.board_right_extra_width
        )

        # compute chord length and angle
        chord_length = compute_chord_length(
            self.params.geometry.curvature_radius, electrode_span_width
        )
        self.params.geometry.chord_length = chord_length

        chord_angle = compute_cord_angle(
            self.params.geometry.curvature_radius, chord_length
        )
        self.params.geometry.chord_angle = chord_angle

        # Calculate curvature centre above origin
        curvature_centre = (
            0,
            self.params.geometry.curvature_radius
            - 0.5 * chord_length * np.tan(chord_angle / 4.0),
        )  # (mm, mm)

        # Create PCB substrate region
        electrode_board_centres = self._compute_electrode_centres_009_board(
            N_electrodes,
            electrode_gap,
            electrode_width,
            0.5 * (radius_frame_dimples + radius_inner_frame),
            chord_length,
        )

        bottom_left_left_coord = (
            -self.params.geometry.board_left_width - 0.5 * chord_length,
            -self.params.geometry.frame_height,
            0,
        )
        top_left_left_coord = (
            -self.params.geometry.board_left_width - 0.5 * chord_length,
            0,
            0,
        )
        top_left_middle_coord = (-0.5 * chord_length, 0, 0)
        top_right_middle_coord = (0.5 * chord_length, 0, 0)
        top_right_right_coord = (
            0.5 * chord_length + self.params.geometry.board_right_width,
            0,
            0,
        )
        bottom_right_right_coord = (
            0.5 * chord_length + self.params.geometry.board_right_width,
            -self.params.geometry.frame_height,
            0,
        )

        x_coord_circular = 0.5 * chord_length + np.sqrt(
            self.params.geometry.frame_height * self.params.geometry.frame_height / 2
        )

        bottom_right_middle = (
            x_coord_circular,
            -self.params.geometry.frame_height,
            0,
        )
        bottom_left_middle = (
            -x_coord_circular,
            -self.params.geometry.frame_height,
            0,
        )

        p1 = cartesian_to_polar2D(
            np.array(bottom_left_middle)[:2], np.array(curvature_centre)
        )
        p2 = cartesian_to_polar2D(
            np.array(bottom_right_middle)[:2], np.array(curvature_centre)
        )
        arc_length = p1[0] * (p2[1] - p1[1])

        ground_plate_radius = np.sqrt(
            (bottom_right_middle[0] - curvature_centre[0]) ** 2
            + (bottom_right_middle[1] - curvature_centre[1]) ** 2
        )

        # Add the board under the electrodes
        for point in electrode_board_centres:
            cart_point = polar2D_to_cartesian(point, origin=curvature_centre)
            self.add_inner_shape(
                shape="rectangle",
                centre=(cart_point[0], cart_point[1], 0),
                width=self.params.geometry.electrode_width + 2,
                height=self.params.geometry.board_height,
                theta=np.pi / 2 + point[1],
                permittivity=self.params.geometry.permittivity_board,
                description="fixedRegions",
            )

        # Add soldercoat on top of electrodes
        for radius, theta in electrode_board_centres:
            radius = (
                radius
                - 0.5 * self.params.geometry.board_height
                - self.params.geometry.electrode_height
                - 0.5 * self.params.geometry.soldercoat_height
            )
            cart_point = polar2D_to_cartesian((radius, theta), origin=curvature_centre)

            self.add_inner_shape(
                shape="rectangle",
                centre=(cart_point[0], cart_point[1], 0),
                width=self.params.geometry.electrode_width,
                height=self.params.geometry.soldercoat_height,
                theta=np.pi / 2 + theta,
                permittivity=self.params.geometry.permittivity_soldercoat,
                description="fixedRegions",
            )

        # Add board on top left
        self.add_inner_shape(
            shape="rectangle",
            centre=(
                -0.5 * chord_length - 0.5 * self.params.geometry.board_left_width,
                0.5 * self.params.geometry.board_height,
                0,
            ),
            width=self.params.geometry.board_left_width,
            height=self.params.geometry.board_height,
            permittivity=self.params.geometry.permittivity_board,
            description="fixedRegions",
        )

        # Add board on top right
        self.add_inner_shape(
            shape="rectangle",
            centre=(
                0.5 * chord_length + 0.5 * self.params.geometry.board_right_width,
                0.5 * self.params.geometry.board_height,
                0,
            ),
            width=self.params.geometry.board_right_width,
            height=self.params.geometry.board_height,
            permittivity=self.params.geometry.permittivity_board,
            description="fixedRegions",
        )

        # Build frame for the board to sit in

        bottom_left_left = add_point(*bottom_left_left_coord)
        top_left_left = add_point(*top_left_left_coord)
        top_left_middle = add_point(*top_left_middle_coord)
        top_right_middle = add_point(*top_right_middle_coord)
        top_right_right = add_point(*top_right_right_coord)
        bottom_right_right = add_point(*bottom_right_right_coord)

        bottom_left_middle = add_point(*bottom_left_middle)
        bottom_right_middle = add_point(*bottom_right_middle)

        frame_border = []

        left_edge = add_line(bottom_left_left, top_left_left)
        top_edge_left = add_line(top_left_left, top_left_middle)

        for edge in [left_edge, top_edge_left]:
            frame_border.append(edge)

        old_top_left_point = add_point(*top_left_middle_coord)

        for point in electrode_board_centres:
            cart_point = polar2D_to_cartesian(point, origin=curvature_centre)
            (
                bottom_left,
                bottom_right,
                top_right,
                top_left,
            ) = self._add_rectangle_points(
                centre=(cart_point[0], cart_point[1], 0),
                width=self.params.geometry.electrode_width + 2,
                height=self.params.geometry.board_height,
                theta=np.pi / 2 + point[1],
            )

            gap_edge = add_line(old_top_left_point, top_left)
            left_edge = add_line(top_left, bottom_left)
            bottom_edge = add_line(bottom_left, bottom_right)
            right_edge = add_line(bottom_right, top_right)

            for edge in [gap_edge, left_edge, bottom_edge, right_edge]:
                frame_border.append(edge)

            old_top_left_point = top_right

        temp_edge = add_line(old_top_left_point, top_right_middle)

        top_edge_right = add_line(top_right_middle, top_right_right)
        right_edge = add_line(top_right_right, bottom_right_right)
        bottom_edge_right = add_line(bottom_right_right, bottom_right_middle)

        centre_point = add_point(*curvature_centre)

        bottom_arc = add_circular_arc(
            bottom_right_middle, centre_point, bottom_left_middle
        )

        bottom_edge_left = add_line(bottom_left_middle, bottom_left_left)

        for edge in [
            temp_edge,
            top_edge_right,
            right_edge,
            bottom_edge_right,
            bottom_arc,
            bottom_edge_left,
        ]:
            frame_border.append(edge)

        outline_loop = add_loop(frame_border)

        # Now create board shape
        self.add_inner_shape(
            shape="from_outline",
            permittivity=self.params.geometry.permittivity_frame,
            object_tag=outline_loop,
            description="fixedRegions",
        )

        # Add electrodes on top of board
        for radius, theta in electrode_board_centres:
            radius = (
                radius
                - 0.5 * self.params.geometry.board_height
                - 0.5 * self.params.geometry.electrode_height
            )
            cart_point = polar2D_to_cartesian((radius, theta), origin=curvature_centre)

            # Add electrodes
            self.add_boundary(
                shape="rectangle",
                centre=(cart_point[0], cart_point[1], 0),
                width=self.params.geometry.electrode_width,
                height=self.params.geometry.electrode_height,
                theta=np.pi / 2 + theta,
                description="electrodes",
            )

        # Add ground plate below the board
        outline_loop = self.add_curved_rectangle_outline(
            centre=curvature_centre,
            width=arc_length,
            height=self.params.geometry.electrode_height,
            radius_curvature=ground_plate_radius,
            theta_offset=-np.pi / 2,
        )
        self.add_boundary(
            shape="from_outline",
            description="grounds",
            object_tag=outline_loop,
        )

        # Add ground plate on top left of board
        ground_plate_centre = (
            top_left_left_coord[0]
            + self.params.geometry.ground_wing_offset
            + 0.5 * self.params.geometry.left_ground_plate_width,
            0.5 * self.params.geometry.electrode_height
            + self.params.geometry.board_height,
            0,
        )
        self.add_boundary(
            shape="rectangle",
            centre=ground_plate_centre,
            width=self.params.geometry.left_ground_plate_width,
            height=self.params.geometry.electrode_height,
            description="grounds",
        )

    def add_curved_rectangular_pixelation(
        self,
        pixel_permittivity: np.ndarray,
        columns: int = None,
        rows: int = None,
        pixel_region_height: int = None,
    ):
        """Add a matrix of curved pixels representing a material.

        Args:
            pixel_permittivity (np.ndarray): 2d array of permittivities
            columns (int, optional): number of columns.
                Defaults to None (reassigned as self.params.pixels.num_pixel_columns)
            rows (int, optional): number of rows.
                Defaults to None (reassigned as self.params.pixels.num_pixel_rows)
            pixel_region_height (int, optional): pixelated region heigth (mm).
                Defaults to None (reassigned as self.params.geometry.material_height)
        """
        # Set parameters from input or self.params
        pixel_tags = []
        N_pixels_x = columns if columns else self.params.pixels.num_pixel_columns
        N_pixels_y = rows if rows else self.params.pixels.num_pixel_rows

        pixel_region_height = (
            pixel_region_height
            if pixel_region_height
            else self.params.geometry.material_height
        )

        # Calculate curvature centre above origin
        curvature_centre = (
            0,
            self.params.geometry.curvature_radius
            - 0.5
            * self.params.geometry.chord_length
            * np.tan(self.params.geometry.chord_angle / 4.0),
        )  # (mm, mm)

        radius_curvature = (
            self.params.geometry.curvature_radius - self.params.geometry.material_gap
        )

        # Compute length of circular arc above the electrodes
        pixel_region_arc = 2 * np.arcsin(
            (
                0.5 * self.params.geometry.chord_length
                - self.params.geometry.board_left_extra_width
            )
            / (radius_curvature - self.params.geometry.material_gap)
        )

        # Compute the maximum object size enclosable by the sensor
        max_material_height = 0.5 * (
            self.params.geometry.chord_length - 2 * self.params.geometry.material_gap
        )

        # Check material will fit on the sensor
        assert pixel_region_height < max_material_height

        theta_offset = (
            -np.pi / 2
        )  # This is hardcoded for now, will only change if sensor not horizontal

        # Compute pixel widths and height
        pixel_arc_length = pixel_region_arc / N_pixels_x
        pixel_height = pixel_region_height / N_pixels_y

        # Compute the center of the rectangles in polar coordinates
        index_list = [(i, j) for i in range(N_pixels_x) for j in range(N_pixels_y)]
        pixel_centres = [
            (
                radius_curvature - j * pixel_height,
                -pixel_arc_length * (N_pixels_x / 2 - i - 1 / 2),
            )
            for j in range(N_pixels_y)
            for i in range(N_pixels_x)
        ]

        for point, idx in list(zip(pixel_centres, index_list)):
            outline_loop = self.add_curved_rectangle_outline(
                centre=curvature_centre,
                width=point[0] * pixel_arc_length,
                height=pixel_height,
                radius_curvature=point[0],
                theta_offset=point[1] + theta_offset,
            )
            pixel_tags.append(
                self.add_inner_shape(
                    shape="from_outline",
                    permittivity=pixel_permittivity[idx[0], idx[1]],
                    object_tag=outline_loop,
                    description="pixels",
                    sub_info=f"p_{idx[0]}_{idx[1]}",
                )
            )
        return pixel_tags

    def add_curved_rectangle_outline(
        self,
        *,
        centre: tuple = (0, 0),
        width: float = 1,
        height: float = 1,
        radius_curvature: float = 0,
        theta_offset: float = 0,
    ) -> tuple:
        """
        Function for generating a rectanlge, using centre coordinates and width and height
        Note that rectangle lines and loops are created in positive direction

        Args:
            centre (tuple, optional): Centre coordinates. Defaults to (0, 0, 0).
            width (float, optional): Total width. Defaults to 1.
            height (float, optional): Total height. Defaults to 1.
            radius_curvature (float): Curvature of rectangle.

        Returns:
            tuple:
                outline_loop (int): curve loop tag
                edges (list): list of tags of curve loop segments
        """
        if width > 0 and height > 0 and radius_curvature > 0:
            centre_point = add_point(*centre)
            theta = (1 / radius_curvature) * (width) / 2
            left_top_coord = (radius_curvature, -theta + theta_offset)
            right_top_coord = (radius_curvature, +theta + theta_offset)
            left_bottom_coord = (
                radius_curvature - height,
                -theta + theta_offset,
            )
            right_bottom_coord = (
                radius_curvature - height,
                theta + theta_offset,
            )

            point = polar2D_to_cartesian(left_top_coord, origin=centre)
            top_left = add_point(*point)

            point = polar2D_to_cartesian(right_top_coord, origin=centre)
            top_right = add_point(*point)

            point = polar2D_to_cartesian(left_bottom_coord, origin=centre)
            bottom_left = add_point(*point)

            point = polar2D_to_cartesian(right_bottom_coord, origin=centre)
            bottom_right = add_point(*point)

            # Create edges
            left_edge = add_line(bottom_left, top_left)
            top_edge = add_circular_arc(top_left, centre_point, top_right)
            right_edge = add_line(top_right, bottom_right)
            bottom_edge = add_circular_arc(bottom_right, centre_point, bottom_left)

            edges = [left_edge, top_edge, right_edge, bottom_edge]

            outline_loop = add_loop(edges)

            return outline_loop
        else:
            logger.warning(
                "Width, height and radius curvature need to be larger than 0, \
                    theta offset equal or larger than 0"
            )

    @staticmethod
    def _compute_electrode_centres_009_board(
        N_electrodes: int,
        electrode_gap: float,
        electrode_width: float,
        radius_curvature: float,
        chord_length: float,
    ) -> list:
        """Function to compute the polar coordinates of the electrode centres

        Args:
            N_electrodes (int): number of electrodes
            electrode_gap (float): gap between electrodes
            electrode_width (float): electrode width
            radius_curvature (float): radius of curvature of the board
            chord_length (float): chord length of the board arc

        Returns:
            list: list of tuples with centre points of the electrodes
        """

        # compute width of board based on electrode
        electrode_span_width = (
            N_electrodes - 1
        ) * electrode_gap + N_electrodes * electrode_width

        # compute chord length
        chord_length = compute_chord_length(radius_curvature, electrode_span_width)

        assert chord_length <= electrode_span_width

        # compute electrode centre to centre
        electrode_c2c = electrode_width + electrode_gap
        # angle for electrode_c2c arc length
        electrode_c2c_angle = electrode_c2c / radius_curvature

        electrode_centres_angles = [
            -electrode_c2c_angle * (N_electrodes / 2 - i - 1 / 2)
            for i in range(N_electrodes)
        ]

        # Rotate angles by -pi/2
        electrode_centre_points = [
            (radius_curvature, theta - np.pi / 2) for theta in electrode_centres_angles
        ]
        return electrode_centre_points
