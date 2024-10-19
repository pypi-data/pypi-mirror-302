import numpy as np

from forwardSolver.scripts.params.forward_solver_params import ForwardSolverParams
from forwardSolver.scripts.utils.cache import find_cached
from forwardSolver.scripts.utils.hash import hash_dictionary
from forwardSolver.tests.fixtures.forward_solver import VOLTAGES_AND_CHARGES_004


def test_cache_works():
    """
    conftest has run the forward solver with params_P1000_004
    Make sure that the cached file exists.
    """
    params = ForwardSolverParams.factory("P1000-004")
    params.sensor.noise_power_pulldown_on_receive = 0.0

    cached_data = find_cached(hash_dictionary(params.as_dict()))

    assert cached_data is not None

    np.testing.assert_equal(cached_data.V, VOLTAGES_AND_CHARGES_004[0])
