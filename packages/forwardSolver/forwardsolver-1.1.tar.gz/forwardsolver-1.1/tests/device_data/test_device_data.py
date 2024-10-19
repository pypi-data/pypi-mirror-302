import datetime
import os
import re

import h5py
import numpy as np
import pytest

from forwardSolver.scripts.utils.device_data.device_data import (
    DeviceData,
    DeviceDataADC,
    DeviceDataHDF,
    DeviceDataParams,
    build_banded_matrix_from_vector,
)
from forwardSolver.scripts.utils.device_data.signal import SignalHDF


# Function required for test
def print_datasets(f, filter_strings=[]):
    """
    Returns all datasets in a file f, which contain all metadata in
    filter_strings (e.g. if a filter_string is "Span1".
    A filter_string is anything that is found within the h5 filename)

    Function to list all datasets in H5 file.
    Returns list of datasets that are in the groups given by filter_strings.

    eg.
    print_datasets(dataset, filter_strings = ['Air', 'Span1'])
    returns a list of the location of span 1 measurements for Air.
    """
    h5_elements = []

    def filter_datasets(h5_element):
        is_dataset = isinstance(f[h5_element], h5py._hl.dataset.Dataset)
        contains_filter_string = [
            True for filter_string in filter_strings if filter_string in h5_element
        ]
        if is_dataset and len(contains_filter_string) == len(filter_strings):
            return True
        else:
            return False

    f.visit(
        lambda h5_element: (
            h5_elements.append(h5_element)
            if filter_datasets(h5_element) is True
            else None
        )
    )
    return h5_elements


@pytest.mark.usefixtures("hdf_file", "foo_file")
def test_DeviceData_read_file(hdf_file, foo_file):
    """
    Testing that the correct concretised data type is called
    depending on the argument passed to DeviceData.read_file
    """

    data_hdf = DeviceData.read_file(hdf_file)

    assert isinstance(data_hdf, DeviceData)
    assert isinstance(data_hdf, DeviceDataHDF)

    with pytest.raises(ValueError):
        _ = DeviceData.read_file("donkey")

    with pytest.raises(TypeError):
        _ = DeviceData.read_file(foo_file)


@pytest.mark.usefixtures("hdf_file")
def test_DeviceData_read_hdf_file(hdf_file):
    """
    Test that a full HDF file is properly read
    """

    hdf = h5py.File(hdf_file, "r")
    datasets = print_datasets(hdf, filter_strings=["PulseResponse"])

    data: DeviceDataHDF = DeviceData.read_file(hdf)
    for __set in datasets:
        transmit, receive = re.search(r"T(\d+)/R(\d+)", __set).groups((1, 2))

        __signal = data.signal(transmit=int(transmit), receive=int(receive))

        np.testing.assert_array_equal(hdf[__set][0, :, 0, :], __signal.raw_times)
        np.testing.assert_array_equal(hdf[__set][0, :, 1, :], __signal.raw_tnodes)
        np.testing.assert_array_equal(hdf[__set][0, :, 2, :], __signal.raw_knodes)

        for k, v in data.metadata.params_map.items():
            obj_attr = getattr(data.metadata, v)

            dat_attr = hdf[__set].attrs[k]
            if data.metadata.types[v] == np.ndarray:
                attr_val = np.array(dat_attr)
            else:
                if data.metadata.types[v] == str:
                    attr_val = dat_attr.strip()
                elif data.metadata.types[v] in [int, float, bool]:
                    attr_val = (
                        data.metadata.types[v](dat_attr) if dat_attr != "" else None
                    )
                elif data.metadata.types[v] in [
                    datetime.date,
                    datetime.datetime,
                ]:
                    attr_val = data.metadata.types[v].fromisoformat(dat_attr)
                else:
                    raise AttributeError(f"Unknown attribute {v}")

            if isinstance(obj_attr, np.ndarray):
                np.testing.assert_array_equal(obj_attr, attr_val)
            else:
                np.testing.assert_equal(obj_attr, attr_val)

    hdf.close()


