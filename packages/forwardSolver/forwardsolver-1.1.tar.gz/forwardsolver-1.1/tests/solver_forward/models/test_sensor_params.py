import pytest

from forwardSolver.scripts.params.sensor_params import SensorParams
from forwardSolver.scripts.utils.dict import check_all_keys_none


def test_sensor_params_initialise_empty():
    # Initialise without args should all be none
    sensor_params = SensorParams(**{})
    assert check_all_keys_none(sensor_params.as_dict())

    # Initialise with empty dict should all be none
    sensor_params = SensorParams()
    assert check_all_keys_none(sensor_params.as_dict())


def test_sensor_params_initialise_key():
    # Should raise TypeError when an extra key is added to dict but not dataclass
    with pytest.raises(TypeError):
        SensorParams(**{"donkey123": 123})


def test_sensor_params_equality():
    # test equality operator and as_dict() function
    sensor_params1 = SensorParams(
        num_transmitter=2, c_receive_multiplexer_off=[1, 2, 3]
    )
    sensor_params2 = SensorParams(**sensor_params1.as_dict())
    assert sensor_params1 == sensor_params2

    sensor_params1.c_receive_multiplexer_off = [1, 2, 3.1]
    assert sensor_params1 != sensor_params2
