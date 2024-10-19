import copy
import platform
from itertools import combinations

import numpy as np
import pytest
from mock import patch

from forwardSolver.scripts.params.forward_solver_params import ForwardSolverParams
from forwardSolver.scripts.solver_forward_P1000 import (
    SolverForwardP1000,
    SolverForwardP1000_00X,
)
from forwardSolver.scripts.utils.constants import MICROSECONDS_TO_SECONDS
from forwardSolver.scripts.utils.create_pixelation import (
    permittivity_array_to_matrix,
)
from forwardSolver.scripts.utils.input_generator_P1000_pulse import (
    InputGeneratorP1000Pulse,
)
from forwardSolver.scripts.utils.logging import close_logger, get_logger
from forwardSolver.scripts.utils.metrics import ExperimentMetric

params_X_dict = ForwardSolverParams.factory("P1000-00X").as_dict()
params_4_dict = ForwardSolverParams.factory("P1000-004").as_dict()
params_6_dict = ForwardSolverParams.factory("P1000-006").as_dict()
params_9_dict = ForwardSolverParams.factory("P1000-009").as_dict()

logger = get_logger(__name__)
# Some regression tests fail due to platform-dependent computation differences - this variable allows tests to pass
# on Windows when results are close enough, whilst maintaining strict regression testing in CI before merging can occur
OS_TO_DECIMAL_TOLERANCE_STRICT = {
    "Darwin": 4,
    "Linux": 10,
    "Windows": 3,
}

decimal_tolerance_strict = OS_TO_DECIMAL_TOLERANCE_STRICT[platform.system()]


def test_simple_capacitor_symmetry():
    """
    Ensure that the P1000-00X board has symmetric results regardless of which is the transmit and receive electrode.
    """
    params_X = ForwardSolverParams(**params_X_dict)
    input_generator = InputGeneratorP1000Pulse(params_X)
    t, V_transmit = input_generator.simulate()

    params_X.sensor.num_transmitter = 2
    solver_forward_cap = SolverForwardP1000_00X(params_X)
    V_electrode_2, Q_electrode = solver_forward_cap.simulate(t, V_transmit)

    params_X.sensor.num_transmitter = 1
    solver_forward_cap = SolverForwardP1000_00X(params_X)
    V_electrode_1, _ = solver_forward_cap.simulate(t, V_transmit)

    np.testing.assert_array_almost_equal(
        V_electrode_1[0, :], V_electrode_2[1, :], decimal=10
    )
    np.testing.assert_array_almost_equal(
        V_electrode_1[1, :], V_electrode_2[0, :], decimal=10
    )
    np.testing.assert_array_almost_equal(
        Q_electrode[0, :], -Q_electrode[1, :], decimal=8
    )


def test_simple_capacitor_constant_capacitances(mock_simulation_p1000_00x):
    """
    For a two-conductor system, the equation Q=CV holds. This test ensures that the equation is true for our
    P1000-00X simulation. Note that for systems containing more than 2 conductors we cannot use this simple equation.
    """
    params_X = ForwardSolverParams(**params_X_dict)
    input_generator = InputGeneratorP1000Pulse(params_X)
    t, V_transmit = input_generator.simulate()

    solver_forward_cap = SolverForwardP1000_00X(params_X)
    V_electrode, Q_electrode = solver_forward_cap.simulate(t, V_transmit)

    num_electrodes = V_electrode.shape[0]
    electrode_combs = combinations(range(num_electrodes), 2)

    for electrode_comb in list(electrode_combs):
        V_first_electrode = V_electrode[electrode_comb[0], :]
        V_second_electrode = V_electrode[electrode_comb[1], :]
        delta_V = V_second_electrode - V_first_electrode

        Q_first_electrode = Q_electrode[electrode_comb[0], :]
        Q_second_electrode = Q_electrode[electrode_comb[1], :]

        # The divide by two is due to capacitance typically leading to +Q and -Q
        # on the two electrodes, so it is truly half the charge difference
        half_delta_Q = (Q_second_electrode - Q_first_electrode) / 2

        C = half_delta_Q / delta_V

        # Rising edge does not show a constant capacitance
        idx_fall_start = int(params_X.signal.t_rise / params_X.simulation.t_step) + 2
        np.testing.assert_almost_equal(
            C[idx_fall_start:],
            params_X.sensor.c_sensor,
            decimal=2,
        )