@pytest.mark.usefixtures("hdf_file")
def test_DeviceData_to_dict(hdf_file):
    data = DeviceData.read_file(hdf_file)

    actual_output = data.to_dict()

    expected_output = dict(filename=str(hdf_file))
    np.random.seed(123)
    expected_output["data"] = {
        i + 1: {j + 1: i * 2 + j for j in range(2)} for i in range(2)
    }

    expected_output["interval"] = 1
    expected_output["metadata"] = DeviceDataParams.read_hdf_metadata(
        {
            "BARO_PRESSURE": "",
            "BOARD_ID": "",
            "CABLE_SET": "",
            "DATE": "2022-09-28",
            "INPUT_PARAM": [[50, 50, 20, 90]],
            "MATERIAL": "",
            "OSC_BANDWIDTH_CH1": "1.0000E+9\n",
            "OSC_BANDWIDTH_CH2": "1.0000E+9\n",
            "OSC_BANDWIDTH_CH3": "1.0000E+9\n",
            "OSC_BANDWIDTH_CH4": "1.0000E+9\n",
            "OSC_HSCALE": "4.0000E-6\n",
            "OSC_MODE": "HIRES\n",
            "OSC_MODEL": "MDO4104C",
            "OSC_MODE_CH1": "1.0000E+9\n",
            "OSC_MODE_CH2": "1.0000E+9\n",
            "OSC_MODE_CH3": "1.0000E+9\n",
            "OSC_MODE_CH4": "1.0000E+9\n",
            "OSC_OFFSET_CH1": "0.0E+0\n",
            "OSC_OFFSET_CH2": "0.0E+0\n",
            "OSC_OFFSET_CH3": "0.0E+0\n",
            "OSC_OFFSET_CH4": "0.0E+0\n",
            "OSC_POS_CH1": "0.0E+0\n",
            "OSC_POS_CH2": "0.0E+0\n",
            "OSC_POS_CH3": "0.0E+0\n",
            "OSC_POS_CH4": "0.0E+0\n",
            "OSC_PROBE_CONFIG_CH1": r"\"TPP1000\";\"C148297\";100.0000E-3;\"V\";10.0000E+6;\"TPP1000\";5.3000E-9;5.3000E-9\n",
            "OSC_PROBE_CONFIG_CH2": r"\"No probe detected\";\"\";100.0000E-3;\"V\";0.0E+0;\"Other\";0.0E+0;0.0E+0\n",
            "OSC_PROBE_CONFIG_CH3": r"\"TPP1000\";\"C148279\";100.0000E-3;\"V\";10.0000E+6;\"TPP1000\";5.3000E-9;5.3000E-9\n",
            "OSC_PROBE_CONFIG_CH4": r"\"No probe detected\";\"\";100.0000E-3;\"V\";0.0E+0;\"Other\";0.0E+0;0.0E+0\n",
            "OSC_PROBE_ID_CH1": r"\"TPP1000\";\"C148297\"\n",
            "OSC_PROBE_ID_CH2": r"\"No probe detected\";\"\"\n",
            "OSC_PROBE_ID_CH3": r"\"TPP1000\";\"C148279\"\n",
            "OSC_PROBE_ID_CH4": r"\"No probe detected\";\"\"\n",
            "OSC_PROBE_SN_CH1": r"\"C148297\"\n",
            "OSC_PROBE_SN_CH2": r"\"\"\n",
            "OSC_PROBE_SN_CH3": r"\"C148279\"\n",
            "OSC_PROBE_SN_CH4": r"\"\"\n",
            "OSC_RECORD": "100000\n",
            "OSC_SAMPLE_RATE": "2.5000E+9\n",
            "OSC_SN": "SN000011627",
            "OSC_TERM_CH1": "1.0000E+6\n",
            "OSC_TERM_CH2": "50.0000\n",
            "OSC_TERM_CH3": "1.0000E+6\n",
            "OSC_TERM_CH4": "1.0000E+6\n",
            "OSC_VSCALE_CH1": "600.0000E-3\n",
            "OSC_VSCALE_CH2": "6.0000\n",
            "OSC_VSCALE_CH3": "600.0000E-3\n",
            "OSC_VSCALE_CH4": "600.0000E-3\n",
            "PHANTOM": "",
            "PHANTOM_OR": "",
            "PHANTOM_OR2": "",
            "PIC_FIRMWARE": "P1000v9\n",
            "PROBE": "",
            "PROBE_SET": "",
            "PROBE_TIP": "",
            "PYTHON_GIT_BRANCH": "P1000-009_pic-control",
            "PYTHON_GIT_IS_DIRTY": True,
            "PYTHON_GIT_SHA": "7bd482f1286329b67ccb25b25153f2190d82744b",
            "RECEIVE_POINT": 1,
            "REP_NUM": 5,
            "RHUMIDITY": "",
            "SG_MODEL": "AFG31252",
            "SG_SN": "70365",
            "TEMPERATURE": "",
            "TESTER": "",
            "TEST_PROTOCOL": "P1000-009-TP",
            "THP_MODEL": "PCE-THB 40",
            "THP_SN": "S056695",
            "TIMESTAMP": "2022-09-28 18:38:19.350714",
            "TRANSMIT_POINT": 1,
            "T_PROBE": "",
            "T_PROBE_SET": "",
            "T_PROBE_TIP": "",
            "UUT_ID": "",
        }
    ).to_dict()

    print(actual_output["metadata"])
    np.testing.assert_equal(actual_output, expected_output)


