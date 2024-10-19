import os
import re

import h5py
import numpy as np
import pytest

from forwardSolver.scripts.utils.device_data.signal import (
    Signal,
    SignalADC,
    SignalHDF,
    SignalSynthetic,
    utr_idx,
)


def test_utr_idx():
    """
    Testing upper triangular index method
    """
    # TEST 1: 3x3 Matrix
    a = np.array([[11, 12, 13], [21, 22, 23], [31, 32, 33]])

    a_utr = a[np.triu_indices(3)]

    # Check that the correct upper triangular indices are called
    for i in range(3):
        for j in range(i, 3):
            np.testing.assert_equal(a_utr[utr_idx(3, i + 1, j + 1)], a[i, j])

    # Check that the symmetric upper triangular indices are called
    for i in range(3):
        for j in range(i + 1):
            np.testing.assert_equal(a_utr[utr_idx(3, i + 1, j + 1)], a[j, i])

    # TEST 1: 5x5 Matrix
    b = np.array(
        [
            [11, 12, 13, 14, 15],
            [21, 22, 23, 24, 25],
            [31, 32, 33, 34, 35],
            [41, 42, 43, 44, 45],
            [51, 52, 53, 54, 55],
        ]
    )

    b_utr = b[np.triu_indices(5)]

    # Check that the correct upper triangular indices are called
    for i in range(5):
        for j in range(i, 5):
            np.testing.assert_equal(b_utr[utr_idx(5, i + 1, j + 1)], b[i, j])

    # Check that the symmetric upper triangular indices are called
    for i in range(5):
        for j in range(i + 1):
            np.testing.assert_equal(b_utr[utr_idx(5, i + 1, j + 1)], b[j, i])


@pytest.mark.usefixtures("hdf_file")
def test_Signal_read(hdf_file):
    """
    Testing that the correct concretised data type is created depending on the
    argument passed to Signal.read
    """
    hdf = h5py.File(hdf_file, "r")
    dataset: h5py.Dataset = hdf["PulseResponse/T1/R1"]
    signal = Signal.read(data=dataset)

    assert isinstance(signal, Signal)
    assert isinstance(signal, SignalHDF)

    with pytest.raises(TypeError):
        signal = Signal.read(["foo"])

    with pytest.raises(TypeError):
        signal = Signal.read(np.random.rand(1, 10))

    hdf.close()


@pytest.mark.usefixtures("hdf_file")
def test_Signal_averaging(hdf_file):
    np.random.seed(123)
    # Expected output
    dataset = np.random.rand(1, 5, 4, 1000)

    # Actual output
    hdf = h5py.File(hdf_file, "r")
    signal = Signal.read(data=hdf["PulseResponse/T1/R1"])

    # Test
    np.testing.assert_array_equal(signal.times, dataset.mean(axis=1)[0, 0, :])
    np.testing.assert_array_equal(signal.tnodes, dataset.mean(axis=1)[0, 1, :])
    np.testing.assert_array_equal(signal.knodes, dataset.mean(axis=1)[0, 2, :])

    hdf.close()


@pytest.mark.usefixtures("hdf_file")
def test_Signal_to_dict(hdf_file):
    np.random.seed(123)
    # Expected output
    dataset = np.random.rand(1, 5, 4, 1000)
    expected = dict(
        datatype="hdf",
        raw_times=dataset[0, :, 0, :],
        raw_tnodes=dataset[0, :, 1, :],
        raw_knodes=dataset[0, :, 2, :],
        raw_vsources=dataset[0, :, 3, :],
        nreps=5,
        good_repeats=None,
    )

    # Actual output
    hdf = h5py.File(hdf_file, "r")
    signal = Signal.read(data=hdf["PulseResponse/T1/R1"])

    # Test
    np.testing.assert_equal(signal.to_dict(), expected)

    hdf.close()

    # TODO: Add ADC example


