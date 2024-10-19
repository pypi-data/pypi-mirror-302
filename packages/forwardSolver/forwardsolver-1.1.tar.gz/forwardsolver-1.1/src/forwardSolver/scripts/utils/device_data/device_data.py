import io
import json
import os
import re
from functools import cached_property
from typing import Dict, List, Tuple, Union, abstractmethod

import h5py
import numpy as np

from forwardSolver.scripts.utils.constants import HDF_EXTENSIONS
from forwardSolver.scripts.utils.device_data.models.device_metadata import (
    DeviceDataParams,
)
from forwardSolver.scripts.utils.device_data.models.noise_data import NoiseData
from forwardSolver.scripts.utils.device_data.signal import (
    Signal,
    SignalADC,
    SignalHDF,
    SignalSynthetic,
)
from forwardSolver.scripts.utils.json_coder import (
    CustomJsonDecoder,
    CustomJsonEncoder,
)
from forwardSolver.scripts.utils.logging import get_logger

logger = get_logger(__name__)


def build_banded_matrix_from_vector(array: np.ndarray) -> np.ndarray:
    """
    Takes a one dimensional N-component `array` and creates a two dimensional NxN matrix
    where every element of the i-th diagonal is the i-th element of the array.

    Example:
        input = [1, 2, 3, 4]
        output = [
            [1, 2, 3, 4],
            [2, 1, 2, 3],
            [3, 2, 1, 2],
            [4, 3, 2, 1],
        ]

    Args:
        array (np.ndarray): 1D array

    Returns:
        np.ndarray: 2D banded array
    """
    assert np.asarray(array).ndim == 1, f"Array {array} is not a 1D array"
    assert len(array) > 0, f"Array {array} does not have elements"
    return np.diag(np.tile(array[0], len(array))) + sum(
        [
            np.diag(np.tile(array[i], len(array) - i), i)
            + np.diag(np.tile(array[i], len(array) - i), -i)
            for i in range(1, len(array))
        ]
    )