@pytest.mark.usefixtures("hdf_file")
def test_DeviceData_json_IO(hdf_file, tmp_path_factory):
    """
    Test the input/output to JSON file by creating a json file in the testing directory,
    loading it and comparing the two
    """

    hdf = h5py.File(hdf_file, "r")

    data = DeviceData.read_file(hdf)
    # Output to JSON

    jsonpath = tmp_path_factory.mktemp("data") / "device_data.json"

    data.to_json(jsonpath)

    # Assert that the file was created
    np.testing.assert_(os.path.isfile(jsonpath))

    # Read json file
    data_read = DeviceData.from_json(jsonfile=jsonpath)

    np.testing.assert_(data == data_read)

    hdf.close()


@pytest.mark.usefixtures("hdf_file")
def test_DeviceDataHDF_read_file(hdf_file):
    """
    Test the proper reading of an HDF file
    """
    # expected output
    hdf = h5py.File(hdf_file, "r")

    # actual output
    data: DeviceDataHDF = DeviceData.read_file(hdf_file)

    assert data.h5file == hdf


@pytest.mark.usefixtures("hdf_file")
def test_DeviceDataHDF_list_hdf_datasets(hdf_file):
    # expected output
    expected = [
        f"PulseResponse/{pair}" for pair in ["T1/R1", "T1/R2", "T2/R1", "T2/R2"]
    ]

    # actual output
    data: DeviceDataHDF = DeviceData.read_file(hdf_file)
    actual_output = data.list_hdf_datasets()

    np.testing.assert_equal(actual_output, expected)


@pytest.mark.usefixtures("hdf_file")
def test_DeviceDataHDF_read_hdf_datasets(hdf_file):
    """
    The DeviceDataHDF.read_hdf_datasets
        1. lists the hdf datasets and stores in DeviceDataHDF.filtered_datasets
            - this is tested in test_DeviceDataHDF_list_hdf_datasets
        2. reads the metadata from the first HDF dataset
        (the metadata will be the same across all datasets)
            - this is tested in tests/device_data/models/test_device_metadata.py
        3. Defines the number of electrodes
        4. Stores the number of the dataset corresponding to a T/R electrode pair in
        a num_electrodes x num_electrodes array

    This test is specifically that the return of this method is correct, i.e.
    testing only steps 3 and 4.
    """

    # expected output
    datasets = [
        f"PulseResponse/{pair}" for pair in ["T1/R1", "T1/R2", "T2/R1", "T2/R2"]
    ]
    expected = np.arange(len(datasets)).reshape((2, 2))

    # actual output
    data: DeviceDataHDF = DeviceData.read_file(hdf_file)
    actual = data.read_hdf_datasets()

    # Testing step 3.
    np.testing.assert_equal(data.electrodes, np.arange(1, 3))

    # Testing step 4.
    np.testing.assert_array_equal(actual, expected)


