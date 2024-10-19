import itertools
import logging
import pathlib
from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from math import pi
from typing import Type, Union

import numpy as np

from forwardSolver.scripts.geometry_generation.geometry_interface import (
    add_box,
    add_ellipse,
    add_ellipsoid,
    add_line,
    add_loop,
    add_physical_group,
    add_point,
    add_rectangle,
    add_surface,
    add_volume_from_outline,
    cut_objects,
    extrude_2D_objects,
    fuse_objects,
    general_fuse_objects,
    get_bounding_box,
    get_loops,
    initialise_geometry_kernel,
    mesh_fields_set,
    remove_entities,
    rotate_objects,
    run_mesh_generation,
    save_mesh_to_path,
    set_mesh_size_at_objects,
    set_mesh_size_within_box,
    set_meshing_algorithm,
    synchronise,
    translate_objects,
)
from forwardSolver.scripts.utils.constants import RelativePermittivity


class Shape2D(Enum):
    """Enum class representing allowed shapes.
    To be added to as the shapes pallet is expanded."""

    ellipse = auto()
    rectangle = auto()
    rounded_rectangle = auto()
    from_outline = auto()


class Shape3D(Enum):
    ellipsoid = auto()
    box = auto()
    from_outline = auto()
    from_section = auto()
    from_volume = auto()


@dataclass
class ShapeInfo:
    tag: int = None  # physical group tag
    description: str = None
    permittivity: float = None
    geo_tag: int = None
    sub_info: str = None


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
logger.addHandler(ch)


