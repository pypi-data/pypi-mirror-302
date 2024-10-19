from dataclasses import asdict

import numpy as np
import pytest
from PySpice.Spice.Netlist import Circuit

from forwardSolver.scripts.params.forward_solver_params import ForwardSolverParams
from forwardSolver.scripts.solver_forward_P1000 import SolverForwardP1000
from forwardSolver.scripts.utils.constants import (
    MEGA_OHM_TO_OHM,
    MICROSECONDS_TO_SECONDS,
    PICO_FARAD_TO_FARAD,
)
from forwardSolver.scripts.utils.device_data.device_data import DeviceData
from forwardSolver.scripts.utils.spice_forward_voltage import (
    CircuitParameters,
    SpiceSolver,
    WaveformParameters,
    pwl_source_from_device_data,
)

LARGE_RESISTANCE_OHM = 1e20


@pytest.fixture(scope="module")
def params_009() -> ForwardSolverParams:
    params = ForwardSolverParams.factory("P1000-009")
    params.simulation.t_end = 40  # simulation end time set to 40 microseconds
    return params


@pytest.fixture(scope="module")
def forward_solver_object_009(params_009: ForwardSolverParams) -> SolverForwardP1000:
    return SolverForwardP1000(
        params_009, is_cap_calculated=True, is_voltage_mat_calculated=False
    )


@pytest.fixture(scope="module")
def spice_solver_circuit_parameters(
    params_009: ForwardSolverParams,
) -> CircuitParameters:
    circuit_parameters = CircuitParameters()
    circuit_parameters.resistance_tnode_to_ground = LARGE_RESISTANCE_OHM * np.ones(
        (len(params_009.sensor.r_series))
    )

    circuit_parameters.capacitance_tnode_to_ground = (
        params_009.sensor.c_transmit_multiplexer_off * PICO_FARAD_TO_FARAD
    )
    circuit_parameters.resistance_tnode_to_knode = (
        params_009.sensor.r_series * MEGA_OHM_TO_OHM
    )
    circuit_parameters.resistance_knode_to_ground = (
        params_009.sensor.r_pulldown_on_receive * MEGA_OHM_TO_OHM
    )
    circuit_parameters.capacitance_knode_to_ground = (
        params_009.sensor.c_receive_multiplexer_off * PICO_FARAD_TO_FARAD
    )
    circuit_parameters.resistance_at_source = 10e3
    circuit_parameters.capacitance_source_to_ground = 1e-15
    return circuit_parameters


@pytest.fixture(scope="module")
def spice_solver_waveform_parameters(
    params_009: ForwardSolverParams,
) -> WaveformParameters:
    waveform_parameters = WaveformParameters()
    waveform_parameters.time_start = 0.0
    waveform_parameters.time_delay = 0.0
    waveform_parameters.time_rise = params_009.signal.t_rise * MICROSECONDS_TO_SECONDS
    waveform_parameters.time_dwell = params_009.signal.t_dwell * MICROSECONDS_TO_SECONDS
    waveform_parameters.time_fall = params_009.signal.t_fall * MICROSECONDS_TO_SECONDS
    waveform_parameters.time_end = params_009.simulation.t_end * MICROSECONDS_TO_SECONDS
    waveform_parameters.time_step = (
        params_009.simulation.t_step * MICROSECONDS_TO_SECONDS
    )
    waveform_parameters.voltage_max = params_009.signal.v_max
    waveform_parameters.voltage_start = 0.0
    waveform_parameters.voltage_end = 0.0
    waveform_parameters.voltage_max = params_009.signal.v_max

    return waveform_parameters


@pytest.fixture(scope="function")
def spice_solver_object(
    params_009: ForwardSolverParams,
    forward_solver_object_009: SolverForwardP1000,
    spice_solver_circuit_parameters: CircuitParameters,
    spice_solver_waveform_parameters: WaveformParameters,
) -> SpiceSolver:
    spice_solver = SpiceSolver(
        params_forward_solver=params_009,
        capacitance_matrix=forward_solver_object_009.C_true,
        params_circuit=spice_solver_circuit_parameters,
        params_waveform=spice_solver_waveform_parameters,
        resistance_at_source=None,
        capacitance_source_to_ground=None,
        voltage_start=None,
        voltage_end=None,
    )

    return spice_solver