def test_simple_capacitor_simple_regression(mock_simulation_p1000_00x):
    """
    Regression test to ensure that the P1000-00X simulation results don't accidentally get changed.
    """
    params_X = ForwardSolverParams(**params_X_dict)
    input_generator = InputGeneratorP1000Pulse(params_X)
    t, V_transmit = input_generator.simulate()

    params_X.sensor.num_transmitter = 1
    solver_forward_cap = SolverForwardP1000_00X(params_X)
    V_electrode, _ = solver_forward_cap.simulate(t, V_transmit)

    # Check voltage values at four points through the signal
    V_transmit = V_electrode[0, :]
    V_receive = V_electrode[1, :]

    length = len(V_transmit)

    V_transmit_test_measurements = [
        V_transmit[round(0.25 * length)],
        V_transmit[round(0.50 * length)],
        V_transmit[round(0.75 * length)],
        V_transmit[-1],
    ]
    # print(f"{V_transmit_test_measurements = }")  # Useful when updating values
    V_transmit_regression_measurements = [
        2.5,
        2.5,
        2.5,
        2.5,
    ]
    np.testing.assert_array_almost_equal(
        V_transmit_test_measurements,
        V_transmit_regression_measurements,
        decimal=10,
    )

    V_receive_test_measurements = [
        V_receive[round(0.25 * length)],
        V_receive[round(0.50 * length)],
        V_receive[round(0.75 * length)],
        V_receive[-1],
    ]
    # print(f"{V_receive_test_measurements = }")  # Useful when updating values
    V_receive_regression_measurements = [
        1.1496402654977296,
        0.7951557032974914,
        0.5499742932307772,
        0.3804491745645521,
    ]
    np.testing.assert_array_almost_equal(
        V_receive_test_measurements,
        V_receive_regression_measurements,
        decimal=10,
    )


def test_total_charge_sums_to_zero(mock_simulation_p1000_004):
    """
    Ensuring that the total charge on conductive elements in the system sums to zero.
    NB: This is using the P1000-004 simulation which uses the same code as the P1000-001 but has no probe capacitance.
    """
    params_4 = ForwardSolverParams(**params_4_dict)
    input_generator = InputGeneratorP1000Pulse(params_4)
    t, V_transmit = input_generator.simulate()

    solver_forward = SolverForwardP1000(params_4)
    _, Q_conductors = solver_forward.simulate(t, V_transmit)

    # Check that total charge sums to zero
    Q_total = np.sum(Q_conductors, axis=0)
    max_abs_Q_total = np.max(abs(Q_total))

    np.testing.assert_almost_equal(max_abs_Q_total, 0, decimal=13)


def test_capacitance_matrix_properties():
    """
    Confirm key properties of the capacitance matrix (diagonals are negative, off-diagonals are positive, symmetric)
    """
    params_4 = ForwardSolverParams(**params_4_dict)
    solver_forward = SolverForwardP1000(
        params_4,
        is_cap_calculated=True,
        is_voltage_mat_calculated=False,
        use_cache_input=False,
        use_cache_output=False,
    )
    C_true = solver_forward.C_true

    # Negative diagonal elements (allowing them to be zero if we wish to avoid computing them to save time)
    assert (np.sign(np.diagonal(C_true)) <= 0).all()

    # Symmetric
    (C_true == C_true.T).all()

    # Positive off-diagonals
    C_positive_check = copy.deepcopy(C_true)
    np.fill_diagonal(C_positive_check, 1)
    assert (np.sign(C_positive_check) == 1).all()


def test_board_symmetry_and_decreasing_voltages(mock_simulation_p1000_004):
    """
    Within an air-only setup and no noise, the simulation should be symmetric about the transmit electrode
    NB: This is using the P1000-004 simulation which uses the same code as the P1000-001 but has no probe capacitance.
    """
    params_4 = ForwardSolverParams(**params_4_dict)
    params_4.sensor.noise_power_pulldown_on_receive = 0.0

    input_generator = InputGeneratorP1000Pulse(params_4)
    t, V_transmit = input_generator.simulate()

    solver_forward_cap = SolverForwardP1000(params_4)
    V_electrodes, _ = solver_forward_cap.simulate(t, V_transmit)
    max_span = params_4.sensor.num_transmitter - 1

    for span in range(max_span):  # zero representing the closest electrodes
        np.testing.assert_almost_equal(
            V_electrodes[span, :], V_electrodes[-(1 + span), :], decimal=2
        )

    # Check that the absolute integrated voltages are decreasing with increasing span
    integrated_voltage = np.array([np.sum(np.abs(x)) for x in V_electrodes])
    for span in range(max_span):
        assert (
            integrated_voltage[max_span + span]
            > integrated_voltage[max_span + (span + 1)]
        )
        assert (
            integrated_voltage[max_span - span]
            > integrated_voltage[max_span - (span + 1)]
        )