class GeometricModel:
    """Interface for generative geometry and mesh set up - see demo not ebook
    Geometry_generation_basic_functions for example use. Shapes are added in order from background
    to the top layer - intersections are computed in the same order (i.e. the last shape will be added on top
    of the preceeding one).
    Background (domain) must always be added first, followed by internal solids with given permittivity values,
    followed by boundaries. Once all the shapes and boundaries are defined, the intersections between these are
    calculated and resolved, and only then can the mesh be generated"""

    def __init__(self):
        initialise_geometry_kernel()
        # geometry dimension - 2D/ 3D
        self.dim: int = 2
        # background: (permittivity, surface_tag)
        self.domain_attributes: ShapeInfo = None
        # raw_inner_shapes: [surface_tag, ...]
        self.inner_regions: list[ShapeInfo] = []
        # boundaries: [ShapeInfo]
        self.boundaries: list[ShapeInfo] = []
        # permittivity_tags: permittivity_tag: permittivity
        self._permittivity_tags: dict = {}
        # start value for shape tags
        self._permittivity_tag_value: int = 100
        # start value for boundary tags
        self._boundary_tag_value: int = 801
        # boundary tag for domain
        self._domain_boundary_tag: int = 800
        # geometry and mesh generation stages checks
        self._domain_added: bool = False
        self._intersections_run: bool = False
        self._initial_mesh_generated: bool = False
        # mesh size parameters
        self.internal_boundary_mesh_size: float = 0.01
        self.domain_boundary_mesh_size: float = 0.1
        self.internal_region_mesh_size: float = 0.05
        self.max_mesh_size: float = 10
        self.mesh_size_dist_threshold_lower: float = 3
        self.mesh_size_dist_threshold_upper: float = 15
        # segments with mesh size points added
        self._size_points_segments = []
        self._mesh_fields = []
        # paths
        self._parameter_mapping_filepath: pathlib.Path = None

    def add_domain(
        self,
        *,
        shape: str = "ellipse",
        centre: tuple = (0, 0, 0),
        width: float = 1,
        height: float = 1,
        depth: float = 1,
        permittivity: float = RelativePermittivity.AIR,
    ):
        """Add background domain (the extent of the mesh) and set its attributes

        Args:
            shape (str, optional): Geometrical shape of the domain.
                Defaults to "ellipse".
            centre (tuple, optional): Centre coordinates. Defaults to (0, 0, 0).
            width (float, optional): Total width. Defaults to 1.
            height (float, optional): Total height. Defaults to 1.
            permittivity (float, optional): Domain medium permittivity.
                Defaults to RelativePermittivity.AIR.
        """
        if not self._domain_added:
            if self.dim == 2:
                domain_surface = self._create_shape(
                    shape=shape,
                    centre=centre,
                    width=width,
                    height=height,
                )
            else:
                domain_surface = self._create_shape(
                    shape=shape,
                    centre=centre,
                    width=width,
                    height=height,
                    depth=depth,
                )
            self.domain_attributes = ShapeInfo(
                permittivity=permittivity,
                geo_tag=domain_surface,
                description="domain",
            )
            self._domain_added = True
            synchronise()

        else:
            logger.warning("Domain already added")

    def add_inner_shape(
        self,
        *,
        shape: str = "ellipse",
        centre: tuple = (0, 0, 0),
        width: float = 1,
        height: float = 1,
        depth: float = None,
        theta: float = 0,
        permittivity: float = 20,
        object_tag: int = None,
        description: str = "fixedRegion",
        sub_info: str = None,
    ) -> ShapeInfo:
        """Define internal shape to be added to geometry.

        Args:
            shape (str, optional): Geometrical shape. Defaults to "ellipse".
            centre (tuple, optional): Centre coordinates. Defaults to (0, 0, 0).
            width (float, optional): Total width. Defaults to 1.
            height (float, optional): Total height. Defaults to 1.
            theta (float, optional): Angle of rotation (radians). Defaults to 1.
            permittivity (float, optional): Local medium permittivity. Defaults to 20.
            object_tag (int, optional): Tag of:
              - curve loop to use with 'from_outline' shape or
              - surface to use with 'from_section' shape (3D only)
              - volume to use with 'from_volume' shape (3D only)

        Returns:
            int: surface tag
        """
        if self._domain_added and not self._intersections_run:
            geo_tag = self._create_verified_shape(
                shape=shape,
                centre=centre,
                width=width,
                height=height,
                depth=depth,
                theta=theta,
                object_tag=object_tag,
            )
            if geo_tag:
                shape_object = ShapeInfo(
                    permittivity=permittivity,
                    description=description,
                    geo_tag=geo_tag,
                    sub_info=sub_info,
                )
                self.inner_regions.append(shape_object)
                return shape_object
        else:
            logger.warning(
                "Inner shape can only be added once background is created,"
                "and before intersections are processed"
            )

    def add_boundary(
        self,
        *,
        shape: str = "ellipse",
        centre: tuple = (0, 0, 0),
        theta: float = 0,
        width: float = 1,
        height: float = 1,
        depth: float = None,
        description: str = "boundaries",
        object_tag: int = None,
        rounded_radius: float = 0,
    ) -> ShapeInfo:
        """Define internal boundary to be added to geometry.
        Future extension can include optional internal meshing along with permittivity
        setting if required.

        Args:
            shape (str, optional): Geometrical shape. Defaults to "ellipse".
            centre (tuple, optional): Centre coordinates. Defaults to (0, 0, 0).
            width (float, optional): Total width. Defaults to 1.
            height (float, optional): Total height. Defaults to 1.
            reverse_direction (bool, optional): Whether direction of segments should be reversed
                before meshing. Defaults to False.
            description (str, optional): Information/ notes on boundary to be retrieved from dict
                that can be used in FreeFem. Defaults to "".
            object_tag (int, optional): Tag of:
              - curve loop to use with 'from_outline' shape or
              - surface to use with 'from_section' shape (3D only)
              - volume to use with 'from_volume' shape (3D only)
        Returns:
            int: boundary surface tag
        """
        if self._domain_added and not self._intersections_run:
            geo_tag = self._create_verified_shape(
                shape=shape,
                centre=centre,
                width=width,
                height=height,
                depth=depth,
                theta=theta,
                object_tag=object_tag,
                rounded_radius=rounded_radius,
            )
            if geo_tag:
                shape_object = ShapeInfo(
                    tag=self._boundary_tag_value,
                    description=description,
                    geo_tag=geo_tag,
                )
                self.boundaries.append(shape_object)
                self._boundary_tag_value += 1

                return shape_object
        else:
            logger.warning(
                "Boundaries can only be added once background is created"
                " and before intersections are processed"
            )

    def run_intersections(self):
        """Fuse all defined shapes with the background. The intersections are subsequently
        processed with conformal interfaces.

        The method is using occ-generated fragments (intersecting surfaces or line segments)
        by wrapping the general fuse method. This takes in surfaces and boundaries and
        returns their conformal fragments with recomputed interfaces, mapped to the original
        surfaces/boundaries. We then iterate over the fragments map using _resolve_fragments,
        starting from the last shape added, delete duplicate fragmets and remap.
        Lastly, mesh points are added to internal borders and physical groups to boundaries and
        internal permittivity cores.

        """
        self.domain_attributes.tag = self._permittivity_tag_value
        self._permittivity_tag_value += 1
        # check if elements other than the domain are in the model
        if len(self.inner_regions) > 0 or len(self.boundaries) > 0:
            # process boundaries and inner_regions with domain and output
            # fragments (objects subdivided where intersecting)
            fragments = general_fuse_objects(
                object_to_fuse_to=[self.domain_attributes.geo_tag],
                objects_to_fuse_with=[
                    shape
                    for shape in [shape.geo_tag for shape in self.inner_regions]
                    + [shape.geo_tag for shape in self.boundaries]
                ],
                dim=self.dim,
            )

            # process fragments to remove overlaps
            resolved_fragments = self._resolve_fragments(
                fragments_collection=fragments[1]
            )

            synchronise()

            # add physical group to background
            background_fragments = self._compress_list(resolved_fragments[0])
            add_physical_group(
                objects=background_fragments,
                tag=self.domain_attributes.tag,
                dim=self.dim,
            )

            # process solid inner shapes and boundaries, starting from the last
            # shape added
            self._mark_physical_groups(resolved_fragments)

            # process domain boundaries
            self.add_physical_group_domain_boundary(background_fragments)

            # append domain boundaries to boundaries list (already processed)
            self.boundaries.append(
                ShapeInfo(tag=self._domain_boundary_tag, description="domainBoundary")
            )

            self._intersections_run = True
            return resolved_fragments
        else:
            # if there is only domain present, add a physical group to domain volume
            # and physical groups to domain boundaries and terminate
            background_fragments = [self.domain_attributes.geo_tag]
            add_physical_group(
                objects=background_fragments,
                tag=self.domain_attributes.tag,
                dim=self.dim,
            )
            self.add_physical_group_domain_boundary(background_fragments)
            self._intersections_run = True
            return []

    def add_physical_group_domain_boundary(self, background_fragments: list):
        """Add physical group to domain boundaries - reconstruct the curve/ surface loops
        of boundary surface/ volume and use boundary tag to create a physical group

        Args:
            background_fragments (list): background objects - surfaces/ volumes
        """
        segments = self._flatten_list(
            [
                get_loops(background_fragment, dim=self.dim)[1][0]
                for background_fragment in background_fragments
            ]
        )

        # add boundary physical group
        add_physical_group(
            segments,
            tag=self._domain_boundary_tag,
            dim=self.dim - 1,
        )

        # add boundary mesh fields
        self._mesh_fields.append(
            set_mesh_size_at_objects(
                curves=segments if self.dim == 2 else [],
                surfaces=segments if self.dim == 3 else [],
                size_min=self.domain_boundary_mesh_size,
                size_max=self.max_mesh_size,
                threshold_lower=self.mesh_size_dist_threshold_lower,
                threshold_upper=self.mesh_size_dist_threshold_upper,
            )
        )

    def _mark_physical_groups(self, resolved_fragments: list):
        """Add physical groups definitions for boundaries and inner regions

        Args:
            resolved_fragments (list): list of post-processed unique fragments
        """
        # enumerate fragments list backwards, excluding domain
        bounds_min = None
        for i, resolved_fragment in enumerate(list(reversed(resolved_fragments[1:]))):
            fused_objects = resolved_fragment
            # mesh_size = self.internal_region_mesh_size
            # if processing boundary, adjust mesh size and fuse objects to avoid
            # floating boundary edges

            if i <= len(self.boundaries) - 1:
                if len(resolved_fragment) > 1:
                    fused_objects = fuse_objects(
                        [resolved_fragment[0]], resolved_fragment[1:]
                    )[0]
                    synchronise()

                objects_tags = self._compress_list(fused_objects)

                for object_tag in objects_tags:
                    segments = self._flatten_list(
                        get_loops(object_tag, dim=self.dim)[1]
                    )
                    self._mesh_fields.append(
                        set_mesh_size_at_objects(
                            curves=segments if self.dim == 2 else [],
                            surfaces=segments if self.dim == 3 else [],
                            size_min=self.internal_boundary_mesh_size,
                            size_max=self.max_mesh_size,
                            threshold_lower=self.mesh_size_dist_threshold_lower,
                            threshold_upper=self.mesh_size_dist_threshold_upper,
                        )
                    )

                    # add physical groups for boundary segments

                    add_physical_group(
                        segments,
                        tag=self.boundaries[len(self.boundaries) - 1 - i].tag,
                        dim=self.dim - 1,
                    )

            # add physical groups for inner shapes
            else:
                objects_tags = self._compress_list(fused_objects)
                self.inner_regions[len(resolved_fragments) - 2 - i].tag = (
                    self._permittivity_tag_value
                )

                if objects_tags:
                    bounds_inner = get_bounding_box(objects_tags[0], dim=self.dim)
                    if bounds_min:
                        bounds_min[:3] = np.minimum(bounds_min[:3], bounds_inner[:3])
                        bounds_min[3:] = np.maximum(bounds_min[3:], bounds_inner[3:])
                    else:
                        bounds_min = list(bounds_inner)

                    add_physical_group(
                        objects_tags,
                        tag=self._permittivity_tag_value,
                        dim=self.dim,
                    )

                self._permittivity_tag_value += 1
        if bounds_min:
            self._mesh_fields.append(
                set_mesh_size_within_box(
                    size_inside=self.internal_region_mesh_size,
                    size_outside=self.max_mesh_size,
                    x_min=bounds_min[0],
                    x_max=bounds_min[3],
                    y_min=bounds_min[1],
                    y_max=bounds_min[4],
                    z_min=bounds_min[2],
                    z_max=bounds_min[5],
                )
            )
        self._intersections_run = True

    def generate_mesh(
        self,
        *,
        save: bool = True,
        directory: Union[str, pathlib.Path] = pathlib.Path().absolute(),
        filename: str = "output",
        extension: str = "mesh",
        algorithm: str = "Frontal-Delaunay",
    ):
        """Following geometry definition, generate mesh.

        Args:
            save (bool, optional): Save mesh to file. Defaults to True.
            directory (Union[str, pathlib.Path], optional): Mesh file directory.
                Defaults to pathlib.Path().absolute().
            filename (str, optional): Mesh filename (without extension).
                Defaults to "mesh_output".
            extension (str): mesh file extension. Defaults to "mesh".

        """
        if self._domain_added:
            if not self._intersections_run:
                logger.info(
                    "Intersections need to be processed before meshing - "
                    "computing intersections"
                )
                self.run_intersections()

            # compute mesh sizes from distance fields
            mesh_fields_set(fields_list=self._mesh_fields)
            synchronise()

            run_mesh_generation(dim=self.dim)
            set_meshing_algorithm(algorithm=algorithm)

            if save:
                self.save_mesh(
                    directory=directory,
                    filename=f"{filename}_mesh",
                    extension=extension,
                )
                self._save_permittivity_files(
                    directory=directory,
                    filename=f"{filename}_parameter_mapping",
                )
        else:
            logger.warning("Domain needs to be added before meshing.")

    def save_mesh(self, *, directory=".", filename="test", extension="mesh"):
        """Save mesh file.

        Args:
            directory (Union[str, pathlib.Path], optional): Mesh file directory.
                Defaults to pathlib.Path().absolute().
            filename (str, optional): Mesh filename (without extension).
                Defaults to "mesh_output".
            extension (str, optional): mesh file extension. Defaults to "mesh".
        """
        directory_path = pathlib.Path(directory)
        directory_path.mkdir(parents=True, exist_ok=True)
        path = pathlib.Path(directory / f"{filename}.{extension}").as_posix()
        save_mesh_to_path(path)

    def set_mesh_size_params(
        self,
        *,
        internal_boundary: float = None,
        internal_region: float = None,
        domain_boundary: float = None,
        max_size: float = None,
        threshold_lower: float = None,
        threshold_upper: float = None,
    ):
        """Provide mesh_size parameters for mesh size setting points added in
        run_intersections(). If no argument for a given outline type is provided,


        Args:
            internal_boundary (float, optional): mesh size at internal boundary.
                Defaults to None.
            internal_region (float, optional): mesh size for internal regions.
                Defaults to None.
            domain_boundary (float, optional): mesh size at domain boundary.
                Defaults to None.
        """
        if internal_boundary:
            self.internal_boundary_mesh_size = internal_boundary

        if internal_region:
            self.internal_region_mesh_size = internal_region

        if domain_boundary:
            self.domain_boundary_mesh_size = domain_boundary

        if max_size:
            self.max_mesh_size = max_size

        if threshold_lower:
            self.mesh_size_dist_threshold_lower = threshold_lower

        if threshold_upper:
            self.mesh_size_dist_threshold_upper = threshold_upper

    def get_permittivity_tag_dict(self) -> dict[str, list[ShapeInfo]]:
        """Getter for permittivity tag dictionary to cross reference permittivity values

        Returns:
            dict: permittivity tag dictionary: permittivity_tag: permittivity
        """
        if self.inner_regions or self.domain_attributes:
            all_permittivity_regions = [self.domain_attributes] + self.inner_regions
            # filter permittivity regions to ensure the ones covered don't get printed
            filtered_permittivity_regions = [
                region for region in all_permittivity_regions if region.tag
            ]
            region_types = np.unique(
                [region.description for region in filtered_permittivity_regions]
            )
            shape_info_dict = {
                key: sorted(
                    [
                        region
                        for region in filtered_permittivity_regions
                        if region.description == key
                    ],
                    key=lambda x: x.tag,
                )
                for key in region_types
            }
            if "pixels" not in shape_info_dict.keys():
                shape_info_dict["pixels"] = []

            return shape_info_dict

        else:
            return dict()

    def get_boundary_tag_dict(self) -> dict[str, list[str]]:
        """Getter for boundary tag dictionary with keys given by the description
        of each boundary

        Returns:
            dict: boundary tag dictionary[description: list[tags]]
        """
        if self.boundaries:
            bdry_types = np.unique([bdry.description for bdry in self.boundaries])
            return {
                key: [
                    str(bdry.tag) for bdry in self.boundaries if bdry.description == key
                ]
                for key in bdry_types
            }
        else:
            return dict()

    def _resolve_fragments(
        self, fragments_collection: list = [], index: int = None
    ) -> list:
        """Function removing nested and common fragments recursively from the
        last shape added to the last.

        Args:
            fragments_collection (list, optional): a nested list of tuples, each
                sublist defining set of fragments adding up to original shape.
                Defaults to [].
            index (int, optional): Index of last shape already processed (reversed).
                Defaults to None.

        Returns:
            list: refined list of list of tuples with common/ nested elements removed
        """
        if index is None:
            if not fragments_collection:
                return logger.warning("Method requires nested list of tuples as input")
            index = len(fragments_collection) - 1
            return self._resolve_fragments(fragments_collection, index)
        elif index == 0:
            return fragments_collection
        else:
            refined_fragments = []

            for fragments_to_refine in fragments_collection[:index]:
                refined_fragments.append(
                    [
                        fragment
                        for fragment in fragments_to_refine
                        if fragment not in fragments_collection[index]
                    ]
                )
            index -= 1
            return self._resolve_fragments(
                refined_fragments + fragments_collection[(index + 1) :],  # noqa: E203
                index,
            )

    def _create_verified_shape(
        self,
        *,
        shape: str,
        centre: tuple,
        width: float,
        height: float,
        depth: float = None,
        theta: float = 0,
        object_tag: int = None,
        rounded_radius: float = 0,
    ) -> int:
        """Create shape and check if it is nested in background, if not, remove

        Args:
            shape (str): Geometrical shape name.
            centre (tuple): Centre coordinates.
            width (float): Total width.
            height (float): Total height.
            permittivity (float): permittivity value
            object_tag (int, optional): Tag of:
              - curve loop to use with 'from_outline' shape or
              - surface to use with 'from_section' shape (3D only)
              - volume to use with 'from_volume' shape (3D only)
        Returns:
            int: tag of verified shape
        """
        if self.dim == 2:
            object_tag = self._create_shape(
                shape=shape,
                centre=centre,
                width=width,
                height=height,
                theta=theta,
                object_tag=object_tag,
                rounded_radius=rounded_radius,
            )
        else:
            object_tag = self._create_shape(
                shape=shape,
                centre=centre,
                width=width,
                height=height,
                depth=depth,
                object_tag=object_tag,
            )

        if self._check_if_nested(object_tag=object_tag):
            return object_tag
        else:
            logger.warning(
                "Shape must be fully nested in the background. Shape not generated"
            )
            remove_entities(tags=[object_tag], dim=self.dim)

    def _check_if_nested(self, *, object_tag: int) -> bool:
        """Check if a surface created from loop_tag  is nested in background
        surface
        Args:
            loop_tag (int): loop tag of shape that requires verification
        Returns:
            bool: output of check - True if nested
        """
        cut_output = cut_objects(
            objects_to_be_cut=[object_tag],
            cutters=[self.domain_attributes.geo_tag],
            dim=self.dim,
        )
        return not bool(cut_output[0])

    @staticmethod
    def _check_shape_list(shape: str, shape_class: Type = Shape2D):
        shape_found = False
        for shp in shape_class:
            if shape == shp.name or shape == shp.value:
                shape = shp.name
                shape_found = True
                break
        if not shape_found:
            raise ValueError(
                f"Incorrectly specified shape input {shape}. "
                f"Choose from {[shape.name for shape in shape_class]}"
            )

    def _save_permittivity_files(
        self,
        *,
        directory: str = None,
        filename: str = None,
        override_filepath: str = None,
    ):
        """Internal function for permittivity files generation

        Args:
            directory (str): directory to save the files to
            filename (str): filename for tags file (without extension)
        """
        perm_dict = self.get_permittivity_tag_dict()
        bdry_dict = self.get_boundary_tag_dict()

        if override_filepath:
            pt = open(pathlib.Path(override_filepath), "w")
        else:
            if directory is None or filename is None:
                return ValueError(
                    "Directory and filename must be provided for permittivity mapping file generation"
                )
            directory_path = pathlib.Path(directory)
            directory_path.mkdir(parents=True, exist_ok=True)

            self._parameter_mapping_filepath = pathlib.Path(
                directory / f"{filename}.txt"
            )
            pt = open(self._parameter_mapping_filepath, "w")

        for key, infos in perm_dict.items():
            pt.write(f"{key} {len(infos)}\n")
            if len(infos) > 0:
                pt.write("\n".join([f"{i.tag} {i.permittivity}" for i in infos]) + "\n")

        for key, tags in bdry_dict.items():
            pt.write(f"{key} {len(tags)}\n")
            pt.write(" ".join(tags) + "\n")

        pt.close()

    def update_permittivities(
        self,
        new_permittivities_dict: dict,
        use_sub_info: bool = True,
    ) -> list[ShapeInfo]:
        """Update inner_shapes list with new permittivities. Use either .sub_info tags
        or physical group tags (.tag) as key for new_permittivities_dict

        Args:
            new_permittivities_dict (dict, optional): keys are either .sub_info tags
                or physical group .tag; values are new permittivity values. Defaults to None.
            use_sub_info (bool, optional): use .sub_info rather than .tag keys.
                Defaults to True.

        Returns:
            list[ShapeInfo]: Current list of inner regions ShapeInfo
        """
        for shape in self.inner_regions:
            if use_sub_info:
                if shape.sub_info in list(new_permittivities_dict.keys()):
                    shape.permittivity = new_permittivities_dict[shape.sub_info]
            else:
                if shape.tag in list(new_permittivities_dict.keys()):
                    shape.permittivity = new_permittivities_dict[shape.tag]
        self._save_permittivity_files(
            override_filepath=self._parameter_mapping_filepath
        )
        return self.inner_regions

    def update_pixels(self, new_permittivity_array: np.ndarray) -> list[ShapeInfo]:
        """Update permittivity information of 'pixels' objects within a post-processed geometry

        Args:
            new_permittivity_array (np.ndarray): array of permittivities for pixels

        Returns:
            list[ShapeInfo]: updated inner_regions list
        """
        # dismantle pixel information based on sub_info
        try:
            dims = list(np.shape(new_permittivity_array))
        except ValueError:
            logger.error("Invalid np array input as new_permittivity_array")
        if len(dims) > 3 or len(dims) < 1:
            return ValueError(
                f"Num dimensions {new_permittivity_array.ndim} in new pixel permittivity array incorrect"
            )

        if len(dims) == 1:
            tags_dict = {f"p_{i}": new_permittivity_array[i] for i in range(dims[0])}
        elif len(dims) == 2:
            tags_dict = {
                f"p_{i}_{j}": new_permittivity_array[i, j]
                for i in range(dims[0])
                for j in range(dims[1])
            }
        else:
            tags_dict = {
                f"p_{i}_{j}_{k}": new_permittivity_array[i, j, k]
                for i in range(dims[0])
                for j in range(dims[1])
                for k in range(dims[2])
            }

        return self.update_permittivities(new_permittivities_dict=tags_dict)

    @abstractmethod
    def _create_shape(
        self,
        *,
        shape: str,
        centre: tuple,
        width: float,
        height: float,
        theta: float = 0,
        object_tag: int = None,
        rounded_radius: float = 0,
    ) -> tuple:
        """Basic shape creation manager and verifier.

        Args:
            shape (str): Geometrical shape name.
            centre (tuple): Centre coordinates.
            width (float): Total width.
            height (float): Total height.
            theta (float): angle for rotation in (x,y) plane
            outline_loop = object_tag

        Raises:
            ValueError: if incorrect shape type is specified
            ValueError: if 'from_outline' is specified but no curve loop tag provided

        Returns:
            tuple: curve loop, segments list
        """
        raise NotImplementedError

    def _rotate_point(
        self,
        x: tuple,
        theta: float = 0,
        centre: tuple = (0, 0, 0),
        degrees: int = 0,
    ) -> tuple:
        """
        Function which takes a point (x, y, z) and returns the point rotated anticlockwise in x-y plane
        by theta about the point (x_center, y_center, z_center)

        Args:
            x (tuple, required): (x,y,z) coordinate of point
            theta (float, required): Rotation angle (radians). Defaults to 0
            centre (tuple, optional): coordinate of rotation point. Default to (0,0,0)
            degrees (int, optional): Used if theta is given in degrees not radians

        Returns:
            tuple:
                (x,y,z) coordinate of rotated point
        """
        if degrees:
            theta = 180 * theta / np.pi

        rotation_matrix = np.array(
            [
                [np.cos(theta), -np.sin(theta), 0],
                [np.sin(theta), np.cos(theta), 0],
                [0, 0, 1],
            ]
        )

        x_rotated = np.matmul(rotation_matrix, x - centre)

        return x_rotated + centre

    @staticmethod
    def _flatten_list(nested_list: list) -> list:
        """Helper function to flatten nested lists (one level)

        Args:
            nested_list (list): list of lists to flatten

        Returns:
            list: flattened list
        """
        return list(itertools.chain(*nested_list))

    @staticmethod
    def _compress_list(tuple_list: list) -> list:
        """Helper function to convert list of tuples to list of objects
        without dimensional information

        Args:
            tuple_list (list): input list e.g. [(2, 5), (2,1)]

        Returns:
            list: distilled object tags
        """
        return [tag for (_, tag) in tuple_list]