@pytest.fixture(scope="function")
def spice_solver_circuit_rc_network_009(
    forward_solver_object_009: SolverForwardP1000,
    spice_solver_circuit_parameters: SpiceSolver,
) -> Circuit:
    num_electrodes = forward_solver_object_009.C_true.shape[0]
    circuit = Circuit("spice_circuit")
    for iloop_electrode in range(1, num_electrodes + 1):
        # Resistance from T node to ground
        circuit.R(
            f"_TG{iloop_electrode}",
            f"T{iloop_electrode}",
            circuit.gnd,
            spice_solver_circuit_parameters.resistance_tnode_to_ground[
                iloop_electrode - 1
            ],
        )

        # Capacitance from T node to ground
        circuit.C(
            f"_TG{iloop_electrode}",
            f"T{iloop_electrode}",
            circuit.gnd,
            spice_solver_circuit_parameters.capacitance_tnode_to_ground[
                iloop_electrode - 1
            ],
        )

        # Resistance from T node to K node
        circuit.R(
            f"_TK{iloop_electrode}",
            f"T{iloop_electrode}",
            f"K{iloop_electrode}",
            spice_solver_circuit_parameters.resistance_tnode_to_knode[
                iloop_electrode - 1
            ],
        )

        # Resistance from K node to ground
        circuit.R(
            f"_KG{iloop_electrode}",
            f"K{iloop_electrode}",
            circuit.gnd,
            spice_solver_circuit_parameters.resistance_knode_to_ground[
                iloop_electrode - 1
            ],
        )

        # Capacitance from K node to ground
        circuit.C(
            f"_KG{iloop_electrode}",
            f"K{iloop_electrode}",
            circuit.gnd,
            spice_solver_circuit_parameters.capacitance_knode_to_ground[
                iloop_electrode - 1
            ],
        )

    for iloop_electrode in range(1, num_electrodes + 1):
        for jloop_electrode in range(iloop_electrode + 1, num_electrodes + 1):
            circuit.C(
                f"_{iloop_electrode}_{jloop_electrode}",
                f"K{iloop_electrode}",
                f"K{jloop_electrode}",
                PICO_FARAD_TO_FARAD
                * forward_solver_object_009.C_true[
                    iloop_electrode - 1, jloop_electrode - 1
                ],
            )
    return circuit


def test_pwl_source_from_device_data():
    # create a mock device data object with coarse time steps
    num_electrodes = 2
    time_start = 0
    time_end = 20e-6
    num_time_steps = 2
    device_data_mock = DeviceData()
    times = np.linspace(time_start, time_end, num_time_steps)
    tnode_voltages = np.sin(times)
    device_data_mock.times = np.tile(times, num_electrodes * num_electrodes).reshape(
        num_electrodes, num_electrodes, num_time_steps
    )
    device_data_mock.tnode_voltages = np.tile(
        tnode_voltages, num_electrodes * num_electrodes
    ).reshape(num_electrodes, num_electrodes, num_time_steps)
    device_data_mock.knode_voltages = device_data_mock.tnode_voltages

    pwl_source_list_entry = [
        (times[0], tnode_voltages[0]),
        (times[1], tnode_voltages[1]),
    ]
    pwl_source_list_expected = [pwl_source_list_entry, pwl_source_list_entry]

    pwl_source_list = pwl_source_from_device_data(device_data_mock)

    assert pwl_source_list_expected == pwl_source_list


def test_spice_solver_init(
    params_009: ForwardSolverParams,
    forward_solver_object_009: SolverForwardP1000,
    spice_solver_circuit_parameters: CircuitParameters,
    spice_solver_waveform_parameters: WaveformParameters,
):
    """Test that the initialization of the spice solver with explicitly provided
    parameters works fine.  The initialization that involves calculations
    from forward solver parameters are tested separately.
    """

    spice_solver = SpiceSolver(
        params_forward_solver=params_009,
        capacitance_matrix=forward_solver_object_009.C_true,
        params_circuit=spice_solver_circuit_parameters,
        params_waveform=spice_solver_waveform_parameters,
        resistance_at_source=None,
        capacitance_source_to_ground=None,
        voltage_start=None,
        voltage_end=None,
    )
    np.testing.assert_equal(
        asdict(spice_solver.params_forward_solver), asdict(params_009)
    )
    np.testing.assert_equal(
        forward_solver_object_009.C_true * PICO_FARAD_TO_FARAD,
        spice_solver.capacitance_matrix,
    )
    np.testing.assert_equal(
        spice_solver.num_electrodes, forward_solver_object_009.C_true.shape[0]
    )
    np.testing.assert_equal(
        asdict(spice_solver.params_circuit), asdict(spice_solver_circuit_parameters)
    )
    np.testing.assert_equal(
        asdict(spice_solver.params_waveform), asdict(spice_solver_waveform_parameters)
    )