def test_p1000_001_simple_regression(mock_simulation_p1000_004):
    """
    Regression test to ensure that the P1000-001 simulation results don't accidentally get changed.
    NB: This is using the P1000-004 simulation which uses the same code as the P1000-001 but has no probe capacitance.
    """
    params_4 = ForwardSolverParams(**params_4_dict)
    input_generator = InputGeneratorP1000Pulse(params_4)
    t, V_transmit = input_generator.simulate()

    solver_forward = SolverForwardP1000(params_4)
    V_electrode, _ = solver_forward.simulate(t, V_transmit)

    # Check voltage values at four points through the signal
    V_transmit = V_electrode[params_4.sensor.num_transmitter - 1, :]
    V_receive = V_electrode[4, :]

    length = len(V_transmit)

    V_transmit_test_measurements = [
        V_transmit[round(0.25 * length)],
        V_transmit[round(0.50 * length)],
        V_transmit[round(0.75 * length)],
        V_transmit[-1],
    ]
    # print(f"{V_transmit_test_measurements = }")  # Useful when updating values
    V_transmit_regression_measurements = [
        2.5,
        2.5,
        2.5,
        2.499999999999987,
    ]
    np.testing.assert_array_almost_equal(
        V_transmit_test_measurements,
        V_transmit_regression_measurements,
        decimal=decimal_tolerance_strict,
    )

    V_receive_test_measurements = [
        V_receive[round(0.25 * length)],
        V_receive[round(0.50 * length)],
        V_receive[round(0.75 * length)],
        V_receive[-1],
    ]
    # print(f"{V_receive_test_measurements = }")  # Useful when updating values
    V_receive_regression_measurements = [
        0.0749755409395487,
        0.0466729518320374,
        0.0290748133733691,
        0.0181590224706069,
    ]
    np.testing.assert_array_almost_equal(
        V_receive_test_measurements,
        V_receive_regression_measurements,
        decimal=decimal_tolerance_strict,
    )


# TODO - Is this function still necessary?
def test_solver_forward_values():
    """
    Ensure that the inputs are checked on instantiation and the outputs are checked before being returned.
    """
    with patch.object(SolverForwardP1000, "check_inputs") as mock_check_inputs:
        with patch.object(SolverForwardP1000, "calculate_voltages") as mock_calculate:
            with patch.object(
                SolverForwardP1000, "check_simulation"
            ) as mock_check_simulation:
                params_4 = ForwardSolverParams(**params_4_dict)
                solver_forward = SolverForwardP1000(params_4, use_cache_output=False)
                mock_check_inputs.assert_called_once()
                solver_forward.simulate(None, None, None, use_cached_voltage=False)
                mock_calculate.assert_called_once()
                mock_check_simulation.assert_called_once()

    with patch.object(SolverForwardP1000_00X, "check_inputs") as mock_check_inputs:
        with patch.object(
            SolverForwardP1000_00X, "calculate_voltages"
        ) as mock_calculate:
            with patch.object(
                SolverForwardP1000_00X, "check_simulation"
            ) as mock_check_simulation:
                params_X = ForwardSolverParams(**params_X_dict)
                solver_forward = SolverForwardP1000_00X(params_X)
                mock_check_inputs.assert_called_once()
                solver_forward.simulate(None, None)
                mock_calculate.assert_called_once()
                mock_check_simulation.assert_called_once()


def test_pixelation_invariance():
    """
    Confirm that the choice of pixelation does not affect the results of the forward solver
    """

    params_pixel_1_1 = ForwardSolverParams(**params_4_dict)
    params_pixel_1_1.pixels.num_pixel_rows = 1
    params_pixel_1_1.pixels.num_pixel_columns = 1
    params_pixel_3_2 = ForwardSolverParams(**params_4_dict)
    params_pixel_3_2.pixels.num_pixel_rows = 3
    params_pixel_3_2.pixels.num_pixel_columns = 2
    solver_forward_pixel_1_1 = SolverForwardP1000(
        params_pixel_1_1,
        is_cap_calculated=True,
        is_voltage_mat_calculated=False,
        use_cache_input=False,
        use_cache_output=False,
    )
    solver_forward_pixel_3_2 = SolverForwardP1000(
        params_pixel_3_2,
        is_cap_calculated=True,
        is_voltage_mat_calculated=False,
        use_cache_input=False,
        use_cache_output=False,
    )

    # May be very slight differences due to the difference in mesh with more pixels
    np.testing.assert_almost_equal(
        solver_forward_pixel_1_1.C_true,
        solver_forward_pixel_3_2.C_true,
        decimal=3,
    )