@pytest.mark.usefixtures("hdf_file")
def test_Signal_from_dict(hdf_file):
    np.random.seed(123)
    # Input output
    dataset = np.random.rand(1, 5, 4, 1000)
    input = dict(
        datatype="hdf",
        raw_times=dataset[0, :, 0, :],
        raw_tnodes=dataset[0, :, 1, :],
        raw_knodes=dataset[0, :, 2, :],
        raw_vsources=dataset[0, :, 3, :],
        nreps=5,
        good_repeats=None,
    )
    # Actual output
    signal_from_dict = Signal.from_dict(input)

    # Expected output
    hdf = h5py.File(hdf_file, "r")
    signal = Signal.read(data=hdf["PulseResponse/T1/R1"])

    # Test
    np.testing.assert_equal(signal_from_dict, signal)

    hdf.close()

    # TODO: Add ADC, Synthetic data examples


@pytest.mark.usefixtures("hdf_file")
def test_Signal_json_IO(hdf_file, tmp_path_factory):
    """
    Test the input/output to JSON file by creating a json file in the testing directory,
    loading it and comparing the two
    """
    # Instantiate dataset
    hdf = h5py.File(hdf_file, "r")
    dataset: h5py.Dataset = hdf["PulseResponse/T1/R1"]

    # Initialise the signal from HDF
    signal = Signal.read(dataset)

    # Output to JSON
    jsonpath = tmp_path_factory.mktemp("data") / "signal.json"

    if os.path.isfile(jsonpath):
        os.remove(jsonpath)

    signal.to_json(jsonpath)

    # Assert that the file was created
    np.testing.assert_(os.path.isfile(jsonpath))

    # Read json file
    signal_read = Signal.from_json(jsonfile=jsonpath)

    np.testing.assert_array_equal(signal.knodes, signal_read.knodes)
    np.testing.assert_array_equal(signal.tnodes, signal_read.tnodes)
    np.testing.assert_array_equal(signal.times, signal_read.times)

    hdf.close()

    # TODO: Add ADC example


@pytest.mark.usefixtures("hdf_file")
def test_SignalHDF_read(hdf_file):
    """
    Test that an HDF dataset's timeseries is correctly read
    """
    # Instantiate dataset
    hdf = h5py.File(hdf_file, "r")
    dataset: h5py.Dataset = hdf["PulseResponse/T1/R1"]
    signal: SignalHDF = Signal.read(data=dataset)

    np.testing.assert_array_equal(signal.raw_times, dataset[0, :, 0, :])
    np.testing.assert_array_equal(signal.raw_tnodes, dataset[0, :, 1, :])
    np.testing.assert_array_equal(signal.raw_knodes, dataset[0, :, 2, :])
    np.testing.assert_equal(signal.nreps, 5)
    np.testing.assert_equal(signal.datatype, "hdf")

    hdf.close()


@pytest.mark.usefixtures("hdf_file")
def test_SignalHDF_json_IO(hdf_file, tmp_path_factory):
    """
    Test the input/output to JSON file by creating a json file in the testing directory,
    loading it and comparing the two
    """
    # Instantiate dataset
    hdf = h5py.File(hdf_file, "r")
    dataset: h5py.Dataset = hdf["PulseResponse/T1/R1"]

    # Initialise the signal from HDF
    signal: SignalHDF = Signal.read(dataset)

    # Output to JSON
    jsonpath = tmp_path_factory.mktemp("data") / "signal.json"

    if os.path.isfile(jsonpath):
        os.remove(jsonpath)

    signal.to_json(jsonpath)

    # Assert that the file was created
    np.testing.assert_(os.path.isfile(jsonpath))

    # Read json file
    signal_read: SignalHDF = Signal.from_json(jsonfile=jsonpath)

    np.testing.assert_array_equal(signal.raw_knodes, signal_read.raw_knodes)
    np.testing.assert_array_equal(signal.knodes, signal_read.knodes)
    np.testing.assert_array_equal(signal.raw_tnodes, signal_read.raw_tnodes)
    np.testing.assert_array_equal(signal.tnodes, signal_read.tnodes)
    np.testing.assert_array_equal(signal.raw_times, signal_read.raw_times)
    np.testing.assert_array_equal(signal.times, signal_read.times)

    hdf.close()