def test_spice_solver_calculate_capacitance(
    params_009: ForwardSolverParams,
    forward_solver_object_009: SolverForwardP1000,
    spice_solver_circuit_parameters: CircuitParameters,
    spice_solver_waveform_parameters: WaveformParameters,
):
    """This function tests whether the capacitance matrix calculation in the
    spice solver matches the forward solver capacitance matrix."""

    spice_solver = SpiceSolver(
        params_forward_solver=params_009,
        capacitance_matrix=None,
        params_circuit=spice_solver_circuit_parameters,
        params_waveform=spice_solver_waveform_parameters,
        resistance_at_source=None,
        capacitance_source_to_ground=None,
        voltage_start=None,
        voltage_end=None,
    )
    np.testing.assert_equal(
        forward_solver_object_009.C_true * PICO_FARAD_TO_FARAD,
        spice_solver.capacitance_matrix,
    )


def test_spice_solver_get_circuit_parameters(
    params_009: ForwardSolverParams,
    forward_solver_object_009: SolverForwardP1000,
    spice_solver_circuit_parameters: CircuitParameters,
    spice_solver_waveform_parameters: WaveformParameters,
):
    """Tests whether the circuit parameters initialized using the forward solver
    parameters are as expected."""

    spice_solver = SpiceSolver(
        params_forward_solver=params_009,
        capacitance_matrix=forward_solver_object_009.C_true,
        params_circuit=None,
        params_waveform=spice_solver_waveform_parameters,
        resistance_at_source=spice_solver_circuit_parameters.resistance_at_source,
        capacitance_source_to_ground=spice_solver_circuit_parameters.capacitance_source_to_ground,
        voltage_start=None,
        voltage_end=None,
    )

    np.testing.assert_equal(
        asdict(spice_solver_circuit_parameters), asdict(spice_solver.params_circuit)
    )


def test_spice_solver_get_waveform_parameters(
    params_009: ForwardSolverParams,
    forward_solver_object_009: SolverForwardP1000,
    spice_solver_circuit_parameters: CircuitParameters,
    spice_solver_waveform_parameters: WaveformParameters,
):
    """Tests whether the waveform parameters initialized using the forward solver
    parameters are as expected."""
    spice_solver = SpiceSolver(
        params_forward_solver=params_009,
        capacitance_matrix=forward_solver_object_009.C_true,
        params_circuit=spice_solver_circuit_parameters,
        params_waveform=None,
        resistance_at_source=None,
        capacitance_source_to_ground=None,
        voltage_start=spice_solver_waveform_parameters.voltage_start,
        voltage_end=spice_solver_waveform_parameters.voltage_end,
    )

    np.testing.assert_equal(
        asdict(spice_solver_waveform_parameters), asdict(spice_solver.params_waveform)
    )


def test_spice_solver_create_source_pwl_points_dict(
    spice_solver_object: SpiceSolver,
    spice_solver_waveform_parameters: WaveformParameters,
):
    """Verify the list of tuples that define the piecewise constant voltage source."""
    source_pwl_points_dict_expected = {
        "start_tuple": (
            spice_solver_waveform_parameters.time_start,
            spice_solver_waveform_parameters.voltage_start,
        ),
        "rise_tuple": (
            spice_solver_waveform_parameters.time_start
            + spice_solver_waveform_parameters.time_rise,
            spice_solver_waveform_parameters.voltage_max,
        ),
        "dwell_tuple": (
            spice_solver_waveform_parameters.time_start
            + spice_solver_waveform_parameters.time_rise
            + spice_solver_waveform_parameters.time_dwell,
            spice_solver_waveform_parameters.voltage_max,
        ),
        "fall_tuple": (
            spice_solver_waveform_parameters.time_start
            + spice_solver_waveform_parameters.time_rise
            + spice_solver_waveform_parameters.time_dwell
            + spice_solver_waveform_parameters.time_fall,
            spice_solver_waveform_parameters.voltage_end,
        ),
        "end_tuple": (
            spice_solver_waveform_parameters.time_end,
            spice_solver_waveform_parameters.voltage_end,
        ),
    }

    np.testing.assert_equal(
        source_pwl_points_dict_expected,
        spice_solver_object.create_source_pwl_points_dict(),
    )


def test_spice_solver_create_spice_rc_network(
    spice_solver_object: SpiceSolver,
    spice_solver_circuit_rc_network_009: CircuitParameters,
):
    """Verify the RC network netlist generated against the expected result."""
    assert str(spice_solver_object.create_spice_rc_network()) == str(
        spice_solver_circuit_rc_network_009
    )