def test_full_capacitance_matrix_regression():
    """
    Confirm that the capacitance matrix calculated does not change if some modifications are made in forward solver.

    This test could be metged with test_capacitance_matrix_properties to speed up the test suite.
    """
    params_4 = ForwardSolverParams(**params_4_dict)
    solver_forward = SolverForwardP1000(
        params_4,
        is_cap_calculated=True,
        is_voltage_mat_calculated=False,
        use_cache_input=False,
        use_cache_output=False,
    )
    C_values_simulated = solver_forward.C_true
    N_electrodes = C_values_simulated.shape[0]
    C_values_simulated_upper_triangular = C_values_simulated[
        np.triu_indices(N_electrodes, k=1)
    ]  # The upper triangular part of the matrix
    C_values_regression_upper_triangular = np.array(
        [
            0.6206778428449439,
            0.1558648944420348,
            0.0600402018364186,
            0.0290040157502690,
            0.0168430156119906,
            0.0111723616676847,
            0.0081237311802297,
            0.0063499075480837,
            0.0055294382048835,
            0.0067727273974148,
            0.5460034248127159,
            0.1278642078315168,
            0.0468471358057952,
            0.0215531438436156,
            0.0120091325130534,
            0.0077769187642999,
            0.0056449854295130,
            0.0046779957059162,
            0.0055286974270049,
            0.5392470277235160,
            0.1246458394220950,
            0.0450779786708076,
            0.0204194451147078,
            0.0112654871414464,
            0.0073269355296851,
            0.0056457039804871,
            0.0063499125407658,
            0.5381308284248260,
            0.1240732866306476,
            0.0446959144858644,
            0.0202326497287922,
            0.0112625454745856,
            0.0077757925096462,
            0.0081215344248260,
            0.5379166451091919,
            0.1238762091659838,
            0.0447072279473282,
            0.0204191823415344,
            0.0120101321281482,
            0.0111719216337126,
            0.5378958144539099,
            0.1241010396848940,
            0.0450757531258260,
            0.0215534665975922,
            0.0168411610488121,
            0.5381880518622419,
            0.1246205601745632,
            0.0468400155385242,
            0.0289964880263450,
            0.5393634510856219,
            0.1278885053678928,
            0.0600416591286742,
            0.5461253738853898,
            0.1558469735130742,
            0.6206954950913061,
        ]
    )

    np.testing.assert_almost_equal(
        C_values_simulated_upper_triangular,
        C_values_regression_upper_triangular,
        decimal=decimal_tolerance_strict,
    )


def test_full_capacitance_matrix_width_ground_capacitances_off_diagonal():
    params_009 = ForwardSolverParams(**params_9_dict)

    solver_forward = SolverForwardP1000(
        params_009,
        is_cap_calculated=True,
        is_full_cap_calculated=True,
        is_voltage_mat_calculated=False,
    )

    C_true = solver_forward.C_true
    C_full = solver_forward.C_full
    C_full_diagonal_removed = C_full - np.diag(np.diag(C_full))

    np.testing.assert_equal(C_full_diagonal_removed, C_true)


def test_full_capacitance_matrix_width_ground_capacitances_diagonal_regression():
    params_009 = ForwardSolverParams(**params_9_dict)

    solver_forward = SolverForwardP1000(
        params_009,
        is_cap_calculated=False,
        is_full_cap_calculated=True,
        is_voltage_mat_calculated=False,
    )

    C_full = solver_forward.C_full
    C_full_diagonal = np.diag(C_full)

    C_full_diagonal_regression = np.array(
        [
            4.898872109,  # 4.8995150428,
            4.2681215636,  # 4.268016328,
            4.2227391562,  # 4.2224363716,
            4.2029304853,  # 4.2037690867,
            4.1934530933,  # 4.1930845515,
            4.1878414448,  # 4.1875176064,
            4.184625542,  # 4.1847205651,
            4.1831934504,  # 4.1832954489,
            4.1835616846,  # 4.1838777985,
            4.1861747226,  # 4.1859395708,
            4.1900050826,  # 4.1901779521,
            4.1988447143,  # 4.1984702976,
            4.21488511,  # 4.2153759633,
            4.2503926708,  # 4.2506444183,
            4.7788869206,  # 4.7802544642,
        ]
    )

    np.testing.assert_almost_equal(
        C_full_diagonal,
        C_full_diagonal_regression,
        decimal=decimal_tolerance_strict,
    )


def test_FEM_solvers():
    params = ForwardSolverParams(**params_4_dict)
    params.pixels.num_pixel_rows = 1
    params.pixels.num_pixel_columns = 2
    NP = params.pixels.num_pixel_rows * params.pixels.num_pixel_columns
    params.pixels.permittivity_matrix = permittivity_array_to_matrix(
        np.linspace(1, NP, NP), params
    )

    solver_forward = SolverForwardP1000(
        params,
        is_cap_calculated=True,
        is_voltage_mat_calculated=True,
        use_cache_input=False,
        use_cache_output=False,
        is_python_used_as_solver=True,
    )

    eps_update = solver_forward.compute_mesh_epsilon(
        params.pixels.permittivity_matrix, update_eps=False
    )

    np.testing.assert_almost_equal(solver_forward.eps, eps_update, decimal=12)

    """
    Test that the A matrix and K matrix are the same as the ones used in the FreeFem++ solver.
    """

    A, K = solver_forward.build_FE_matrices(params.pixels.permittivity_matrix)

    diffA = abs(A - solver_forward.sA)
    diffK = abs(K - solver_forward.sL[:, : -params.sensor.num_wings])
    np.testing.assert_almost_equal(diffA.max(), 0, decimal=12)  # check to within 1e-12
    np.testing.assert_almost_equal(diffK.max(), 0, decimal=12)  # check to within 1e-12

    """
    Test that the capacitance matrix calculated by solving in FreeFem++ is the same as
    the matrix computed by solving in python.
    """

    Cmat1 = solver_forward.C_true
    Cmat2 = solver_forward.calculate_capacitance_matrix(
        params.pixels.permittivity_matrix
    )
    results = ExperimentMetric.matrix_norm_of_difference(Cmat1, Cmat2)
    diff_norm = results["capacitance_matrix_norm_diff"]
    # results["capacitance_matrix_norm_diff_relative"] doesn't need to be
    # tested because it uses results['capacitance_matrix_norm_diff']
    logger.info(f"Difference between python and freefem solvers is: {diff_norm}")

    np.testing.assert_almost_equal(diff_norm, 0, decimal=9)  # check to within 1e-9


