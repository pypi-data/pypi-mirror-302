import copy

import pytest

from forwardSolver.scripts.params.forward_solver_params import ForwardSolverParams
from forwardSolver.scripts.solver_forward_P1000 import (
    SolverForwardP1000,
    SolverForwardP1000_00X,
)
from forwardSolver.scripts.utils.input_generator_P1000_pulse import (
    InputGeneratorP1000Pulse,
)


def simulation_do_nothing(*args, **kwargs):
    """
    This function mocks setup_solver_environment so should always return the same sized result.
    """
    return (None,) * 24


def create_p1000_voltage_data(params: ForwardSolverParams):
    input_generator = InputGeneratorP1000Pulse(params)
    t, V_transmit = input_generator.simulate()

    solver_forward_true_point = SolverForwardP1000(
        params, is_cap_calculated=False, use_cache_input=True, use_cache_output=True
    )
    voltages_and_charges = solver_forward_true_point.simulate(t, V_transmit)
    return voltages_and_charges


def create_p1000_00x_voltage_data(params: ForwardSolverParams):
    input_generator = InputGeneratorP1000Pulse(params)
    t, V_transmit = input_generator.simulate()

    solver_forward_true_point = SolverForwardP1000_00X(params)
    voltages_and_charges = solver_forward_true_point.simulate(t, V_transmit)
    return voltages_and_charges


params_X_original = ForwardSolverParams.factory("P1000-00X")
params_1_original = ForwardSolverParams.factory("P1000-001")
params_4_original = ForwardSolverParams.factory("P1000-004")
params_6_original = ForwardSolverParams.factory("P1000-006")
params_9_original = ForwardSolverParams.factory("P1000-009")

# Make a complete copy of parameters and remove the noise.
params_X = copy.deepcopy(params_X_original)
params_X.sensor.noise_power_pulldown_on_receive = 0.0
params_1 = copy.deepcopy(params_1_original)
params_1.sensor.noise_power_pulldown_on_receive = 0.0
params_4 = copy.deepcopy(params_4_original)
params_4.sensor.noise_power_pulldown_on_receive = 0.0
params_6 = copy.deepcopy(params_6_original)
params_6.sensor.noise_power_pulldown_on_receive = 0.0
params_9 = copy.deepcopy(params_9_original)
params_9.sensor.noise_power_pulldown_on_receive = 0.0


VOLTAGES_AND_CHARGES_004 = create_p1000_voltage_data(params_4)
VOLTAGES_AND_CHARGES_006 = create_p1000_voltage_data(params_6)
VOLTAGES_AND_CHARGES_009 = create_p1000_voltage_data(params_9)
VOLTAGES_AND_CHARGES_00X = create_p1000_00x_voltage_data(params_X)


@pytest.fixture
def mock_simulation_p1000_00x(monkeypatch):
    """SolverForwardP1000_00X.simulate() mocked to return cached results.
    setup_solver_environment prevented from running.
    """

    def use_cached_simulate(*args, **kwargs):
        return VOLTAGES_AND_CHARGES_00X

    monkeypatch.setattr(
        "forwardSolver.scripts.solver_forward_P1000.setup_solver_environment",
        simulation_do_nothing,
    )
    monkeypatch.setattr(
        "forwardSolver.scripts.solver_forward_P1000.SolverForwardP1000_00X.simulate",
        use_cached_simulate,
    )


@pytest.fixture
def mock_simulation_p1000_004(monkeypatch):
    """SolverForwardP1000.simulate() mocked to return cached results.
    setup_solver_environment prevented from running.
    """

    def use_cached_simulate(*args, **kwargs):
        return VOLTAGES_AND_CHARGES_004

    monkeypatch.setattr(
        "forwardSolver.scripts.solver_forward_P1000.setup_solver_environment",
        simulation_do_nothing,
    )
    monkeypatch.setattr(
        "forwardSolver.scripts.solver_forward_P1000.SolverForwardP1000.simulate",
        use_cached_simulate,
    )


@pytest.fixture
def mock_simulation_p1000_006(monkeypatch):
    """SolverForwardP1000.simulate() mocked to return cached results.
    setup_solver_environment prevented from running.
    """

    def use_cached_simulate(*args, **kwargs):
        return VOLTAGES_AND_CHARGES_006

    monkeypatch.setattr(
        "forwardSolver.scripts.solver_forward_P1000.setup_solver_environment",
        simulation_do_nothing,
    )
    monkeypatch.setattr(
        "forwardSolver.scripts.solver_forward_P1000.SolverForwardP1000.simulate",
        use_cached_simulate,
    )


@pytest.fixture
def mock_simulation_p1000_009(monkeypatch):
    """SolverForwardP1000.simulate() mocked to return cached results.
    setup_solver_environment prevented from running.
    """

    def use_cached_simulate(*args, **kwargs):
        return VOLTAGES_AND_CHARGES_009

    monkeypatch.setattr(
        "forwardSolver.scripts.solver_forward_P1000.setup_solver_environment",
        simulation_do_nothing,
    )
    monkeypatch.setattr(
        "forwardSolver.scripts.solver_forward_P1000.SolverForwardP1000.simulate",
        use_cached_simulate,
    )