@pytest.mark.usefixtures("hdf_file")
def test_DeviceDataHDF_signal(hdf_file):
    """
    Test that the signals are read and imported correctly
    """

    # expected output
    np.random.seed(123)  # same as in the fixture
    datasets = np.array([np.random.rand(1, 5, 4, 1000) for _ in range(4)])

    # actual output
    data = DeviceData.read_file(hdf_file)

    # Testing
    for s, pair in enumerate([(1, 1), (1, 2), (2, 1), (2, 2)]):
        signal: SignalHDF = data.signal(transmit=pair[0], receive=pair[1])

        np.testing.assert_array_equal(datasets[s][0, :, 0, :], signal.raw_times)
        np.testing.assert_array_equal(datasets[s][0, :, 1, :], signal.raw_tnodes)
        np.testing.assert_array_equal(datasets[s][0, :, 2, :], signal.raw_knodes)


@pytest.mark.usefixtures("hdf_file")
def test_DeviceDataHDF_get_subset(hdf_file):
    # expected output
    np.random.seed(123)  # same as in the fixture
    datasets = np.array([np.random.rand(1, 5, 4, 1000) for _ in range(4)])

    data: DeviceDataHDF = DeviceData.read_file(hdf_file)

    # Fixture data has five repetitions
    nreps = 5
    num_electrodes = np.max(data.electrodes)

    for n in range(1, nreps + 1):
        # Actual output
        _times, _tnodes, _knodes = data.get_subset(n)

        for i in range(num_electrodes * num_electrodes):
            transmit = i // num_electrodes
            receive = i % num_electrodes

            # Expected output
            fixture_data = datasets[i][0, :n, :, :]

            np.testing.assert_array_equal(
                fixture_data[:, 0, :], _times[transmit][receive]
            )
            np.testing.assert_array_equal(
                fixture_data[:, 1, :], _tnodes[transmit][receive]
            )
            np.testing.assert_array_equal(
                fixture_data[:, 2, :], _knodes[transmit][receive]
            )


# ADC specific testing


@pytest.fixture
def signals_dict():
    dd_adc = DeviceDataADC()
    return dd_adc.read_hdf_datasets()


@pytest.fixture(scope="session")
def hdf_adc_file(tmp_path_factory):
    num_turns = 2
    num_electrodes = 15
    num_samples_tot = 3
    num_frames = num_electrodes * (num_electrodes + 1)
    np.random.seed(123)
    voltages = np.random.rand(num_turns, num_frames, num_samples_tot)
    fn = tmp_path_factory.mktemp("data") / "HDF_adc_file.h5"
    simple_counter = 0
    with h5py.File(fn, "w") as hf:
        # create a data group and assing the metadata as attributes
        hgroup = hf.create_group("scan_data")

        for t in range(1, num_electrodes + 1):
            for r in range(t, num_electrodes + 1):
                # slice the data with T and K node
                data = voltages[
                    :, simple_counter : (simple_counter + 2), :  # noqa: E203
                ]
                # create dataset
                dataset = hgroup.create_dataset(f"T{t}R{r}", data=data)
                # if the transmit is even, add overvoltage flag
                dataset.attrs["over_voltage"] = t % 2 == 0
                if t != r:
                    dataset = hgroup.create_dataset(f"T{r}R{t}", data=data)
                    dataset.attrs["over_voltage"] = r % 2 == 0

                simple_counter += 2
    return fn


@pytest.fixture
@pytest.mark.usefixtures("hdf_adc_file")
def DeviceDataADC_instance(hdf_adc_file):
    return DeviceData.read_file(
        hdf_adc_file, source="device", average_offset_to_zero=False
    )