def test_FDconductivity_permitivity_equivalence():
    params = ForwardSolverParams(**params_9_dict)

    solver_forward = SolverForwardP1000(
        params,
        is_cap_calculated=True,
        is_voltage_mat_calculated=False,
        use_cache_input=False,
        use_cache_output=False,
        physics_model=0,
    )
    Cmat1 = solver_forward.C_true

    solver_forward2 = SolverForwardP1000(
        params,
        is_cap_calculated=True,
        is_voltage_mat_calculated=False,
        use_cache_input=False,
        use_cache_output=False,
        physics_model=1,
    )
    # Convert result to pF
    Cmat2 = 1e9 * np.real(solver_forward2.C_true)

    np.testing.assert_almost_equal(
        Cmat1,
        Cmat2,
        decimal=decimal_tolerance_strict,
    )


def test_FDconductivity_regression():
    params = ForwardSolverParams(**params_9_dict)

    params.pixels.num_pixel_rows = 1
    params.pixels.num_pixel_columns = 2
    NP = params.pixels.num_pixel_rows * params.pixels.num_pixel_columns
    params.pixels.permittivity_matrix = permittivity_array_to_matrix(
        np.linspace(1, NP, NP), params
    )
    params.pixels.conductivity_matrix = permittivity_array_to_matrix(
        np.linspace(5, 5 + NP, NP), params
    )
    solver_forward = SolverForwardP1000(
        params,
        is_cap_calculated=True,
        is_voltage_mat_calculated=False,
        use_cache_input=False,
        use_cache_output=False,
        physics_model=1,
    )
    C_values_simulated = solver_forward.C_true
    N_electrodes = C_values_simulated.shape[0]
    C_values_simulated_upper_triangular = C_values_simulated[
        np.triu_indices(N_electrodes, k=1)
    ]  # The upper triangular part of the matrix
    print(f"{C_values_simulated_upper_triangular}")  # Useful when updating values

    C_values_regression_upper_triangular = [
        2.00157918e-09 - 2.64054894e-14j,
        7.08740071e-10 - 1.59366781e-14j,
        6.79125074e-10 - 9.29597353e-15j,
        6.78073639e-10 - 4.08409820e-15j,
        6.78047117e-10 + 3.04322161e-16j,
        6.78155027e-10 + 4.07308204e-15j,
        6.78158045e-10 + 7.10241463e-15j,
        6.78003407e-10 + 9.10328266e-15j,
        6.78064209e-10 + 1.08339635e-14j,
        6.78019439e-10 + 1.22969475e-14j,
        6.78155952e-10 + 1.34840399e-14j,
        6.78063560e-10 + 1.43869884e-14j,
        6.78934900e-10 + 1.50414364e-14j,
        6.78142209e-10 + 1.53356768e-14j,
        1.98307769e-09 - 1.97788346e-14j,
        7.14775258e-10 - 1.09044305e-14j,
        6.85913714e-10 - 5.07576745e-15j,
        6.84927969e-10 - 4.26035044e-16j,
        6.85003387e-10 + 3.47873569e-15j,
        6.85005259e-10 + 6.58827598e-15j,
        6.84849018e-10 + 8.63170593e-15j,
        6.84910432e-10 + 1.03924238e-14j,
        6.84865210e-10 + 1.18787038e-14j,
        6.85003074e-10 + 1.30839171e-14j,
        6.84908991e-10 + 1.40008498e-14j,
        6.85767688e-10 + 1.46649775e-14j,
        6.84307027e-10 + 1.49697760e-14j,
        1.98226924e-09 - 1.53193665e-14j,
        7.13973674e-10 - 7.07860851e-15j,
        6.85162325e-10 - 1.77524597e-15j,
        6.84277684e-10 + 2.37854524e-15j,
        6.84245928e-10 + 5.59553137e-15j,
        6.84088682e-10 + 7.67838757e-15j,
        6.84149987e-10 + 9.45457650e-15j,
        6.84104813e-10 + 1.09472439e-14j,
        6.84242524e-10 + 1.21546128e-14j,
        6.84148522e-10 + 1.30723729e-14j,
        6.85005600e-10 + 1.37356060e-14j,
        6.83526098e-10 + 1.40484590e-14j,
        1.98190512e-09 - 1.19828268e-14j,
        7.14030083e-10 - 4.20497483e-15j,
        6.85321141e-10 + 6.37539990e-16j,
        6.84329246e-10 + 4.12735486e-15j,
        6.84138373e-10 + 6.30881315e-15j,
        6.84198504e-10 + 8.12551632e-15j,
        6.84153286e-10 + 9.63650503e-15j,
        6.84291005e-10 + 1.08518642e-14j,
        6.84196995e-10 + 1.17735421e-14j,
        6.85054110e-10 + 1.24370328e-14j,
        6.83573780e-10 + 1.27610351e-14j,
        1.98209022e-09 - 9.52443035e-15j,
        7.14121358e-10 - 2.18256559e-15j,
        6.85297034e-10 + 2.02128935e-15j,
        6.84146153e-10 + 4.43723508e-15j,
        6.84172665e-10 + 6.34649984e-15j,
        6.84126271e-10 + 7.89838341e-15j,
        6.84263943e-10 + 9.13160711e-15j,
        6.84169936e-10 + 1.00616575e-14j,
        6.85027016e-10 + 1.07268035e-14j,
        6.83546719e-10 + 1.10649082e-14j,
        1.98239409e-09 - 7.86787879e-15j,
        7.14128040e-10 - 1.10875745e-15j,
        6.85150369e-10 + 1.92271279e-15j,
        6.84216950e-10 + 4.05123264e-15j,
        6.84136934e-10 + 5.69614316e-15j,
        6.84273430e-10 + 6.96978220e-15j,
        6.84179381e-10 + 7.91827621e-15j,
        6.85036471e-10 + 8.58889494e-15j,
        6.83556153e-10 + 8.94485467e-15j,
        1.98280189e-09 - 6.91313841e-15j,
        7.14087729e-10 - 1.61678658e-15j,
        6.85322254e-10 + 1.08442063e-15j,
        6.84281934e-10 + 2.94892295e-15j,
        6.84384822e-10 + 4.31490908e-15j,
        6.84289578e-10 + 5.30439215e-15j,
        6.85146765e-10 + 5.98953678e-15j,
        6.83666207e-10 + 6.36902120e-15j,
        1.98263456e-09 - 7.50399598e-15j,
        7.14155743e-10 - 2.87135341e-15j,
        6.85280222e-10 - 4.64846242e-16j,
        6.84422773e-10 + 1.10852652e-15j,
        6.84293890e-10 + 2.18592543e-15j,
        6.85149902e-10 + 2.90442139e-15j,
        6.83669296e-10 + 3.31611883e-15j,
        1.98196119e-09 - 8.04933625e-15j,
        7.13942822e-10 - 3.92113596e-15j,
        6.85261693e-10 - 1.87951624e-15j,
        6.84172698e-10 - 6.24615138e-16j,
        6.84994892e-10 + 1.62269509e-16j,
        6.83513447e-10 + 6.15682318e-16j,
        1.98212229e-09 - 9.22199778e-15j,
        7.14151758e-10 - 5.42159815e-15j,
        6.85229112e-10 - 3.68562354e-15j,
        6.85091173e-10 - 2.72596463e-15j,
        6.83576002e-10 - 2.19492655e-15j,
        1.98225402e-09 - 1.10100343e-14j,
        7.14003866e-10 - 7.51128535e-15j,
        6.86040860e-10 - 6.08735834e-15j,
        6.83566808e-10 - 5.39094232e-15j,
        1.98257390e-09 - 1.34171296e-14j,
        7.15009043e-10 - 1.02711531e-14j,
        6.84730882e-10 - 9.15760842e-15j,
        1.98325034e-09 - 1.66197957e-14j,
        7.14355018e-10 - 1.39379272e-14j,
        2.00886819e-09 - 2.14618766e-14j,
    ]

    np.testing.assert_almost_equal(
        C_values_simulated_upper_triangular,
        C_values_regression_upper_triangular,
        decimal=decimal_tolerance_strict,
    )


