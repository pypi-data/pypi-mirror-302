import copy
from typing import Callable, Union

import numpy as np
import scipy
from scipy.optimize import OptimizeResult

from forwardSolver.scripts.params.forward_solver_params import ForwardSolverParams
from forwardSolver.scripts.solver_forward_P1000 import SolverForwardP1000
from forwardSolver.scripts.utils.device_data.device_data import DeviceData
from forwardSolver.scripts.utils.spice_forward_voltage import (
    SpiceSolver,
    pwl_source_from_device_data,
)


def calculate_l2_norm_of_voltage(device_data: DeviceData) -> float:
    """

    Calculate the l2 norm of the voltage signals in the device data object

    Args:
        device_data: Input device data object for which the l2 norm is calculated
    """
    num_electrodes, _, num_time_instances = device_data.knode_voltages.shape
    square_norm_l2_voltages = 0

    square_norm_l2_voltages += np.sum(np.square(device_data.tnode_voltages))

    square_norm_l2_voltages += np.sum(np.square(device_data.knode_voltages))

    return np.sqrt(
        square_norm_l2_voltages / (2 * num_time_instances * num_electrodes**2)
    )


def calculate_l2_error_in_voltages(
    device_data_1: DeviceData, device_data_2: DeviceData
) -> float:
    """

    Calculate the l2 norm of the differences in the voltage between the two device
    data objects.

    Args:
        device_data_1: the first device data object.
        device_data_2: the second device data object.

    Raises:
        ValueError: If the sizes of the two device data objects do not match.
    """
    if device_data_1.knode_voltages.shape != device_data_2.knode_voltages.shape:
        raise ValueError("Mismatch in the shapes of the two device data objects.")

    device_data_difference = DeviceData()

    device_data_difference.knode_voltages = (
        device_data_1.knode_voltages - device_data_2.knode_voltages
    )

    device_data_difference.tnode_voltages = (
        device_data_1.tnode_voltages - device_data_2.tnode_voltages
    )

    return calculate_l2_norm_of_voltage(device_data_difference)


def calculate_spice_voltages(
    params_forward_solver: ForwardSolverParams,
    use_ground_capacitances: bool = True,
    capacitance_matrix_full: np.ndarray = None,
    device_data_measured: DeviceData = None,
    pwl_subsample_interval: int = 100,
) -> DeviceData:
    """

    Apply the T node voltage from the measured device data object to compute the
    response voltages using the spice model.

    Args:
        params_forward_solver: The forward solver parameters used by the spice model.
        use_ground_capacitances: Whether the ground capacitances are used in
                                    voltage computation.
        capacitance_matrix_full: The full capacitance matrix including the
                                    ground capacitances.
        device_data_measured: The measured device data object whose T node voltage is
                                    injected to the spice model.
        pwl_subsample_interval: The interval at which the measured T node voltage is
                                    subsampled before applying as piecewise linear
                                    source voltages to the spice model.
    """
    source_voltage_list = pwl_source_from_device_data(
        device_data_measured,
        subsample_interval=pwl_subsample_interval,
    )
    spice_solver = SpiceSolver(
        params_forward_solver,
        capacitance_matrix=capacitance_matrix_full,
        use_ground_capacitances=use_ground_capacitances,
        pwl_source_list_at_tnode=source_voltage_list,
    )
    device_data = spice_solver.create_spice_device_data()
    return device_data


def calculate_voltages_with_stray_capacitances(
    capacitances_stray: Union[float, np.ndarray],
    params_forward_solver: ForwardSolverParams,
    capacitance_matrix_full: np.ndarray,
    device_data_measured: DeviceData,
    pwl_subsample_interval: int = 100,
) -> DeviceData:
    """
    Function that calculates the voltages for given stray capacitance values.

    Args:
        capacitances_stray: The stray capacitance values.
        params_forward_solver: The forward solver parameters for spice voltages.
        capacitance_matrix_full: The full capacitance matrix with ground capacitances.
        device_data_measured: Measured device data object to be applied
                                to the tnode of spice circuit.
        pwl_subsample_interval: The interval at which the measured tnode voltage is
                                    subsampled before applying as piecewise linear
                                    source voltages to the spice model.
    """
    params_forward_solver_copy = copy.deepcopy(params_forward_solver)
    params_forward_solver_copy.sensor.c_receive_multiplexer_off += capacitances_stray
    device_data_calculated = calculate_spice_voltages(
        params_forward_solver_copy,
        capacitance_matrix_full=capacitance_matrix_full,
        use_ground_capacitances=True,
        device_data_measured=device_data_measured,
        pwl_subsample_interval=pwl_subsample_interval,
    )

    return device_data_calculated