def test_spice_solver_create_spice_netlist(
    spice_solver_circuit_parameters: ForwardSolverParams,
    spice_solver_object: SpiceSolver,
    spice_solver_circuit_rc_network_009: Circuit,
):
    """Verify the spice netlist generated for a source voltage applied at a
    particular electrode (set to source_node_index = 2) against the expected result."""

    circuit_expected = spice_solver_circuit_rc_network_009
    source_node_index = 2
    circuit_expected.PieceWiseLinearVoltageSource(
        f"_source_{source_node_index}",
        f"E{source_node_index}",
        circuit_expected.gnd,
        list(spice_solver_object.create_source_pwl_points_dict().values()),
    )
    circuit_expected.R(
        f"_source_{source_node_index}",
        f"E{source_node_index}",
        f"T{source_node_index}",
        spice_solver_circuit_parameters.resistance_at_source,
    )
    circuit_expected.C(
        f"_source_{source_node_index}",
        f"T{source_node_index}",
        circuit_expected.gnd,
        spice_solver_circuit_parameters.capacitance_source_to_ground,
    )

    circuit_created = spice_solver_object.create_spice_netlist(source_node_index=2)

    assert str(circuit_expected) == str(circuit_created)


def test_spice_solver_interpolate_spice_voltages(
    spice_solver_object: SpiceSolver,
):
    """Verify that the interpolated voltages for a simple time series is as expected."""
    num_electrodes = 2
    time_start = 0
    time_end = 2
    num_time_steps = 10

    time = np.array([0, 1.5, 2])
    tnode_voltage_1d = 2 * time
    knode_voltage_1d = 3 * time

    time_interpolated_expected = np.linspace(time_start, time_end, num_time_steps)
    tnode_voltage_1d_interpolated_expected = 2 * time_interpolated_expected
    knode_voltage_1d_interpolated_expected = 3 * time_interpolated_expected

    # Create 2d arrays of times and voltages
    tnode_voltage = np.tile(tnode_voltage_1d, (num_electrodes, 1))
    knode_voltage = np.tile(knode_voltage_1d, (num_electrodes, 1))

    # Create the expected interpolation values
    tnode_voltage_interpolated_expected = np.tile(
        tnode_voltage_1d_interpolated_expected, (num_electrodes, 1)
    )
    knode_voltage_interpolated_expected = np.tile(
        knode_voltage_1d_interpolated_expected, (num_electrodes, 1)
    )

    # Adjust the spice solver parameters
    spice_solver_object.params_waveform.time_start = time[0]
    spice_solver_object.params_waveform.time_end = time[-1]
    spice_solver_object.params_waveform.time_step = (time[-1] - time[0]) / (
        num_time_steps - 1
    )
    spice_solver_object.num_electrodes = num_electrodes

    # Obtain the result from spice solver interpolation function
    (
        time_interpolated,
        tnode_voltage_interpolated,
        knode_voltage_interpolated,
    ) = spice_solver_object.interpolate_spice_voltages(
        time, tnode_voltage, knode_voltage
    )

    np.testing.assert_equal(time_interpolated, time_interpolated_expected)
    np.testing.assert_equal(
        tnode_voltage_interpolated, tnode_voltage_interpolated_expected
    )
    np.testing.assert_equal(
        knode_voltage_interpolated, knode_voltage_interpolated_expected
    )