def test_sensor_versions(mock_simulation_p1000_006):
    params_6 = ForwardSolverParams(**params_6_dict)
    Nt = int(params_6.simulation.t_end / params_6.simulation.t_step)
    Nt_split = int(np.floor(Nt / 2))
    input_generator = InputGeneratorP1000Pulse(params_6)
    t, V_transmit = input_generator.simulate()

    solver_forward = SolverForwardP1000(params_6)
    V_electrode, _ = solver_forward.simulate(t, V_transmit)

    assert (V_electrode > 0).any()  # At least one positive value

    # Test a very weak monotonicity-type condition.
    for i in range(11):
        if i + 1 != params_6.sensor.num_transmitter:
            assert np.mean(V_electrode[i, :Nt_split]) > np.mean(
                V_electrode[i, Nt_split:]
            )


def test_k_and_t_node_voltages():
    """Test the function to calculate T and K node voltages"""

    params_6 = ForwardSolverParams(**params_6_dict)
    Nt = int(params_6.simulation.t_end / params_6.simulation.t_step)
    Nt_split = int(np.floor(Nt / 2))
    input_generator = InputGeneratorP1000Pulse(params_6)
    t, V_transmit = input_generator.simulate()

    solver_forward = SolverForwardP1000(
        params_6,
        is_cap_calculated=False,
        is_voltage_mat_calculated=True,
        use_cache_input=False,
        use_cache_output=False,
    )
    voltage_knode, voltage_tnode = solver_forward.export_voltages_at_all_nodes(
        t, V_transmit
    )

    # At least one positive value in K and T node voltages
    assert (voltage_tnode > 0).any()
    assert (voltage_knode > 0).any()
    assert voltage_tnode.shape == voltage_knode.shape

    # Test a very weak monotonicity-type condition.
    for i in range(11):
        if i + 1 != params_6.sensor.num_transmitter:
            assert np.mean(voltage_tnode[i, :Nt_split]) > np.mean(
                voltage_tnode[i, Nt_split:]
            )
            assert np.mean(voltage_knode[i, :Nt_split]) > np.mean(
                voltage_knode[i, Nt_split:]
            )