class DeviceData:
    """
    Class to interface with device data.
    Concrete classes for reading HDF files or ADC files will be defined

    Attributes:
    -----------
        signals (np.ndarray): numpy array containing the signals corresponding to each
                              transmit/receive pair
        interval (int): sampling rate to read the voltage time-series
        filename (str): name of the file with the data
        metadata (DeviceDataParams): metadata stored with the voltage time-series
        electrodes (np.ndarray): np.arange from 1 to the number of electrodes
        good_repeats (Dict[str, np.ndarray]): A dictionary containing the specific good
            repeats in each transmit/receive dataset. e.g. {'T1R2': [0,1,3] } means that
            repeats 0, 1 and 3 satisfied the noise threshold.
    """

    signals: Union[np.ndarray, dict] = None
    filename: str = None
    interval: int = None
    metadata: DeviceDataParams = None
    electrodes: np.ndarray = np.arange(0)
    _good_repeats: Dict[str, np.ndarray] = None
    _h5file: h5py.File = None

    @abstractmethod
    def signal(self, transmit: int, receive: int) -> Signal:
        """
        Retrieve the signal between given transmit and receive electrodes

        Args:
            transmit (int): Transmit electrode number
            receive (int): Receive electrode number

        Raises:
            ValueError: if the provided pair (transmit, receive) is not recognised
            AttributeError: if the signal data has not yet been retrieved.

        Returns:
            Signal
        """
        logger.warning(
            "Abstract method DeviceData.signal(transmit, receive) called, "
            "empty signal returned."
        )
        return Signal()

    @classmethod
    def read_file(
        self,
        fname: Union[str, os.PathLike, h5py.File],
        interval: int = 1,
        source: str = "oscilloscope",
        **adc_kwargs,
    ) -> "DeviceData":
        """Read supplied file

        Args:
            fname (str): filename
            interval (int): downsampling interval
            source (str): source of H5 file. Options are ["oscilloscope", "device"]
            adc_kwargs (dict): keyword args for DeviceDataADC.read_file

        Returns:
            DeviceData
        """
        if isinstance(fname, h5py.File) and source == "oscilloscope":
            return DeviceDataHDF.read_file(fname, interval=interval)
        else:
            if os.path.isfile(fname):
                if (
                    str(fname).lower().endswith(HDF_EXTENSIONS)
                    and source == "oscilloscope"
                ):
                    return DeviceDataHDF.read_file(fname, interval=interval)
                elif str(fname).lower().endswith(HDF_EXTENSIONS) and source == "device":
                    return DeviceDataADC.read_file(
                        fname, interval=interval, **adc_kwargs
                    )
                else:
                    raise TypeError(
                        f"Unrecognised data file {fname} or 'source' keyword - choose 'oscilloscope' or 'device'"
                    )
            else:
                raise ValueError(f"Provided filename {fname} is not an existing file.")

    @cached_property
    def tnode_voltages(self) -> np.ndarray:
        """Numpy array of averages of tnode_voltage measurements"""
        return np.array(
            [
                [self.signal(i, j).tnodes for j in self.electrodes]
                for i in self.electrodes
            ]
        )

    @property
    def h5file(self) -> h5py.File:
        return self._h5file

    @h5file.setter
    def h5file(self, h5file: Union[str, os.PathLike, h5py.File]):
        if h5file is not None:
            if isinstance(h5file, str):
                if os.path.isfile(h5file):
                    try:
                        self._h5file = h5py.File(h5file, "r")
                        self.filename = h5file
                    except Exception:
                        raise ValueError(
                            f"Provided string {h5file} is not a valid HDF file."
                        )
                else:
                    raise ValueError(f"Provided string {h5file} is not a file.")
            elif isinstance(h5file, os.PathLike):
                self._h5file = h5py.File(h5file, "r")
                self.filename = str(h5file)
            elif isinstance(h5file, h5py.File):
                self._h5file = h5file
                self.filename = str(h5file.filename)
            else:
                raise TypeError(f"Could not initialise DeviceData using {type(h5file)}")
        else:
            self._h5file = None
            self.filename = None

    @cached_property
    def knode_voltages(self) -> np.ndarray:
        """Numpy array of averages of knode_voltage measurements"""
        return np.array(
            [
                [self.signal(i, j).knodes for j in self.electrodes]
                for i in self.electrodes
            ]
        )

    @cached_property
    def times(self) -> np.ndarray:
        """Numpy array of averages of time measurements"""
        return np.array(
            [
                [self.signal(i, j).times for j in self.electrodes]
                for i in self.electrodes
            ]
        )

    @property
    def good_repeats(self) -> Dict[str, np.ndarray]:
        return self._good_repeats

    @good_repeats.setter
    def good_repeats(self, noise_data: List[NoiseData]):
        """
        Set the value of good repeats.
        If electrode pairs contain only noisy data then this is aborted.

        i.e. Only set device_data good repeats if all electrodes
        contain at least one non-noisy repeat.
        """
        if not np.all([len(d.good_repeats) > 0 for d in noise_data]):
            logger.warning(
                "No good repeats found for some electrode pairs. "
                "Mask will not be applied."
            )
        else:
            self._good_repeats = {
                f"T{d.transmit}R{d.receive}": d.good_repeats for d in noise_data
            }

    def __eq__(self, other: "DeviceData") -> bool:
        try:
            np.testing.assert_equal(self.to_dict(), other.to_dict())
        except AssertionError:
            return False
        return True

    def to_dict(self) -> Dict:
        """
        Convert current DeviceData to a dict
        """
        datadict = {
            int(i): {int(j): self.signals[i - 1, j - 1] for j in self.electrodes}
            for i in self.electrodes
        }
        return {
            "filename": self.filename,
            "interval": self.interval,
            "data": datadict,
            "metadata": self.metadata.to_dict(),
        }

    def get_subset(self, nrepeats: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Get a subset of the data using a lower number of repeats.

        Arguments:
        ----------
            nrepeats (int): number of repeated measurements to use
                            (strictly positive integer)

        Returns:
        --------
            Tuple[np.ndarray, np.ndarray, np.ndarray]: times, tnode data, knode data
        """
        if nrepeats <= 0:
            logger.warning(
                f"Attempted to get invalid subset using {nrepeats} repeats. "
                "Defaulting to full signal."
            )
            _nreps = self.signal(1, 1).nreps
        else:
            _nreps = nrepeats

        if isinstance(self, DeviceDataHDF):
            times = np.array(
                [
                    [self.signal(i, j).raw_times[:_nreps, :] for j in self.electrodes]
                    for i in self.electrodes
                ]
            )
        else:
            times = np.array(
                [
                    [self.signal(i, j).times for j in self.electrodes]
                    for i in self.electrodes
                ]
            )

        tnodes = np.array(
            [
                [self.signal(i, j).raw_tnodes[:_nreps, :] for j in self.electrodes]
                for i in self.electrodes
            ]
        )
        knodes = np.array(
            [
                [self.signal(i, j).raw_knodes[:_nreps, :] for j in self.electrodes]
                for i in self.electrodes
            ]
        )

        return times, tnodes, knodes

    def get_subset_in_range(
        self, num_repeats_range: tuple = (1, None)
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Get a subset of the data using a range of repeats.

        Arguments:
        ----------
            num_repeats_range (tuple): tuple of start and end repeat indices

        Returns:
        --------
            Tuple[np.ndarray, np.ndarray, np.ndarray]: times, tnode data, knode data
        """
        _num_repeats_start = num_repeats_range[0]
        _num_repeats_end = num_repeats_range[1]
        if _num_repeats_start <= 0 or _num_repeats_end <= 0:
            logger.warning(
                f"Attempted to get invalid subset using start index "
                "{_num_repeats_start}, "
                f"and end index {_num_repeats_end}. "
                "Defaulting to full signal."
            )
            _num_repeats_start = 1
            _num_repeats_end = self.signal(1, 1).nreps + 1
        elif _num_repeats_end is None:
            _num_repeats_end = self.signal(1, 1).nreps + 1

        repeats_slice = slice(_num_repeats_start - 1, _num_repeats_end - 1)
        times = np.array(
            [
                [self.signal(i, j).raw_times[repeats_slice, :] for j in self.electrodes]
                for i in self.electrodes
            ]
        )
        tnodes = np.array(
            [
                [
                    self.signal(i, j).raw_tnodes[repeats_slice, :]
                    for j in self.electrodes
                ]
                for i in self.electrodes
            ]
        )
        knodes = np.array(
            [
                [
                    self.signal(i, j).raw_knodes[repeats_slice, :]
                    for j in self.electrodes
                ]
                for i in self.electrodes
            ]
        )

        return times, tnodes, knodes

    def get_max_voltage_by_span(self) -> np.ndarray:
        """
        Get peak voltage averaged over spans
        returns 2 x num_electrodes array
        """
        max_tnodes = np.max(self.tnode_voltages, axis=2)
        max_knodes = np.max(self.knode_voltages, axis=2)

        return (
            np.array(
                [
                    np.mean(
                        list(np.diagonal(max_tnodes, i))
                        + list(np.diagonal(max_tnodes, -i))
                    )
                    for i in range(max_tnodes.shape[0])
                ]
            ),
            np.array(
                [
                    np.mean(
                        list(np.diagonal(max_knodes, i))
                        + list(np.diagonal(max_knodes, -i))
                    )
                    for i in range(max_knodes.shape[0])
                ]
            ),
        )

    def to_json(self, fpath: Union[str, os.PathLike]):
        """Dump self to a JSON file"""
        with open(fpath, "w") as file:
            json.dump(self.to_dict(), file, cls=CustomJsonEncoder, indent=4)

    @classmethod
    def from_dict(cls, datadict: Dict) -> "DeviceData":
        """
        Convert supplied dict to a DeviceData object
        """
        data = DeviceData()
        data.filename = datadict["filename"]
        data.metadata = DeviceDataParams.from_dict(datadict["metadata"])
        data.interval = datadict["interval"]

        data.electrodes = np.array(
            sorted(datadict["data"].keys(), key=lambda x: int(x))
        )
        data.signals = np.array(
            [
                [datadict["data"][transmit][receive] for receive in data.electrodes]
                for transmit in data.electrodes
            ]
        )
        data.electrodes = np.array(sorted([int(e) for e in data.electrodes]))
        return data

    @classmethod
    def from_json(cls, jsonfile: Union[str, os.PathLike]) -> "DeviceData":
        """Load data from a JSON file"""
        if os.path.isfile(jsonfile):
            with open(jsonfile, "r") as file:
                jsondata = json.load(file, cls=CustomJsonDecoder)
                return DeviceData.from_dict(jsondata)
        else:
            raise FileNotFoundError(f"File {jsonfile} could not be found")


class DeviceDataHDF(DeviceData):
    """
    Class to interface with HDF5 device data

    Attributes:
    -----------
    (in addition to those of DeviceData)
        h5file (h5py.File): HDF file encapsulated by the class
        filtered_datasets (List[str]): List of datasets matching the filtering criteria.

    """

    filtered_datasets: List[str] = None

    @classmethod
    def read_file(
        cls, h5file: Union[str, os.PathLike, h5py.File], interval: int = 1
    ) -> "DeviceDataHDF":
        """Read HDF file

        Process datasets and set class attributes

        Args:
            h5file (Union[str, os.PathLike, h5py.File]): str, Path, or HDF file to read
            interval (int, optional): Interval at which to read the timeseries data.
                                      Defaults to 1.

        Returns:
            DeviceDataHDF
        """
        data = cls()
        data.h5file = h5file
        data.interval = int(interval)
        data.signals = data.read_hdf_datasets()
        return data

    @cached_property
    def source_voltages(self) -> np.ndarray:
        """Numpy array of averages of source_voltage measurements"""
        return np.array(
            [
                [self.signal(i, j).vsources for j in self.electrodes]
                for i in self.electrodes
            ]
        )

    def list_hdf_datasets(self, filter_strings: List[str] = []) -> List[str]:
        """
        Property to list all datasets in the HDF5 file
        whose names contain *all* metadata in filter_strings

        Example: data.datasets(filter_strings = ['Air', 'Span1'])
                 returns a list of the location of span 1 measurements for Air

        Args:
            filter_strings (List[str]): Metadata to filter the datasets.
                                        Defaults to [].

        Returns:
            List[str]: List of datasets that are in the groupd given by filter_strings
        """

        datasets: List[str] = []

        def _filter_datasets(h5_element: str):
            if isinstance(self.h5file[h5_element], h5py.Dataset) and np.all(
                [_str in h5_element for _str in filter_strings]
            ):
                datasets.append(h5_element)
            else:
                return None

        self.h5file.visit(_filter_datasets)
        return datasets

    def read_hdf_datasets(
        self, filter_strings: List[str] = ["PulseResponse"]
    ) -> np.ndarray:
        """
        Convert the list of HDF datasets to a two dimensional numpy array

        Assumes that the HDF file includes a group of datasets called
        'PulseResponse' with 'T<N>/R<M>' in the name corresponding to
        the response between transmit electrode N and receive electrode M

        Returns:
            np.ndarray
        """
        # Set metadata from first signal
        self.filtered_datasets: List[str] = self.list_hdf_datasets(filter_strings)
        # Read metadata from the first dataset, assuming that the metadata is the same
        # across all datasets
        self.metadata = DeviceDataParams.read_hdf_metadata(
            self.h5file[self.filtered_datasets[0]].attrs
        )
        # Find the number of electrodes
        # TODO: Add number of electrodes to the metadata
        num_electrodes = len(
            set(
                [
                    re.search(r"T(\d+)/R(\d+)", d).group(1)
                    for d in self.filtered_datasets
                ]
            )
        )  # Define array of sorted electrode numbers
        self.electrodes = np.arange(1, num_electrodes + 1)
        # Initialise signals array
        self.signals = np.empty((num_electrodes, num_electrodes), dtype=SignalHDF)
        for count, n in enumerate(self.filtered_datasets):
            found_pattern = re.search(r"T(\d+)/R(\d+)", n)
            if found_pattern:
                transmit, receive = found_pattern.groups((1, 2))
                t, r = int(transmit) - 1, int(receive) - 1
                if t < num_electrodes and r < num_electrodes:
                    # save filtered dataset index
                    self.signals[t, r] = count

        return self.signals

    def signal(self, transmit: int, receive: int) -> SignalHDF:
        """
        Retrieve the signal between given transmit and receive electrodes

        Args:
            transmit (int): Transmit electrode number
            receive (int): Receive electrode number

        Raises:
            ValueError: if the provided pair (transmit, receive) is not recognised
            AttributeError: if the signal data has not yet been retrieved.

        Returns:
            Signal
        """
        if self.signals is not None:
            if transmit not in self.electrodes or receive not in self.electrodes:
                raise ValueError(
                    "Unrecognised (transmit, receive) pair " f"({(transmit, receive)})"
                )
            else:
                return SignalHDF.read(
                    self.h5file[
                        self.filtered_datasets[self.signals[transmit - 1, receive - 1]]
                    ],
                    interval=self.interval,
                    good_repeats=(
                        None
                        if self.good_repeats is None
                        else self.good_repeats.get(f"T{transmit}R{receive}")
                    ),
                )

        else:
            raise AttributeError("Have not read signals yet.")


class DeviceDataADC(DeviceData):
    """
    Class to interface with ADC device data

    Attributes:
        group_name (str): name of the data group in h5 file (assuming there is only one relevant group)
        motor_on (bool): motor status flag - if motor_on is False, the first dimension of the array is
            used as repeats. Otherwise user needs to specify rotation_id that is to be processed
        rotation_id (int): index of rotation to be processed, given motor is operational
            (motor_on = True)
        signals (dict): dictionary of references between (transmit, receive) pairs as keys and h5
            dataset names
        pulse_duration (float): Data capture window dureation. Defaults to 75us.
        gains_per_span (np.ndarray): array of gains applied to each signal, as a
                                     2 x num_electrodes x num_electrodes array.
                                    gains_per_span[0, :, :] are the T-node gains
                                    gains_per_span[1, :, :] are the K-node gains.
        average_offset_to_zero (bool): Whether the DC vertical component of the signals is averaged
                                       to zero or not. Defaults to False.
        offset_measure_window (tuple[float, float]): Time window to calculate the vertical offset.
        over_voltages (np.ndarray): array identifying signals for which ADC overvoltage
                                    flag was triggered
    """

    group_name: str = None
    motor_on: bool = False
    rotation_id: int = 0
    signals: dict = {}
    pulse_duration: float = 75e-6
    gains_per_span: np.ndarray = np.ones((2, 15, 15))
    average_offset_to_zero: bool = False
    offset_measure_window: tuple[float, float] = (0.5e-6, 1.5e-6)
    over_voltages: np.ndarray = np.zeros((15, 15))

    @classmethod
    def read_file(
        cls,
        adcfile: Union[str, os.PathLike],
        interval: int = 1,
        num_electrodes: int = 15,
        motor_on: bool = False,
        rotation_id: int = 0,
        gains_per_pair: np.ndarray = None,
        gains_per_span: list = None,
        gain_correction_list: list = None,
        pulse_duration: float = 75e-6,
        average_offset_to_zero: bool = True,
        offset_measure_window: tuple[float, float] = (0.5e-6, 1.5e-6),
    ) -> "DeviceDataADC":
        """Read ADC datafile

        Args:
            adcfile (Union[str, os.PathLike]): str or Path to read
            interval (int, optional): Interval at which to read the timeseries data.
                                      Defaults to 1.
            num_electrodes (int): number of electrodes in device. Defaults to 15.
            motor_on (bool): motor status flag - if motor_on is False, the first dimension of the array is
                used as repeats. Otherwise user needs to specify rotation_id that is to be processed
            rotation_id (int): if motor_on is True, choose which rotation to process
            gains_per_span (np.ndarray): array of gains applied to each signal, as a
                                     2 x num_electrodes x num_electrodes array.
            pulse_duration (float): Data capture window dureation. Defaults to 75us.
            average_offset_to_zero (bool): Whether the DC vertical component of the
                                           signals is averaged to zero or not. Defaults to True.
            offset_measure_window (tuple[float, float]): Time window to calculate the vertical offset.
                                                Defaults to (0.56us, 1.25us)

        Returns:
            DeviceDataADC
        """

        data = DeviceDataADC()
        data.filename = str(adcfile)
        data.h5file = adcfile
        data.interval = int(interval)
        data.signals = data.read_hdf_datasets(num_electrodes)
        data.motor_on = motor_on
        data.rotation_id = rotation_id
        hf = h5py.File(data.filename)
        # extract the name of the group
        data.group_name = list(hf.keys())[0]
        data.electrodes = range(1, num_electrodes + 1)
        if gains_per_pair is None:
            data.set_gains(gains_per_span)
            data.apply_gain_correction(gain_correction_list)
        else:
            data.gains_per_pair = gains_per_pair

        data.pulse_duration = pulse_duration
        data.average_offset_to_zero = average_offset_to_zero
        data.offset_measure_window = offset_measure_window

        return data

    @classmethod
    def read_filebytes(
        cls,
        filebytes: bytes,
        name: str,
        interval: int = 1,
        num_electrodes: int = 15,
        motor_on: bool = False,
        rotation_id: int = 0,
        gains_per_span: list = None,
        gain_correction_list: list = None,
        pulse_duration: float = 75e-6,
        average_offset_to_zero: bool = True,
        offset_measure_window: tuple[float, float] = (0.5e-6, 1.5e-6),
    ) -> "DeviceDataADC":
        """Read ADC datafile

        Args:
            adcfile (Union[str, os.PathLike]): str or Path to read
            interval (int, optional): Interval at which to read the timeseries data.
            Defaults to 1.
            num_electrodes (int): number of electrodes in device. Defaults to 15.
            motor_on (bool): motor status flag - if motor_on is False, the first dimension of the array is
            used as repeats. Otherwise user needs to specify rotation_id that is to be processed
            rotation_id (int): if motor_on is True, choose which rotation to process
            gains_per_span (np.ndarray): array of gains applied to each signal, as a
            2 x num_electrodes x num_electrodes array.
            pulse_duration (float): Data capture window dureation. Defaults to 75us.
            average_offset_to_zero (bool): Whether the DC vertical component of the
            signals is averaged to zero or not. Defaults to True.
            offset_measure_window (tuple[float, float]): Time window to calculate the vertical offset.
                                                Defaults to (0.56us, 1.25us)

        Returns:
            DeviceDataADC
        """

        data = DeviceDataADC()
        data.filename = name
        data.h5file = h5py.File(io.BytesIO(filebytes), "r")
        data.interval = int(interval)
        data.signals = data.read_hdf_datasets(num_electrodes)
        data.motor_on = motor_on
        data.rotation_id = rotation_id

        data.group_name = list(data.h5file.keys())[0]
        data.electrodes = range(1, num_electrodes + 1)
        data.set_gains(gains_per_span)
        data.apply_gain_correction(gain_correction_list)
        data.pulse_duration = pulse_duration
        data.average_offset_to_zero = average_offset_to_zero
        data.offset_measure_window = offset_measure_window
        data.read_overvoltages()

        return data

    def read_overvoltages(self) -> np.ndarray:
        """
        Retrieve ADC overvoltage flags from ADC
        """
        over_voltages = np.zeros((len(self.electrodes), len(self.electrodes)))

        with h5py.File(self.filename) as hf:
            for t in range(len(self.electrodes)):
                for r in range(len(self.electrodes)):
                    pair = f"T{t+1}R{r+1}"
                    if "over_voltage" in hf["scan_data"][pair].attrs.keys():
                        over_voltages[t, r] = int(
                            hf["scan_data"][pair].attrs["over_voltage"]
                        )
                    else:
                        over_voltages[t, r] = 0

        self.over_voltages = over_voltages.copy()
        return over_voltages

    def read_hdf_datasets(self, num_electrodes: int = 15):
        for t in range(1, num_electrodes + 1):
            for r in range(1, num_electrodes + 1):
                self.signals[(t, r)] = f"T{t}R{r}"
        return self.signals

    def signal(self, transmit: int, receive: int) -> SignalADC:
        """
        Retrieve the signal between given transmit and receive electrodes

        Args:
            transmit (int): Transmit electrode number
            receive (int): Receive electrode number

        Raises:
            ValueError: if the provided pair (transmit, receive) is not recognised
            AttributeError: if the signal data has not yet been retrieved.

        Returns:
            SignalADC
        """

        if self.signals is not None:
            if transmit not in self.electrodes or receive not in self.electrodes:
                raise ValueError(
                    "Unrecognised (transmit, receive) pair " f"({(transmit, receive)})"
                )
            else:
                data_array = np.array(
                    self.h5file[self.group_name].get(self.signals[(transmit, receive)])
                )
                return SignalADC.read(
                    data_array,
                    interval=self.interval,
                    good_repeats=(
                        None
                        if self.good_repeats is None
                        else self.good_repeats.get(f"T{transmit}R{receive}")
                    ),
                    motor_on=self.motor_on,
                    rotation_id=self.rotation_id,
                    gains=self.gains_per_pair[:, transmit - 1, receive - 1],
                    pulse_duration=self.pulse_duration,
                    average_offset_to_zero=self.average_offset_to_zero,
                    offset_measure_window=self.offset_measure_window,
                )
        else:
            raise AttributeError("Have not read signals yet.")

    def set_gains(self, gains: list = None):
        """
        Set gain values per span from 1D array of gains.
        If None, gains_per_span will default to 1 for every electrode pair.

        Args:
            gains (list): 1D array of gains per span. Must be len = num_electrodes,
                          and cannot have zeros

        """
        if gains is None:
            self.gains_per_pair = np.ones((2, self.electrodes[-1], self.electrodes[-1]))
        else:
            if len(gains) != 2:
                raise ValueError(
                    "Incorrect number of gains, need both T and K node gains"
                )

            if np.asarray(gains).shape[-1] != self.electrodes[-1]:
                raise ValueError("Incorrect number of gains")

            if (np.asarray(gains) == 0.0).any():
                raise ValueError("Cannot have zero gains")

            self.gains_per_pair = np.array(
                [
                    build_banded_matrix_from_vector(gains[0]),
                    build_banded_matrix_from_vector(gains[1]),
                ]
            )

    def apply_gain_correction(self, gain_correction_list: list):
        """

        Function to correct individual signal gains

        Args:
            gain_correction_list: list of lists of gains to be corrected of the form
                        [[gain_value, node_index, transmit_electrode, receive_electrode]]
                        node_index is 0 for tnode, 1 for knode
        """
        if gain_correction_list is not None:
            for (
                gain_value,
                node_index,
                transmit_electrode,
                receive_electrode,
            ) in gain_correction_list:
                self.gains_per_pair[
                    node_index,
                    transmit_electrode - 1,
                    receive_electrode - 1,
                ] = gain_value


class DeviceDataSynthetic(DeviceData):
    """
    Class to interface with synthetic data produced by the forward solver

    """

    @classmethod
    def create(cls, data_signals: np.ndarray, num_electrodes: int) -> "DeviceData":
        """
        Convert supplied dict to a DeviceData object
        """
        data = DeviceDataSynthetic()
        data.filename = ""
        data.metadata = None
        data.interval = 1

        data.electrodes = np.arange(1, 1 + num_electrodes)
        data.signals = data_signals
        return data

    def signal(self, transmit: int, receive: int) -> SignalSynthetic:
        """
        Retrieve the signal between given transmit and receive electrodes

        Args:
            transmit (int): Transmit electrode number
            receive (int): Receive electrode number

        Raises:
            ValueError: if the provided pair (transmit, receive) is not recognised
            AttributeError: if the signal data has not yet been retrieved.

        Returns:
            SignalSynthetic
        """
        if self.signals is not None:
            if transmit not in self.electrodes or receive not in self.electrodes:
                raise ValueError(
                    "Unrecognised (transmit, receive) pair " f"({(transmit, receive)})"
                )
            else:
                return SignalSynthetic.read(
                    self.signals,
                    transmit=transmit,
                    receive=receive,
                    interval=self.interval,
                )
        else:
            raise AttributeError("Have not read signals yet.")

    @cached_property
    def source_voltages(self) -> np.ndarray:
        """Numpy array of averages of source_voltage measurements"""
        return np.array(
            [
                [self.signal(i, j).vsources for j in self.electrodes]
                for i in self.electrodes
            ]
        )