def calculate_voltage_error_with_stray_capacitances(
    capacitances_stray: Union[float, np.ndarray],
    params_forward_solver: ForwardSolverParams,
    device_data_measured: DeviceData,
    capacitance_matrix_full: np.ndarray,
    pwl_subsample_interval: int = 100,
) -> float:
    """

    Function to calculate the l2 error in the voltages between the device data object
    obtained from the input arguments and the measure device data object.

    Args:
        capacitances_stray: The stray capacitances used for voltage calculation.
        params_forward_solver: The forward solver parameters used in spice model.
        device_data_measured: The measured device data object against which
                                error is computed.
        capacitance_matrix_full: The full capacitance matrix with ground capacitances.
        pwl_subsample_interval: The interval at which the measured tnode voltage is
                                    subsampled before applying as piecewise linear
                                    source voltages to the spice model.

    Returns:
        L2 error between measured and calculated device data voltages.
    """
    device_data_calculated = calculate_voltages_with_stray_capacitances(
        capacitances_stray=capacitances_stray,
        params_forward_solver=params_forward_solver,
        capacitance_matrix_full=capacitance_matrix_full,
        device_data_measured=device_data_measured,
        pwl_subsample_interval=pwl_subsample_interval,
    )
    return calculate_l2_error_in_voltages(device_data_calculated, device_data_measured)


def callback_function(intermediate_result: OptimizeResult) -> None:
    """

    The callback function from the scipy optimizer to check the intermediate results.

    Args:
        intermediate_result: The intermediate result from scipy optimizer.
    """
    print(f"Current solution = {intermediate_result}")


def minimize_voltage_error(
    *,
    device_data_measured: DeviceData = None,
    objective_function: Callable = calculate_voltage_error_with_stray_capacitances,
    initial_guess_capacitance_stray: np.ndarray = None,
    params_forward_solver: ForwardSolverParams = None,
    min_capacitance_bound: float = 1e-3,
    max_capacitance_bound: float = 1e3,
    capacitance_matrix_full: np.ndarray = None,
    num_maximum_iterations: int = 5,
    tolerance: float = 1e-6,
    pwl_subsample_interval: int = 100,
) -> tuple:
    """

    This function uses the scipy optimizer to compute the stray capacitance values and
    the device data object that minimizes the error from the measured
    device data voltages.

    Args:
        device_data_measured: measured device data object
        objective_function: the objective function to be minimized
        initial_guess_capacitance_stray: initial guess for stray capacitance values.
        params_forward_solver: forward solver parameters.
        min_capacitance_bound:  minimum bound for stray capacitances in pF.
        max_capacitance_bound: maximum bound for stray capacitances in pF.
        capacitance_matrix_full: full capacitance matrix with ground capacitances on diagonal.
        num_maximum_iterations: maximum number of iterations of optimizer.
        tolerance: tolerance level used by scipy optimizer.
        pwl_subsample_interval: The interval at which the measured tnode voltage is
                                    subsampled before applying as piecewise linear
                                    source voltages to the spice model.
    Returns:
        Tuple of the optimal stray capacitances and the optimized device data object.

    Raises:
        TypeError: Checks if the device data object passed in is of the right type.
    """
    if params_forward_solver is None:
        params_forward_solver = ForwardSolverParams.factory("P1000-009")

    if initial_guess_capacitance_stray is None:
        initial_guess_capacitance_stray = np.zeros_like(
            params_forward_solver.sensor.c_receive_multiplexer_off
        )
    if not isinstance(device_data_measured, DeviceData):
        raise TypeError("Need to provide a valid device data object")
    if capacitance_matrix_full is None:
        solver_forward = SolverForwardP1000(
            params_forward_solver,
            is_cap_calculated=False,
            is_full_cap_calculated=True,
            is_voltage_mat_calculated=False,
        )
        capacitance_matrix = solver_forward.C_full

    num_electrodes = len(params_forward_solver.sensor.c_receive_multiplexer_off)
    bounds = [(min_capacitance_bound, max_capacitance_bound)] * num_electrodes

    args = (
        params_forward_solver,
        device_data_measured,
        capacitance_matrix,
        pwl_subsample_interval,
    )

    result = scipy.optimize.minimize(
        fun=objective_function,
        x0=initial_guess_capacitance_stray,
        args=args,
        bounds=bounds,
        tol=tolerance,
        callback=callback_function,
        options={"maxiter": num_maximum_iterations, "disp": True},
    )

    device_data_optimal = calculate_voltages_with_stray_capacitances(
        result.x,
        params_forward_solver,
        capacitance_matrix_full,
        device_data_measured,
        pwl_subsample_interval=pwl_subsample_interval,
    )
    return result.x, device_data_optimal
