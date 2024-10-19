import os
from typing import Dict, List, Union

import h5py
import numpy as np
import pytest

from forwardSolver.scripts.utils.device_data.device_data import DeviceDataHDF
from forwardSolver.scripts.utils.device_data.signal import SignalHDF
from forwardSolver.scripts.utils.logging import close_logger, get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="session")
def foo_file(tmp_path_factory) -> str:
    fn = tmp_path_factory.mktemp("data") / "foo_file.txt"
    f = open(fn, "w")
    f.close()
    return fn


@pytest.fixture(scope="session")
def hdf_file(tmp_path_factory) -> str:
    fn = tmp_path_factory.mktemp("data") / "HDF_file.h5"
    hdf = h5py.File(fn, "w")
    # write data to HDF file

    attrs = {
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

    # The actual data in the HDF is irrelevant for the current testing purposes
    # so we don't expose it but instead fix the seed to ensure it won't vary between
    # testing sessions
    np.random.seed(123)
    for pair in ["T1/R1", "T1/R2", "T2/R1", "T2/R2"]:
        _set = hdf.create_dataset(
            f"PulseResponse/{pair}", data=np.random.rand(1, 5, 4, 1000)
        )
        for k, v in attrs.items():
            _set.attrs.create(k, v)

    hdf.close()
    return fn


def random_signal() -> SignalHDF:
    signal = SignalHDF()
    times = np.linspace(0, 1, int(1e4))
    signal.times = times
    signal.tnodes = np.random.random(times.shape)
    signal.knodes = np.random.random(times.shape)
    signal.raw_vsources = 2.5 * np.random.random(times.shape)
    # To ensure the results are the same, we need to generate the same number
    # of random numbers so that the sequence is the same as before (i.e. the
    # sequence of numbers that returns the K matrix and capacitances that are
    # hardcoded into the tests)
    _ = np.random.random(times.shape)
    signal.nreps = 1
    return signal


@pytest.fixture(scope="session")
def device_data() -> DeviceDataHDF:
    class MockDeviceDataHDF(DeviceDataHDF):
        mock_data: Dict[int, Dict[int, SignalHDF]]

        @classmethod
        def read(
            cls, h5file: Union[str, os.PathLike, h5py.File], interval: int = 1
        ) -> "DeviceDataHDF":
            data = MockDeviceDataHDF()
            data.filename = str(h5file)
            data.interval = int(interval)
            data.signals = data.read_hdf_datasets()
            data.electrodes = [x for x in range(1, 16)]

            np.random.seed(123)
            data.mock_data = {
                i: {j: random_signal() for j in range(1, 16)} for i in range(1, 16)
            }
            # Symmetrise the mock_data
            for i in range(1, 16):
                for j in range(1, i):
                    data.mock_data[j][i] = data.mock_data[i][j]

            return data

        def read_hdf_datasets(self, filter_strings: List[str] = ...) -> np.ndarray:
            logger.debug("called fake datasets")
            return np.array([])

        def signals(self) -> np.ndarray:
            logger.debug("called fake signals")
            return np.array([])

        def signal(self, transmit: int, receive: int) -> SignalHDF:
            logger.debug("called fake signal")
            return self.mock_data[transmit][receive]

    return MockDeviceDataHDF.read(None, 1)


close_logger(logger)
