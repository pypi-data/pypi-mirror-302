from copy import deepcopy
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from forwardSolver.scripts.utils.device_data.models.noise_data import NoiseData
from forwardSolver.scripts.utils.device_data.utils_device_data import (
    is_valid_gain_calibration,
    is_valid_gain_electrode_calibration,
    is_valid_gain_span_calibration,
    mask_poor_repeats,
    mask_unusable_capacitance_by_noise,
    mask_unusable_capacitances_by_span,
    read_gain_settings,
)


def test_mask_poor_repeats_stores_good_runs():
    """
    Test that good repeats are stored correctly
    """
    np.random.seed(12345)

    noise_data = []
    for i in range(10):
        noise_data.append(
            NoiseData(
                transmit=np.random.randint(1000),
                receive=np.random.randint(1000),
                rms_noise=None,
                snr=None,
                poor_repeats=None,
                good_repeats=np.random.randint(1000, size=5),
            )
        )

    dict_good = mask_poor_repeats(noise_data)

    for data in noise_data:
        assert np.all(
            dict_good[f"T{data.transmit}R{data.receive}"] == data.good_repeats
        )


def test_mask_poor_repeats_empty_when_list_empty():
    """
    Tests that the mask poor repeats dictionary is empty when input list is empty
    """
    assert mask_poor_repeats([]) == {}


@pytest.mark.skip(reason="test not implmemented")
def test_join_bad_runs():
    raise NotImplementedError


def test_mask_unusable_capacitance_by_noise():
    """
    Check all capacitances are masked without noise data.
    """
    np.random.seed(12345)

    capcitances = np.random.rand(5, 5)
    noise_data = []
    for i in range(5):
        for j in range(5):
            if i == 3 and j == 2:
                good_repeats = []
            else:
                good_repeats = [1, 2, 3]

            noise_data.append(
                NoiseData(
                    transmit=i + 1,
                    receive=j + 1,
                    rms_noise=None,
                    snr=None,
                    poor_repeats=None,
                    good_repeats=good_repeats,
                )
            )

    mask_cap = mask_unusable_capacitance_by_noise(
        noise=noise_data, capacitances=capcitances
    )

    for i in range(5):
        for j in range(5):
            print("TESTING", i, j, mask_cap[i, j], capcitances[i, j])
            if i == 3 and j == 2:
                assert np.isnan(mask_cap[i, j])
            else:
                assert capcitances[i, j] == mask_cap[i, j]


def test_mask_unusable_capacitance_by_noise_empty_list():
    """
    Check all capacitances are masked without noise data.
    """
    np.random.seed(12345)

    capcitances = np.random.rand(5, 5)
    mask_cap = mask_unusable_capacitance_by_noise(noise=[], capacitances=capcitances)

    assert np.isnan(mask_cap).all()


def test_mask_unusable_capacitances_by_span():

    np.random.seed(12345)

    capcitances = np.random.rand(5, 5)
    cap_0 = mask_unusable_capacitances_by_span(max_span=0, capacitances=capcitances)

    test_cap_0 = np.ones((5, 5)) * np.nan
    test_cap_0[np.diag_indices_from(test_cap_0)] = np.diag(capcitances, k=0)
    np.testing.assert_equal(test_cap_0, cap_0)


@pytest.mark.skip(reason="function has no return type and test not implmemented")
def test_check_transmit_time_spread():
    raise NotImplementedError


@pytest.mark.skip(reason="function has no return type and test not implmemented")
def test_check_voltage_dropoff():
    raise NotImplementedError


# Sample data for mocking the JSON file content
MOCKED_JSON_DATA = {
    "SH03": {
        "dac_codes_per_span": [
            "100",
            "111",
            "111",
            "001",
            "001",
            "001",
            "001",
            "001",
            "001",
            "001",
            "001",
            "001",
            "001",
            "001",
            "001",
        ],
        "settings": {
            "001": {"tnode": 1.0, "knode": 1.1},
            "111": {"tnode": 1.2, "knode": 1.3},
            "100": {"tnode": 1.4, "knode": 1.5},
        },
        "calibration": "span",
    }
}


@pytest.fixture
def mock_json_load():
    with patch("json.load", return_value=MOCKED_JSON_DATA):
        yield


def test_valid_device_and_settings(mock_json_load):
    # Test a valid device with valid settings
    device = "SH03"
    settings_per_span = ["001", "111", "100"]
    expected = np.array(
        [
            [1.0, 1.2, 1.4],  # tnode values for settings
            [1.1, 1.3, 1.5],  # knode values for settings
        ]
    )
    result = read_gain_settings(device, settings_per_span)
    np.testing.assert_array_equal(result, expected)


