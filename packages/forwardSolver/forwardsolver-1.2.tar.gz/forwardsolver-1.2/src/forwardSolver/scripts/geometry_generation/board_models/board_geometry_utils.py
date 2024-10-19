from forwardSolver.scripts.geometry_generation.board_models.P1000_009_geometry import (
    GeometryP10002D,
)
from forwardSolver.scripts.geometry_generation.board_models.P3000_005_geometry import (
    GeometryP30002D,
    GeometryP30003D,
)
from forwardSolver.scripts.geometry_generation.geometry_generation import (
    GeometricModel,
)
from forwardSolver.scripts.geometry_generation.geometry_interface import (
    clear_models,
    is_initialised,
    set_verbosity,
)
from forwardSolver.scripts.params.forward_solver_params import ForwardSolverParams
from forwardSolver.scripts.utils.logging import close_logger, get_logger
from forwardSolver.scripts.utils.pixels import Pixels

logger = get_logger(__name__)


def generate_geometry_and_params(
    board_type: str,
    pixels: Pixels,
    ndim: int = 2,
    mesh_filename: str = None,
    mesh_size_internal_boundary: float = 5,
    mesh_size_domain_boundary: float = 20,
    mesh_size_internal_region: float = 10,
    mesh_size_max: float = 10,
    mesh_algorithm: str = "Frontal-Delaunay",
    mesh_threshold_lower: float = 3,
    mesh_threshold_upper: float = 15,
    verbosity: int = 0,
) -> tuple[ForwardSolverParams, GeometricModel]:
    """Generate geometry mesh for given board type with provided pixelation
    and return ForwardSolverParams to run the forward solver with that mesh/pixelation

    Args:
        board_type (str): what board is being generated
        pixels (Pixels): pixelation to include in the mesh
        ndim (int, optional): problem dimension (2D/3D). Defaults to 2.
        mesh_size_[
            internal_boundary,
            domain_boundary,
            internal_region
        ]: mesh_size parameters
        verbosity: level of gmsh verbosity
    Raises:
        ValueError: if incompatible board type and dimensionality

    Returns:
        ForwardSolverParams
    """
    _fpars = ForwardSolverParams.factory(board_type)

    if mesh_filename is None:
        mesh_filename = f"{board_type}_{ndim}D"

    if is_initialised():
        clear_models()

    # Get pixelation dimensions from pixels if possible (if not set to xMaterialW/H)
    try:
        region_width = float(pixels.region_width)
        region_height = float(pixels.region_height)
    except:  # noqa: E722
        # If not possible, set to None and it will be read from forward params geometry
        region_width = None
        region_height = None

    if board_type.lower() == "p1000-009":
        if ndim == 2:
            g = GeometryP10002D(_fpars)

            g.add_domain(
                shape="rectangle",
                width=_fpars.geometry.domain_width,
                height=_fpars.geometry.domain_height,
            )
            g.add_P1000_009_board()

            g.add_curved_rectangular_pixelation(
                pixels.permittivity_matrix,
                columns=pixels.num_pixel_columns,
                rows=pixels.num_pixel_rows,
                pixel_region_height=region_height,
            )
        else:
            raise ValueError(f"P1000 boards not implemented for {ndim}D.")

    elif board_type.lower() == "p3000-005":
        y_offset = (
            -(1 / 6) * _fpars.geometry.domain_height
            + _fpars.geometry.pcb_substrate_height
            + _fpars.geometry.mylar_gap
            + _fpars.geometry.mylar_thickness
            + _fpars.geometry.plastic_thickness
            + _fpars.geometry.material_gap
        )

        if ndim == 2:
            g = GeometryP30002D(_fpars)

            g.add_domain(
                shape="rectangle",
                width=_fpars.geometry.domain_width,
                height=_fpars.geometry.domain_height,
            )
            g.add_P3000_005_board()

            g.add_rectangular_pixelation(
                pixels.permittivity_matrix,
                columns=pixels.num_pixel_columns,
                rows=pixels.num_pixel_rows,
                y_offset=y_offset,
                material_height=region_height,
                material_width=region_width,
            )
        elif ndim == 3:
            # get pixelation region length
            try:
                region_length = float(pixels.region_length)
            except ValueError:
                region_length = None

            g = GeometryP30003D(_fpars)

            g.add_domain(
                shape="box",
                width=_fpars.geometry.domain_width,
                height=_fpars.geometry.domain_height,
                depth=_fpars.geometry.domain_length,
            )

            g.add_P3000_005_board()

            g.add_cuboid_pixelation(
                pixels.permittivity_matrix,
                columns=pixels.num_pixel_columns,
                rows=pixels.num_pixel_rows,
                layers=pixels.num_pixel_layers,
                y_offset=y_offset,
                material_height=region_height,
                material_length=region_length,
                material_width=region_width,
            )
    else:
        raise ValueError(f"Unrecognised board geometry {board_type}")

    g.set_mesh_size_params(
        internal_boundary=mesh_size_internal_boundary,
        domain_boundary=mesh_size_domain_boundary,
        internal_region=mesh_size_internal_region,
        max_size=mesh_size_max,
        threshold_lower=mesh_threshold_lower,
        threshold_upper=mesh_threshold_upper,
    )

    set_verbosity(verbosity)

    g.run_intersections()
    g.generate_mesh(filename=mesh_filename, algorithm=mesh_algorithm)

    return_params = ForwardSolverParams.factory(board_type)
    return_params.board = "imported"
    return_params.mesh_file = f"./{mesh_filename}_mesh.mesh"
    return_params.material_parameter_file = f"./{mesh_filename}_parameter_mapping.txt"
    return_params.dimension = ndim

    logger.info(
        f"Created forward solver params for mesh at {return_params.mesh_file} "
        f"\nwith parameter mapping {return_params.material_parameter_file}"
    )
    return return_params, g


