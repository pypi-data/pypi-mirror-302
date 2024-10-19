import numpy as np

from forwardSolver.scripts.utils.device_data.device_data import DeviceData
from forwardSolver.scripts.utils.utils_voltage_fitting import (
    calculate_l2_error_in_voltages,
    calculate_l2_norm_of_voltage,
)


def create_mock_device_data(
    num_electrodes: int = 2,
    time_start: float = 0,
    time_end: float = 20e-6,
    num_time_steps: int = 10,
    voltage_amplitude: float = 1,
    voltage_bias: float = 0,
    num_sine_wave_cycles: float = 1,
):
    device_data_mock = DeviceData()
    times = np.linspace(time_start, time_end, num_time_steps)
    tnode_voltages = (
        voltage_amplitude * np.sin(2 * np.pi * num_sine_wave_cycles * times / times[-1])
        + voltage_bias
    )
    device_data_mock.times = np.tile(times, num_electrodes * num_electrodes).reshape(
        num_electrodes, num_electrodes, num_time_steps
    )
    device_data_mock.tnode_voltages = np.tile(
        tnode_voltages, num_electrodes * num_electrodes
    ).reshape(num_electrodes, num_electrodes, num_time_steps)
    device_data_mock.knode_voltages = device_data_mock.tnode_voltages
    return device_data_mock


def test_calculate_l2_norm_of_voltage():
    voltage_bias = 10.7
    mock_device_data = create_mock_device_data(
        voltage_amplitude=0, voltage_bias=voltage_bias
    )
    norm_calculated = calculate_l2_norm_of_voltage(mock_device_data)
    np.testing.assert_allclose(voltage_bias, norm_calculated)


def test_calculate_l2_error_in_voltages():
    voltage_bias_1 = 12.8
    voltage_bias_2 = 25.3
    error_expected = np.abs(voltage_bias_2 - voltage_bias_1)
    mock_device_data_1 = create_mock_device_data(
        voltage_amplitude=0, voltage_bias=voltage_bias_1
    )
    mock_device_data_2 = create_mock_device_data(
        voltage_amplitude=0, voltage_bias=voltage_bias_2
    )

    error_calculated = calculate_l2_error_in_voltages(
        mock_device_data_1, mock_device_data_2
    )
    print(f"{error_calculated = }")

    np.testing.assert_allclose(error_expected, error_calculated)