def test_uncalibrated_device(mock_json_load):
    # Test with an uncalibrated device
    device = "UNKNOWN_DEVICE"
    with pytest.raises(ValueError) as excinfo:
        read_gain_settings(device)
    assert "Uncalibrated device" in str(excinfo.value)


@patch(
    "forwardSolver.scripts.utils.device_data.utils_device_data.is_valid_gain_span_calibration"
)
@patch(
    "forwardSolver.scripts.utils.device_data.utils_device_data.is_valid_gain_electrode_calibration"
)
def test_is_valid_gain_calibration(
    mock_is_valid_gain_electrode_calibration, mock_is_valid_gain_span_calibration
):
    calibration = MagicMock()

    for b1 in [True, False]:
        for b2 in [True, False]:
            mock_is_valid_gain_electrode_calibration.reset_mock()
            mock_is_valid_gain_span_calibration.reset_mock()

            mock_is_valid_gain_electrode_calibration.return_value = b1
            mock_is_valid_gain_span_calibration.return_value = b2
            assert is_valid_gain_calibration(calibration) == (b1 or b2)
            # now lets assume lazy evaluation
            # but we can't be sure which one is called first, so we can't use assert_called_once_with
            # lets assume either or both of the functions are called
            try:
                mock_is_valid_gain_span_calibration.assert_called_once_with(calibration)
                break
            except AssertionError:
                mock_is_valid_gain_electrode_calibration.assert_called_once_with(
                    calibration
                )


valid_span_calibration = {
    "calibration": "span",
    "date": "2024-02-23",
    "settings": {
        "001": {"knode": 1.0, "tnode": 2.0},
        "100": {"knode": 3.0, "tnode": 4.0},
        "111": {"knode": 5.0, "tnode": 6.0},
    },
}
valid_electrode_calibration = {
    "calibration": "electrode",
    "date": "2024-02-23",
    "settings": {
        "001": {"knode": [1.0] * 15, "tnode": [2.0] * 15},
        "100": {"knode": [3.0] * 15, "tnode": [4.0] * 15},
        "111": {"knode": [5.0] * 15, "tnode": [6.0] * 15},
    },
}
invalid_calibration = {
    "calibration": "invalid",
    "date": "2024-02-23",
    "settings": {
        "001": {"knode": "1.0", "tnode": 2.0},
        "100": {"knode": 3.0, "tnode": 4.0},
        "111": {"knode": 5.0, "tnode": 6.0},
    },
}


def test_is_valid_gain_span_calibration():
    assert is_valid_gain_span_calibration(valid_span_calibration)
    assert not is_valid_gain_span_calibration(valid_electrode_calibration)
    assert not is_valid_gain_span_calibration(invalid_calibration)

    for key in valid_span_calibration["settings"]:
        invalid_copy = deepcopy(valid_span_calibration)
        del invalid_copy["settings"][key]
        assert not is_valid_gain_span_calibration(invalid_copy)

    invalid_copy = deepcopy(valid_span_calibration)
    del invalid_copy["settings"]["001"]["knode"]
    assert not is_valid_gain_span_calibration(invalid_copy)

    # lastly lets change the type of knode
    invalid_copy = deepcopy(valid_span_calibration)
    invalid_copy["settings"]["001"]["knode"] = [1.0] * 15
    assert not is_valid_gain_span_calibration(invalid_copy)


def test_is_valid_gain_electrode_calibration():
    assert not is_valid_gain_electrode_calibration(valid_span_calibration)
    assert is_valid_gain_electrode_calibration(valid_electrode_calibration)
    assert not is_valid_gain_electrode_calibration(invalid_calibration)

    for key in valid_electrode_calibration["settings"]:
        invalid_copy = deepcopy(valid_electrode_calibration)
        del invalid_copy["settings"][key]
        assert not is_valid_gain_electrode_calibration(invalid_copy)

    invalid_copy = deepcopy(valid_electrode_calibration)
    del invalid_copy["settings"]["001"]["knode"]
    assert not is_valid_gain_electrode_calibration(invalid_copy)

    # lastly lets change the type of knode
    invalid_copy = deepcopy(valid_electrode_calibration)
    invalid_copy["settings"]["001"]["knode"] = 1.0
    assert not is_valid_gain_electrode_calibration(invalid_copy)