def test_k_and_t_node_voltages_for_all_transmitters():
    """Test the function to calculate T and K node voltages
    for all transmitters"""

    params_6 = ForwardSolverParams(**params_6_dict)
    params_6.simulation.t_end = (
        params_6.simulation.t_end / 10
    )  # Need to test only a portion of the waveform for this test to save time

    input_generator = InputGeneratorP1000Pulse(params_6)
    t, V_transmit = input_generator.simulate()

    solver_forward = SolverForwardP1000(
        params_6,
        is_cap_calculated=False,
        is_voltage_mat_calculated=True,
        use_cache_input=False,
        use_cache_output=False,
    )

    # Calculate the T and K node voltages directly
    voltage_knode, voltage_tnode = solver_forward.export_voltages_at_all_nodes(
        t, V_transmit
    )

    # Calculate the T and K node voltage using the function for all
    # transmitters by specifying just one transmit electrode
    num_transmitter = params_6.sensor.num_transmitter
    (
        voltage_knode_for_all_transmitters,
        voltage_tnode_for_all_transmitters,
    ) = solver_forward.export_voltages_for_all_transmitters(
        t, V_transmit, array_of_transmitters=[num_transmitter]
    )

    # Assert that both the results are the same
    np.testing.assert_array_equal(
        voltage_knode, voltage_knode_for_all_transmitters[num_transmitter - 1]
    )
    np.testing.assert_array_equal(
        voltage_tnode, voltage_tnode_for_all_transmitters[num_transmitter - 1]
    )


def test_phantom_pixelation():
    params_9 = ForwardSolverParams(**params_9_dict)
    params_9.pixels.pixel_type = "curved_rectangle"
    params_9.geometry.domain_height = 250
    solver_forward_curved_rectangle_pixels = SolverForwardP1000(
        params_9,
        is_cap_calculated=True,
        is_voltage_mat_calculated=False,
        use_cache_input=False,
        use_cache_output=False,
    )
    params_9.pixels.pixel_type = "circular_phantom"
    params_9.pixels.num_pixel_rows = 1
    params_9.pixels.num_pixel_columns = 6
    solver_forward_circular_phantom = SolverForwardP1000(
        params_9,
        is_cap_calculated=True,
        is_voltage_mat_calculated=False,
        use_cache_input=False,
        use_cache_output=False,
    )
    np.testing.assert_allclose(
        solver_forward_curved_rectangle_pixels.C_true,
        solver_forward_circular_phantom.C_true,
        rtol=2e-3,
    )

    with pytest.raises(ValueError) as exc:
        params_9.pixels.pixel_type = "abc"
        solver_forward_circular_phantom = SolverForwardP1000(
            params_9,
            is_cap_calculated=False,
            is_voltage_mat_calculated=False,
            use_cache_input=False,
            use_cache_output=False,
        )

    valid_pixels = [
        "curved_rectangle",
        "curved_rectangle_nonuniform",
        "circular_phantom",
    ]

    assert (
        str(exc.value)
        == f"The pixel type {params_9.pixels.pixel_type} does not fall in the list "
        + f"of valid choices:{valid_pixels}"
    )
    params_9.pixels.pixel_type = "circular_phantom"

    with pytest.raises(ValueError) as exc:
        params_9.pixels.num_pixel_columns = (
            len(params_9.pixels.circular_phantom_bore_radii) + 2
        )
        solver_forward_circular_phantom = SolverForwardP1000(
            params_9,
            is_cap_calculated=False,
            is_voltage_mat_calculated=False,
            use_cache_input=False,
            use_cache_output=False,
        )

    assert (
        str(exc.value)
        == f"The num_pixel_rows {params_9.pixels.num_pixel_rows} "
        + f"and pixel columns {params_9.pixels.num_pixel_columns} "
        + "are inconsistent with the phantom parameters."
        + f"Should be 1x{len(params_9.pixels.circular_phantom_bore_radii)+1}."
    )
    params_9.pixels.num_pixel_columns = (
        len(params_9.pixels.circular_phantom_bore_radii) + 1
    )

    with pytest.raises(ValueError) as exc:
        params_9.pixels.circular_phantom_bore_radii[0] = (
            params_9.pixels.circular_phantom_radius
            - params_9.pixels.circular_phantom_bore_centre_distance * 0.999
        )
        solver_forward_circular_phantom = SolverForwardP1000(
            params_9,
            is_cap_calculated=False,
            is_voltage_mat_calculated=False,
            use_cache_input=False,
            use_cache_output=False,
        )

    assert (
        str(exc.value)
        == f"The value {params_9.pixels.circular_phantom_bore_radii} is inconsistent"
    )