class GeometricModel2D(GeometricModel):
    def __init__(self):
        super().__init__()

    def _create_shape(
        self,
        *,
        shape: str,
        centre: tuple,
        width: float,
        height: float,
        theta: float = 0,
        object_tag: int = None,
        rounded_radius: float = 0,
    ) -> int:
        """Basic shape creation manager and verifier - 2D

        Args:
            shape (str): Geometrical shape name.
            centre (tuple): Centre coordinates.
            width (float): Total width.
            height (float): Total height.
            theta (float): angle for rotation in (x,y) plane
            radius_curvature (float): radius of curvature of curved rectangle
            object_tag (int): Tag of curve loop to use with 'from_outline' shape

        Raises:
            ValueError: if incorrect shape type is specified
            ValueError: if 'from_outline' is specified but no curve loop tag provided

        Returns:
            int: surface tag
        """

        self._check_shape_list(shape=shape, shape_class=Shape2D)
        if shape == "ellipse":
            outline_loop = self._add_ellipse_outline(
                centre=centre, width=width, height=height
            )
        elif shape == "rectangle":
            outline_loop = self._add_rectangle_outline(
                centre=centre, width=width, height=height, theta=theta
            )
        elif shape == "rounded_rectangle":
            return add_rectangle(
                centre=centre,
                width=width,
                height=height,
                radius=rounded_radius,
            )
        elif shape == "from_outline":
            if object_tag:
                outline_loop = object_tag
            else:
                raise ValueError(
                    "To use 'from_outline' option, outline_loop tag must be speficied"
                )

        surface_tag = add_surface(curve_loops_tags=[outline_loop])
        return surface_tag

    def _add_rectangle_outline(
        self,
        *,
        centre: tuple = (0, 0, 0),
        width: float = 1,
        height: float = 1,
        theta: float = 0,
        ifdegrees: bool = 0,
    ) -> tuple:
        """
        Function for generating a rectangle, using centre coordinates and width and height
        Note that rectangle lines and loops are created in positive (anti-clockwise) direction

        Args:
            centre (tuple, optional): Centre coordinates. Defaults to (0, 0, 0).
            width (float, optional): Total width. Defaults to 1.
            height (float, optional): Total height. Defaults to 1.
            theta (float, optional): Angle of rotation (radians). Defaults to 0.
            ifdegrees (bool, optional): Used if rotation given in degrees.
            if_return_points (bool, optional): Used to return points of rectangle not outline

        Returns:
            tuple:
                outline_loop (int): curve loop tag
                edges (list): list of tags of curve loop segments
        """
        bottom_left, bottom_right, top_right, top_left = self._add_rectangle_points(
            centre=centre,
            width=width,
            height=height,
            theta=theta,
            ifdegrees=ifdegrees,
        )

        # Create edges
        bottom_edge = add_line(bottom_left, bottom_right)
        right_edge = add_line(bottom_right, top_right)
        top_edge = add_line(top_right, top_left)
        left_edge = add_line(top_left, bottom_left)
        edges = [bottom_edge, right_edge, top_edge, left_edge]

        outline_loop = add_loop(objects_to_loop=edges)
        return outline_loop

    def _add_rectangle_points(
        self,
        *,
        centre: tuple = (0, 0, 0),
        width: float = 1,
        height: float = 1,
        theta: float = 0,
        ifdegrees: bool = False,
    ):
        """Add rectangle points as intermittent rectangle generation, as well as for building arc
        based pixels

        Args:
            centre (tuple, optional): Centre coordinates. Defaults to (0, 0, 0).
           width (float, optional): Total width. Defaults to 1.
            height (float, optional): Total height. Defaults to 1.
            theta (float, optional): Angle of rotation (radians). Defaults to 0.
            ifdegrees (bool, optional): Used if rotation given in degrees.

        Raises:
            ValueError: If width/ height provided is zero or negative

        Returns:
            tuple: points (cartesian coordinates)
        """
        if width > 0 and height > 0:
            p = np.array([centre[0] - width / 2, centre[1] + height / 2, 0])
            p = self._rotate_point(x=p, theta=theta, centre=centre, degrees=ifdegrees)
            top_left = add_point(p[0], p[1], p[2])

            p = np.array([centre[0] - width / 2, centre[1] - height / 2, 0])
            p = self._rotate_point(x=p, theta=theta, centre=centre, degrees=ifdegrees)
            bottom_left = add_point(p[0], p[1], p[2])

            p = np.array([centre[0] + width / 2, centre[1] - height / 2, 0])
            p = self._rotate_point(x=p, theta=theta, centre=centre, degrees=ifdegrees)
            bottom_right = add_point(p[0], p[1], p[2])

            p = np.array([centre[0] + width / 2, centre[1] + height / 2, 0])
            p = self._rotate_point(x=p, theta=theta, centre=centre, degrees=ifdegrees)
            top_right = add_point(p[0], p[1], p[2])
            return bottom_left, bottom_right, top_right, top_left
        else:
            raise ValueError("Width and height must be > 0")

    def _add_ellipse_outline(
        self, centre: tuple = (0, 0, 0), width: float = 1, height: float = 1
    ):
        """
        Function for generating an ellipse, using centre coordinates and width and height

        Args:
            centre (tuple, optional): Centre coordinates. Defaults to (0, 0, 0).
            width (float, optional): Total width. Defaults to 1.
            height (float, optional): Total height. Defaults to 1.

        Returns:
            tuple:
                outline_loop (int): curve loop tag
                edges (list): list of tags of curve loop segments
        """
        el_tag = add_ellipse(centre=centre, radius_x=width / 2, radius_y=height / 2)
        outline_loop = add_loop([el_tag])

        return outline_loop


