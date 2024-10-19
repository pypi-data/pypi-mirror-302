from typing import Optional

import numpy as np

from forwardSolver.scripts.params.forward_solver_params import ForwardSolverParams
from forwardSolver.scripts.solver_forward_P1000 import SolverForwardP1000
from forwardSolver.scripts.utils.constants import (
    PICO_FARAD_TO_FARAD,
    RelativePermittivity,
)


def calculate_capacitance_for_phantom(
    *,
    pixel_type: str = "circular_phantom",
    circular_phantom_radius: float = 71.0,
    circular_phantom_bore_radii: list = [20.0, 15.0, 10.0, 7.5, 5.0],
    circular_phantom_bore_centre_distance: float = 41.0,
    circular_phantom_angle: float = 0.0,
    circular_phantom_thickness: Optional[float] = None,
    permittivity_matrix: np.ndarray = RelativePermittivity.AIR * np.ones((6)),
    permittivity_board: float = 4.0,
    permittivity_frame: float = 3.0,
    permittivity_solder_coat: float = 3.0,
    permittivity_background: float = RelativePermittivity.AIR,
    domain_height: float = 250,
    material_gap: float = 1.0,
    board_id: str = "P1000-009",
    time_end: float = 40,
    time_step: float = 0.4e-3,
    resistance_receive: float = 1.0,
) -> tuple:
    """

    Function to set the parameters and run the forward solver to obtain the
    capacitance of the phantom.

    Note:
        This is a convenience function used in the many notebooks.
        This is not tested separately because the capacitance calculation is
        tested thoroughly elsewhere.

    Args:
        pixel_type: type of pixel
        circular_phantom_radius: outer radius of the phantom
        circular_phantom_bore_radii: radii of the bores in the phantom
        circular_phantom_bore_centre_distance: the distance between centre of the phantom
                                                and that of the board.
        circular_phantom_angle: angle between the -ve vertical and first bore
        circular_phantom_thickness: thickness of the circular phantom
        permittivity_matrix: phantom permittivity matrix
        permittivity_board: board  permittivity
        permittivity_frame: frame permittivity
        permittivity_solder_coat: solder coat permittivity
        permittivity_background: background permittivity
        domain_height: height of the domain
        material_gap: gap between the board and the phantom
        board_id: the name of the board
        time_end: simulation end time
        time_step: simulation time step
        resistance_receive: receive resistance in mega ohms
    Returns:
        capacitances matrix in Farads
        forward solver parameters
    """

    params = ForwardSolverParams.factory(board_id)
    params.geometry.domain_height = domain_height
    params.geometry.material_gap = material_gap
    params.pixels.pixel_type = pixel_type
    params.pixels.circular_phantom_radius = circular_phantom_radius
    params.pixels.circular_phantom_bore_radii = circular_phantom_bore_radii
    params.pixels.circular_phantom_bore_centre_distance = (
        circular_phantom_bore_centre_distance
    )
    params.pixels.circular_phantom_angle = circular_phantom_angle
    params.pixels.circular_phantom_thickness = circular_phantom_thickness
    params.pixels.permittivity_matrix = permittivity_matrix
    params.pixels.num_pixel_rows = 1
    params.pixels.num_pixel_columns = len(params.pixels.permittivity_matrix)
    params.geometry.permittivity_board = permittivity_board
    params.geometry.permittivity_frame = permittivity_frame
    params.simulation.t_end = time_end
    params.simulation.t_step = time_step
    params.sensor.r_pulldown_on_receive = resistance_receive * np.ones(
        len(params.sensor.r_pulldown_on_receive)
    )
    params.geometry.permittivity_soldercoat = permittivity_solder_coat
    params.geometry.permittivity_background = permittivity_background

    solver_forward = SolverForwardP1000(
        params,
        is_cap_calculated=True,
        is_voltage_mat_calculated=False,
        use_cache_input=False,
    )
    return solver_forward.C_true * PICO_FARAD_TO_FARAD, params


def calculate_capacitance_for_p3000_phantom(
    *,
    pixel_type: str = "curved_rectangle",
    region_height: float = 80,
    region_width: float = 155,
    permittivity_matrix: np.ndarray = RelativePermittivity.AIR * np.ones((1)),
    permittivity_background: float = RelativePermittivity.AIR,
    domain_height: float = 250,
    domain_width: float = 300,
    material_gap: float = 1.0,
    board_id: str = "P3000-005",
    time_end: float = 10,
    time_step: float = 1 / (150),  # default is a sampling rate of 150 Msampels/s
    resistance_receive: float = 0.47,
    signal_time_rise: float = 0.05,
    signal_time_dwell: float = 20,
    signal_time_fall: float = 0.05,
    signal_time_period: float = 250,
    signal_voltage_max: float = 2.5,
) -> tuple:
    """
    Function to set the parameters and run the forward solver to obtain the
    capacitance of the phantom for P3000 board.

    Note:
        This is a convenience function used in the many notebooks.
        This is not tested separately because the capacitance calculation is
        tested thoroughly elsewhere.

    Args:
        pixel_type: type of pixel
        region_height: height of the pixel region
        region_width: width of the pixel region
        permittivity_matrix: phantom permittivity matrix
        permittivity_background: background permittivity
        domain_height: height of the domain
        domain_width: width of the domain
        material_gap: gap between the board and the phantom
        board_id: the name of the board
        time_end: simulation end time
        time_step: simulation time step
        resistance_receive: receive resistance in mega ohms


    Returns:
        capacitances matrix in Farads
        forward solver parameters
    """

    params = ForwardSolverParams.factory(board_id)
    params.geometry.domain_height = domain_height
    params.geometry.domain_width = domain_width
    params.geometry.material_gap = material_gap
    params.pixels.pixel_type = pixel_type
    params.pixels.region_height = region_height
    params.pixels.region_width = region_width
    params.pixels.permittivity_matrix = permittivity_matrix

    if len(permittivity_matrix.shape) == 1:
        params.pixels.num_pixel_rows = 1
        params.pixels.num_pixel_columns = len(params.pixels.permittivity_matrix)
    else:
        params.pixels.num_pixel_rows = permittivity_matrix.shape[0]
        params.pixels.num_pixel_columns = permittivity_matrix.shape[1]

    params.simulation.t_end = time_end
    params.simulation.t_step = time_step

    params.signal.t_dwell = signal_time_dwell
    params.signal.t_rise = signal_time_rise
    params.signal.t_fall = signal_time_fall
    params.signal.t_period = signal_time_period
    params.signal.v_max = signal_voltage_max

    params.sensor.r_pulldown_on_receive = resistance_receive * np.ones(
        len(params.sensor.r_pulldown_on_receive)
    )

    params.geometry.permittivity_background = permittivity_background

    solver_forward = SolverForwardP1000(
        params,
        is_cap_calculated=True,
        is_voltage_mat_calculated=False,
        use_cache_input=False,
    )
    return solver_forward.C_true * PICO_FARAD_TO_FARAD, params