def generate_geometry_from_params(
    params: ForwardSolverParams,
    mesh_filename: str = None,
    mesh_size_internal_boundary: float = 5,
    mesh_size_domain_boundary: float = 20,
    mesh_size_internal_region: float = 10,
    mesh_size_max: float = 10,
    mesh_algorithm: str = "Frontal-Delaunay",
    mesh_threshold_lower: float = 3,
    mesh_threshold_upper: float = 15,
    verbosity: int = 0,
) -> ForwardSolverParams:
    """
    Generate geometry mesh from given forward solver parameter specification
    """

    if mesh_filename is None:
        mesh_filename = f"{params.board}_{params.dimension}D"

    if is_initialised():
        clear_models()

    if params.board.lower().startswith("p1000"):
        if params.dimension == 2:
            g = GeometryP10002D(params)

            g.add_domain(
                shape="rectangle",
                width=params.geometry.domain_width,
                height=params.geometry.domain_height,
            )
            g.add_P1000_009_board()

            g.add_curved_rectangular_pixelation(
                params.pixels.permittivity_matrix,
                columns=params.pixels.num_pixel_columns,
                rows=params.pixels.num_pixel_rows,
            )
        else:
            raise ValueError(f"P1000 boards not implemented for {params.dimension}D.")

    elif params.board.lower().startswith("p3000"):
        y_offset = (
            -(1 / 6) * params.geometry.domain_height
            + params.geometry.pcb_substrate_height
            + params.geometry.mylar_gap
            + params.geometry.mylar_thickness
            + params.geometry.plastic_thickness
            + params.geometry.material_gap
        )
        if params.dimension == 2:
            g = GeometryP30002D(params)

            g.add_domain(
                shape="rectangle",
                width=params.geometry.domain_width,
                height=params.geometry.domain_height,
            )
            g.add_P3000_005_board()

            g.add_rectangular_pixelation(
                params.pixels.permittivity_matrix,
                columns=params.pixels.num_pixel_columns,
                rows=params.pixels.num_pixel_rows,
                y_offset=y_offset,
            )
        elif params.dimension == 3:
            g = GeometryP30003D(params)

            g.add_domain(
                shape="box",
                width=params.geometry.domain_width,
                height=params.geometry.domain_height,
                depth=params.geometry.domain_length,
            )
            # remove_physical_groups()
            g.add_P3000_005_board()

            g.add_cuboid_pixelation(
                params.pixels.permittivity_matrix,
                columns=params.pixels.num_pixel_columns,
                rows=params.pixels.num_pixel_rows,
                layers=params.pixels.num_pixel_layers,
                y_offset=y_offset,
            )
    else:
        raise ValueError(f"Unrecognised board geometry {params.board}")

    g.set_mesh_size_params(
        internal_boundary=mesh_size_internal_boundary,
        domain_boundary=mesh_size_domain_boundary,
        internal_region=mesh_size_internal_region,
        max_size=mesh_size_max,
        threshold_lower=mesh_threshold_lower,
        threshold_upper=mesh_threshold_upper,
    )

    set_verbosity(verbosity)

    g.run_intersections()
    g.generate_mesh(filename=mesh_filename, algorithm=mesh_algorithm)

    params.mesh_file = f"./{mesh_filename}_mesh.mesh"
    params.material_parameter_file = f"./{mesh_filename}_parameter_mapping.txt"
    params.board = "imported"
    logger.info(
        f"Created mesh for params {params} at {params.mesh_file} "
        f"\nwith parameter mapping {params.material_parameter_file}"
    )


close_logger(logger)