class GeometricModel3D(GeometricModel):
    def __init__(self):
        super().__init__()
        self.dim = 3

    def _create_shape(
        self,
        *,
        shape: str,
        centre: tuple,
        width: float,
        height: float,
        depth: float,
        object_tag: int = None,
    ) -> int:
        """Basic shape creation manager and verifier - 3D

        Args:
            shape (str): Geometrical shape name.
            centre (tuple): Centre coordinates.
            width (float): Total width.
            height (float): Total height.
            depth (float): Total depth.
            object_tag (int, optional): Tag of:
              - curve loop to use with 'from_outline' shape or
              - surface to use with 'from_section' shape
              - volume to use with 'from_volume' shape

        Raises:
            ValueError: if incorrect shape type is specified
            ValueError: if 'from_outline' is specified but no curve loop tag provided

        Returns:
            int: volume tag
        """
        self._check_shape_list(shape=shape, shape_class=Shape3D)
        if shape == "ellipsoid":
            volume_tag = add_ellipsoid(
                centre=centre, width=width, height=height, depth=depth
            )
        elif shape == "box":
            volume_tag = add_box(
                centre=centre,
                width=width,
                height=height,
                depth=depth,
            )
        elif shape == "from_outline":
            if not object_tag:
                raise ValueError(
                    "To use 'from_outline' option, outline_loop tag must be speficied"
                )
            volume_tag = add_volume_from_outline(surface_loops_tags=[object_tag])
        elif shape == "from_section":
            if not object_tag:
                raise ValueError(
                    "To use 'from_section' option, section_surface tag must be speficied"
                )
            volume_tag = extrude_2D_objects(tags=[object_tag], dz=depth)
            translate_objects(tags=[volume_tag], dz=-depth / 2)
        elif shape == "from_volume":
            volume_tag = object_tag

        return volume_tag

    def rotate_pixels(
        self,
        *,
        shapes: list[ShapeInfo],
        rotation_idx: int = 0,
        use_raw_angle: bool = False,
        angle: float = None,
        num_rot_per_pi: int = 12,
    ):
        """Rotate 3D pixels around y axis, either using ind or raw angle

        Args:
            shapes (list[ShapeInfo]): list of shapes to rotate
            rotation_idx (int, optional): rotation index. Defaults to 0.
            use_raw_angle (bool, optional): flag to determine whether raw angle
                should be used instead of index. Defaults to False.
            angle (float, optional): if use_raw_angle selected, angle in radians.
                Defaults to None.
            num_rot_per_pi (int, optional): num of rotations per cycle.
                Defaults to 12.

        Raises:
            ValueError: wrong inputs pairing
        """
        if use_raw_angle:
            if not angle:
                raise ValueError(
                    "To rotate using raw angle, you need to specify theta_y value"
                    "No rotation applied"
                )
            return
        else:
            angle = rotation_idx / num_rot_per_pi * pi
        rotate_objects(
            tags=[shape.geo_tag for shape in shapes],
            theta_y=1,
            angle=angle,
            dim=self.dim,
        )
        synchronise()
