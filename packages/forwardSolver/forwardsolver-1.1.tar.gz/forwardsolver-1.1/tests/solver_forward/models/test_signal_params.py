import pytest

from forwardSolver.scripts.params.signal_params import SignalParams
from forwardSolver.scripts.utils.dict import check_all_keys_none


def test_signal_params_initialise_empty():
    # Initialise without args should all be none
    signal_params = SignalParams(**{})
    assert check_all_keys_none(signal_params.as_dict())

    # Initialise with empty dict should all be none
    signal_params = SignalParams()
    assert check_all_keys_none(signal_params.as_dict())


def test_signal_params_initialise_key():
    # Should raise TypeError when an extra key is added to dict but not dataclass
    with pytest.raises(TypeError):
        SignalParams(**{"donkey123": 123})


def test_signal_params_equality():
    # test equality operator and as_dict() function
    signal_params1 = SignalParams(t_rise=1, t_dwell=2)
    signal_params2 = SignalParams(**signal_params1.as_dict())
    assert signal_params1 == signal_params2

    signal_params1.t_dwell = 3
    assert signal_params1 != signal_params2