def test_read_hdf_dataset():
    signals_dict = {}
    signals_dict[(1, 1)] = "T1R1"
    signals_dict[(1, 2)] = "T1R2"
    signals_dict[(1, 3)] = "T1R3"
    signals_dict[(2, 2)] = "T2R2"
    signals_dict[(2, 3)] = "T2R3"
    signals_dict[(3, 3)] = "T3R3"
    signals_dict[(2, 1)] = "T2R1"
    signals_dict[(3, 1)] = "T3R1"
    signals_dict[(3, 2)] = "T3R2"

    num_electrodes = 3

    dd_adc = DeviceDataADC()
    assert signals_dict == dd_adc.read_hdf_datasets(num_electrodes)


def test_read_overvoltages(hdf_adc_file):
    DeviceDataADC_instance: DeviceDataADC = DeviceData.read_file(
        hdf_adc_file, source="device", average_offset_to_zero=False
    )

    expected_over_voltages = np.zeros(
        (
            len(DeviceDataADC_instance.electrodes),
            len(DeviceDataADC_instance.electrodes),
        )
    )
    for t in range(1, len(DeviceDataADC_instance.electrodes) + 1):
        expected_over_voltages[t - 1, :] = t % 2 == 0

    # Execute the method under test
    over_voltages = DeviceDataADC_instance.read_overvoltages()

    # Verify the results
    print("actual:", over_voltages[0, :])
    print("expected:", expected_over_voltages[0, :])
    np.testing.assert_array_equal(over_voltages, expected_over_voltages)


def test_DeviceDataADC_read_file(hdf_adc_file):
    DeviceDataADC_instance = DeviceData.read_file(
        hdf_adc_file, source="device", average_offset_to_zero=False
    )

    # ensure super class cls works correctly
    assert DeviceDataADC_instance.interval == 1
    assert DeviceDataADC_instance.motor_on is False
    assert DeviceDataADC_instance.rotation_id == 0
    assert DeviceDataADC_instance.group_name == "scan_data"


@pytest.mark.parametrize(
    "t, k, slice_ind, rot_id, error_bool",
    [
        (1, 1, 0, 1, False),
        (1, 2, 2, 1, False),
        (2, 1, 2, 1, False),
        (16, 15, 2, 1, True),
        (1, 2, 2, 3, True),
    ],
)
def test_DeviceDataADC_signal_default(
    DeviceDataADC_instance, t, k, slice_ind, rot_id, error_bool
):
    np.random.seed(123)
    voltages = np.random.rand(2, 15 * 16, 3)
    error = False

    # test raw_tnode raw_knode assignment
    try:
        np.testing.assert_equal(
            DeviceDataADC_instance.signal(t, k).raw_tnodes,
            voltages[:, slice_ind, :],
        )
        np.testing.assert_equal(
            DeviceDataADC_instance.signal(t, k).raw_knodes,
            voltages[:, slice_ind + 1, :],
        )
    except ValueError:
        error = True

    # test version where a single rotation is used for reps
    DeviceDataADC_instance.motor_on = True
    DeviceDataADC_instance.rotation_id = rot_id
    try:
        np.testing.assert_equal(
            DeviceDataADC_instance.signal(t, k).raw_tnodes,
            voltages[rot_id, slice_ind, :],
        )
    except (ValueError, IndexError):
        error = True
    assert error == error_bool


@pytest.mark.parametrize(
    "vector, expected",
    [
        ([1], np.array([[1]])),
        ([1, 2, 3], np.array([[1, 2, 3], [2, 1, 2], [3, 2, 1]])),
        ([[2]], "Array [[2]] is not a 1D array"),
        ([], "Array [] does not have elements"),
    ],
)
def test_build_banded_matrix_from_vector(vector, expected):
    if isinstance(expected, np.ndarray):
        np.testing.assert_array_equal(build_banded_matrix_from_vector(vector), expected)
    else:
        with pytest.raises(AssertionError) as exc:
            build_banded_matrix_from_vector(vector)
            assert str(exc.value) == expected