def test_pixelation_curved_rectangle_nonuniform():
    """Test if the non-uniform pixelation gives the same result
    as the uniform pixelation for the same permittivities."""

    params_9 = ForwardSolverParams(**params_9_dict)
    params_9.pixels.pixel_type = "curved_rectangle"
    params_9.pixels.num_pixel_rows = 2
    params_9.pixels.num_pixel_columns = 1
    params_9.pixels.permittivity_matrix = np.array([[3], [8]])
    solver_forward_curved_rectangle = SolverForwardP1000(
        params_9,
        is_cap_calculated=True,
        is_voltage_mat_calculated=False,
        use_cache_input=False,
        use_cache_output=False,
    )

    params_9.pixels.pixel_type = "curved_rectangle_nonuniform"
    params_9.pixels.num_pixel_rows = 2
    params_9.pixels.num_pixel_columns = 3
    params_9.pixels.pixel_columns_per_row = np.array([2, 3])
    params_9.pixels.permittivity_matrix = np.array([3, 3, 8, 8, 8])
    solver_forward_curved_rectangle_nonuniform = SolverForwardP1000(
        params_9,
        is_cap_calculated=True,
        is_voltage_mat_calculated=False,
        use_cache_input=False,
        use_cache_output=False,
    )

    np.testing.assert_allclose(
        solver_forward_curved_rectangle.C_true,
        solver_forward_curved_rectangle_nonuniform.C_true,
        rtol=2e-3,
    )


@pytest.fixture
def mock_calculate_voltages_for_all_transmitters(monkeypatch):
    def set_data(self: SolverForwardP1000, t, *args, **kwargs):
        self.t = t
        num_electrodes = len(self.params.sensor.c_receive_multiplexer_off)

        self.voltage_knode_for_all_transmitters = np.arange(
            num_electrodes * num_electrodes * len(t)
        ).reshape([num_electrodes, num_electrodes, len(t)])

        # Symmetrise the arrays
        self.voltage_knode_for_all_transmitters = 0.5 * (
            self.voltage_knode_for_all_transmitters
            + np.transpose(self.voltage_knode_for_all_transmitters, (1, 0, 2))
        )

        self.voltage_tnode_for_all_transmitters = np.arange(
            num_electrodes * num_electrodes * len(t)
        ).reshape([num_electrodes, num_electrodes, len(t)])

    monkeypatch.setattr(
        "forwardSolver.scripts.solver_forward_P1000.SolverForwardP1000.calculate_voltages_for_all_transmitters",
        set_data,
    )


# TODO: re-add this test when a more efficient alternative is found
@pytest.mark.skip(reason="exceeds bitbucket memory limit")
def test_export_to_devicedata(mock_calculate_voltages_for_all_transmitters):
    params_9 = ForwardSolverParams(**params_9_dict)
    solver_forward = SolverForwardP1000(
        params_9,
        is_cap_calculated=False,
        is_voltage_mat_calculated=True,
        use_cache_input=False,
        use_cache_output=False,
    )

    input_generator = InputGeneratorP1000Pulse(params_9)
    t, vtransmit = input_generator.simulate()

    data = solver_forward.export_voltages_for_all_transmitters_to_devicedata(
        t, vtransmit
    )
    for i in range(1, 16):
        for j in range(1, 16):
            __signal = data.signal(i, j)
            np.testing.assert_array_equal(__signal.times, t * MICROSECONDS_TO_SECONDS)
            np.testing.assert_array_equal(__signal.vsources, vtransmit)
            np.testing.assert_array_equal(
                __signal.knodes,
                solver_forward.voltage_knode_for_all_transmitters[i - 1][j - 1],
            )
            np.testing.assert_array_equal(
                __signal.tnodes,
                solver_forward.voltage_tnode_for_all_transmitters[i - 1][j - 1],
            )


close_logger(logger)