@pytest.mark.parametrize(
    "interval,  motor_on, array_t, array_k, gains",
    [
        (
            1,
            False,
            ([0, 1, 2], [6, 7, 8]),
            ([3, 4, 5], [9, 10, 11]),
            (1.0, 1.0),
        ),
        (3, False, ([0], [6]), ([3], [9]), (2.0, 2.0)),
        (1, True, ([6, 7, 8]), ([9, 10, 11]), (3.0, 3.0)),
        (1, True, ([6, 7, 8]), ([9, 10, 11]), (3.0, 1.0)),
    ],
)
def test_SignalADC_read_signals_with_gains(interval, motor_on, array_t, array_k, gains):
    # Check that, when gains are supplied to SignalADC.read,
    # the voltage array is read with correct gains applied

    np.random.seed(123)
    voltages = np.arange(12).reshape(2, 2, 3)
    outputs = SignalADC.read(
        data_array=voltages,
        interval=interval,
        pulse_duration=4,
        motor_on=motor_on,
        rotation_id=1,
        gains=gains,
        average_offset_to_zero=False,
    )
    np.testing.assert_equal(outputs.raw_tnodes, np.array(array_t) / gains[0])
    np.testing.assert_equal(outputs.raw_knodes, np.array(array_k) / gains[1])


@pytest.mark.parametrize(
    "motor_on, offset_window, error",
    [
        (False, (0,), dict(type=AssertionError, msg="not of correct length")),
        (False, ("a", 1), dict(type=AssertionError, msg="only contain floats")),
        (False, (0.2, 0.1), dict(type=AssertionError, msg="must have width >= 0")),
        (False, None, None),
        (False, (0.0, 0.1), None),
        (True, (0.1, 0.2), None),
    ],
)
def test_SignalADC_vertical_shift(
    motor_on: bool, offset_window: tuple[float, float], error: dict
):
    # input voltages
    v0t, v1t, v0k, v1k = 1, 4, 0.5, 2
    mt, mk = v1t - v0t, v1k - v0k

    num_points = 101
    voltages = np.array(
        [
            [np.linspace(v0t, v1t, num_points), np.linspace(v0k, v1k, num_points)],
            [np.linspace(v0t, v1t, num_points), np.linspace(v0k, v1k, num_points)],
        ]
    )

    if error is not None:
        with pytest.raises(error["type"]) as exc:
            SignalADC.read(
                data_array=voltages,
                motor_on=motor_on,
                average_offset_to_zero=True,
                offset_measure_window=offset_window,
            )
            assert re.match(error["msg"], str(exc.value))
    else:
        signal = SignalADC.read(
            data_array=voltages,
            motor_on=motor_on,
            average_offset_to_zero=True,
            offset_measure_window=offset_window,
            pulse_duration=1.0,
        )
        if offset_window is not None:
            # Vertical shift
            xm = np.average(offset_window)
            vmt = v0t + mt * xm
            vmk = v0k + mk * xm

            # Assert signal timeseries match expected
            if motor_on:
                expected_tnodes = voltages[0, 0, :] - vmt
                expected_knodes = voltages[0, 1, :] - vmk
            else:
                expected_tnodes = voltages[:, 0, :] - vmt
                expected_knodes = voltages[:, 1, :] - vmk
        else:
            if motor_on:
                expected_tnodes = voltages[0, 0, :]
                expected_knodes = voltages[0, 1, :]
            else:
                expected_tnodes = voltages[:, 0, :]
                expected_knodes = voltages[:, 1, :]

        np.testing.assert_almost_equal(signal.raw_tnodes, expected_tnodes)
        np.testing.assert_almost_equal(signal.raw_knodes, expected_knodes)


def test_SignalSynthetic_read():
    t = np.linspace(0, 24e-6, 10000)
    num_electrodes = 15
    num_signals = 2 * num_electrodes * num_electrodes
    np.random.seed(145)

    v_transmit = np.random.random(t.shape)
    signals = np.random.random((num_signals, len(t)))

    data = np.empty((2 + num_signals, len(t)))
    data[0, :] = t[:]
    data[1, :] = v_transmit[:]
    data[2:, :] = signals

    for i in range(1, 1 + num_electrodes):
        for j in range(1, 1 + num_electrodes):
            idx = num_electrodes * (i - 1) + (j - 1)
            actual_output = SignalSynthetic.read(
                data=data, transmit=i, receive=j, interval=1
            )
            np.testing.assert_array_equal(actual_output.tnodes, signals[2 * idx])
            np.testing.assert_array_equal(actual_output.knodes, signals[2 * idx + 1])
            np.testing.assert_array_equal(actual_output.vsources, v_transmit)
            np.testing.assert_array_equal(actual_output.times, t)
