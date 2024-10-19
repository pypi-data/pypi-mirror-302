import pytest

from forwardSolver.scripts.params.simulation_params import SimulationParams
from forwardSolver.scripts.utils.dict import check_all_keys_none


def test_sim_params_initialise_empty():
    # Initialise without args should all be none
    sim_params = SimulationParams(**{})
    assert check_all_keys_none(sim_params.as_dict())

    # Initialise with empty dict should all be none
    sim_params = SimulationParams()
    assert check_all_keys_none(sim_params.as_dict())


def test_sim_params_initialise_key():
    # Should raise TypeError when an extra key is added to dict but not dataclass
    with pytest.raises(TypeError):
        SimulationParams(**{"donkey123": 123})


def test_sim_params_equality():
    # test equality operator and as_dict() function
    sim_params1 = SimulationParams(t_step=1, t_end=2)
    sim_params2 = SimulationParams(**sim_params1.as_dict())
    assert sim_params1 == sim_params2

    sim_params1.t_step = 5
    assert sim_params1 != sim_params2