@pytest.mark.parametrize(
    "gains_per_span, error",
    [
        (None, None),
        ([1, 2, 3], dict(type=ValueError, msg="Incorrect number of gains")),
        (np.ones((2, 15)), None),
        (1 + 2 * np.random.random((2, 15)), None),
        (
            1 + 2 * np.random.random(15),
            dict(type=ValueError, msg="need both T and K gains"),
        ),
        (
            [np.arange(15), np.arange(15)],
            dict(type=ValueError, msg="Cannot have zero gains"),
        ),
    ],
)
def test_DeviceDataADC_gains_per_span(hdf_adc_file, gains_per_span: list, error: dict):
    if error is None:
        # Check that reading the data with and without the given gains gives the correct change
        data_no_gains = DeviceDataADC.read_file(adcfile=hdf_adc_file)
        data_with_gains = DeviceDataADC.read_file(
            adcfile=hdf_adc_file, gains_per_span=gains_per_span
        )

        tnode_factor = data_with_gains.tnode_voltages / data_no_gains.tnode_voltages
        knode_factor = data_with_gains.knode_voltages / data_no_gains.knode_voltages

        # Check the gains per span are properly set
        np.testing.assert_array_equal(
            data_no_gains.gains_per_pair, np.ones((2, 15, 15))
        )
        if gains_per_span is None:
            np.testing.assert_array_equal(
                data_with_gains.gains_per_pair, np.ones((2, 15, 15))
            )
            expected_factor = np.ones((2, 15, 15, tnode_factor.shape[-1]))
        else:
            np.testing.assert_array_equal(
                data_with_gains.gains_per_pair,
                np.array(
                    [
                        build_banded_matrix_from_vector(gains_per_span[0]),
                        build_banded_matrix_from_vector(gains_per_span[1]),
                    ]
                ),
            )
            expected_factor = np.repeat(
                np.array(
                    [
                        build_banded_matrix_from_vector(1 / gains_per_span[0]),
                        build_banded_matrix_from_vector(1 / gains_per_span[1]),
                    ]
                )[:, :, :, np.newaxis],
                tnode_factor.shape[-1],
                axis=3,
            )

        # Check the voltage gain factor is correctly applied
        np.testing.assert_array_almost_equal(tnode_factor, expected_factor[0])
        np.testing.assert_array_almost_equal(knode_factor, expected_factor[1])
    else:
        with pytest.raises(error["type"]) as exc:
            DeviceDataADC.read_file(adcfile=hdf_adc_file, gains_per_span=gains_per_span)
            assert re.match(error["msg"], str(exc.value))


def test_DeviceDataADC_gain_correction(hdf_adc_file):
    gains_per_span = np.ones((2, 15))
    # Correct the gains for tnode(1,2) and knode(12, 5)
    gain_1, node_1, transmit_1, receive_1 = 4.0, 0, 1, 2
    gain_2, node_2, transmit_2, receive_2 = 7.0, 1, 12, 5
    gain_correction_list = [
        [gain_1, node_1, transmit_1, receive_1],
        [gain_2, node_2, transmit_2, receive_2],
    ]
    # Form the device data objects with and without gains
    data_no_gains = DeviceDataADC.read_file(adcfile=hdf_adc_file)
    data_with_corrected_gains = DeviceDataADC.read_file(
        adcfile=hdf_adc_file,
        gains_per_span=gains_per_span,
        gain_correction_list=gain_correction_list,
    )
    gain_1_obtained = np.max(
        data_no_gains.tnode_voltages[transmit_1 - 1, receive_1 - 1]
    ) / np.max(data_with_corrected_gains.tnode_voltages[transmit_1 - 1, receive_1 - 1])

    gain_2_obtained = np.max(
        data_no_gains.knode_voltages[transmit_2 - 1, receive_2 - 1]
    ) / np.max(data_with_corrected_gains.knode_voltages[transmit_2 - 1, receive_2 - 1])

    np.testing.assert_equal(gain_1_obtained, gain_1)
    np.testing.assert_equal(gain_2_obtained, gain_2)