def test_spice_solver_calculate_spice_voltages(
    spice_solver_object: SpiceSolver,
):
    """Calculate the spice voltages of the circuit.
    The electric circuit is simplified so that all the capacitances are set to a
    very small value, and therefore open circuited. This will isolate the circuits
    associated with each electrode into disconnected units of resistive voltage dividers
    and the result voltages are easy to calculate independently.

    The idea is to remove all components except the series resistor between
    T node and K node and the pull down resistor from K node to ground.
    All the unwanted series resistances have to be short circuited (set to small value)
    and unwanted parallel resistances have to be open circuited (set to large value).
    All the unwanted capacitances are set to zero (small value).
    Then the output voltage at the K node will be approximately given by
    V_K = V_s * (R_{KG})/ (R_{KG}+R_{TK})."""

    # Multiplication factor to make a value approximately zero
    SMALL_NUMBER = 1e-30
    LARGE_NUMBER = 1e30
    resistance_value_t_k = 10e3  # value of the resistances from t node to k node
    resistance_value_k_g = 20e3  # value of the resistances from k node to ground
    # Gain of the resistance divider circuit
    gain_voltage_knode = resistance_value_k_g / (
        resistance_value_k_g + resistance_value_t_k
    )
    source_node_index = 4  # the electrode at which the voltage source is applied

    # Set a source voltage maximum value to non zero level
    spice_solver_object.params_waveform.voltage_max = 2.5

    # Remove all extra components to simplify the circuit
    spice_solver_object.params_circuit.resistance_at_source = (
        SMALL_NUMBER * spice_solver_object.params_circuit.resistance_at_source
    )
    spice_solver_object.params_circuit.capacitance_source_to_ground = (
        SMALL_NUMBER * spice_solver_object.params_circuit.capacitance_source_to_ground
    )
    spice_solver_object.params_circuit.capacitance_tnode_to_ground = (
        SMALL_NUMBER * spice_solver_object.params_circuit.capacitance_tnode_to_ground
    )
    spice_solver_object.params_circuit.resistance_tnode_to_ground = (
        LARGE_NUMBER * spice_solver_object.params_circuit.resistance_tnode_to_ground
    )
    spice_solver_object.params_circuit.capacitance_knode_to_ground = (
        SMALL_NUMBER * spice_solver_object.params_circuit.capacitance_knode_to_ground
    )
    spice_solver_object.capacitance_matrix = (
        SMALL_NUMBER * spice_solver_object.capacitance_matrix
    )

    spice_solver_object.params_circuit.resistance_tnode_to_knode = np.full_like(
        spice_solver_object.params_circuit.resistance_tnode_to_knode,
        resistance_value_t_k,
    )
    spice_solver_object.params_circuit.resistance_knode_to_ground = np.full_like(
        spice_solver_object.params_circuit.resistance_knode_to_ground,
        resistance_value_k_g,
    )

    time, tnode_voltage, knode_voltage = spice_solver_object.calculate_spice_voltages(
        source_node_index=source_node_index
    )

    # Check that the maximum voltage at tnode is close to the maximum source voltage
    np.testing.assert_allclose(
        np.max(tnode_voltage[source_node_index - 1]),
        spice_solver_object.params_waveform.voltage_max,
        rtol=1e-12,
    )
    # Check that the circuit acts like a resistive voltage divider
    np.testing.assert_allclose(
        gain_voltage_knode * tnode_voltage[source_node_index - 1],
        knode_voltage[source_node_index - 1],
        atol=1e-12,
    )

    # Check that all other voltages are close to zero
    np.testing.assert_allclose(
        tnode_voltage[: source_node_index - 1],
        np.full_like(tnode_voltage[: source_node_index - 1], SMALL_NUMBER),
        atol=1e-12,
    )
    np.testing.assert_allclose(
        knode_voltage[: source_node_index - 1],
        np.full_like(knode_voltage[: source_node_index - 1], SMALL_NUMBER),
        atol=1e-12,
    )
    np.testing.assert_allclose(
        tnode_voltage[source_node_index + 1 :],  # noqa E203
        np.full_like(tnode_voltage[source_node_index + 1 :], SMALL_NUMBER),  # noqa E203
        atol=1e-12,
    )
    np.testing.assert_allclose(
        knode_voltage[source_node_index + 1 :],  # noqa E203
        np.full_like(knode_voltage[source_node_index + 1 :], SMALL_NUMBER),  # noqa E203
        atol=1e-12,
    )


def test_spice_solver_create_spice_device_data(
    spice_solver_object: SpiceSolver,
):
    """Test for the consistency of device data voltages.
    When the inter electrodes capacitances are disconnected, and the circuit attached
    to each electrode is the same, then all the corresponding T node and K node voltages
    should be approximately equal."""

    SMALL_NUMBER = 1e-30
    num_electrodes = spice_solver_object.num_electrodes
    spice_solver_object.capacitance_matrix = np.full_like(
        spice_solver_object.capacitance_matrix, SMALL_NUMBER
    )
    device_data = spice_solver_object.create_spice_device_data()
    times = device_data.times
    tnode_voltages = device_data.tnode_voltages
    knode_voltages = device_data.knode_voltages

    # Check that the voltages are approximately the same at all spans
    for iloop_electrode in range(num_electrodes):
        for jloop_electrode in range(iloop_electrode, num_electrodes):
            np.testing.assert_allclose(
                times[iloop_electrode, jloop_electrode],
                times[0, jloop_electrode - iloop_electrode],
            )
            np.testing.assert_allclose(
                tnode_voltages[iloop_electrode, jloop_electrode],
                tnode_voltages[0, jloop_electrode - iloop_electrode],
                atol=1e-12,
                rtol=1e-6,
            )
            np.testing.assert_allclose(
                knode_voltages[iloop_electrode, jloop_electrode],
                knode_voltages[0, jloop_electrode - iloop_electrode],
                atol=1e-12,
                rtol=1e-6,
            )
