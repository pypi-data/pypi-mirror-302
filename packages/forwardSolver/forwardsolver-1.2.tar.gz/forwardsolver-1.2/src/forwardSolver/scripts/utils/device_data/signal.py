import json
import os
from functools import cached_property
from typing import Dict, Union, abstractmethod

import h5py
import matplotlib.pyplot as plt
import numpy as np

from forwardSolver.scripts.utils.constants import SECONDS_TO_MICROSECONDS
from forwardSolver.scripts.utils.json_coder import (
    CustomJsonDecoder,
    CustomJsonEncoder,
)
from forwardSolver.scripts.utils.logging import close_logger, get_logger

logger = get_logger(__name__)


def utr_idx(N: int, i: int, j: int) -> int:
    """Upper triangular index of an NxN matrix
    corresponding to element i,j of the matrix

    Args:
        N (int): square matrix shape
        i (int): row in [1, N]
        j (int): col in [1, N]

    Returns:
        int: upper-triangular index
    """
    if i > N or j > N or i < 1 or j < 1:
        raise LookupError(f"Index ({i},{j}) out of bounds for {N}x{N} matrix.")
    else:

        def _idx(k: int, n: int) -> int:
            return int(n * (N - 0.5 * (n + 1)) + k)

        return _idx(i - 1, j - 1) if i >= j else _idx(j - 1, i - 1)


class Signal:
    """
    Class to hold signal data for a single pair of transmit/receive electrodes

    Attributes:
    -----------
        time (np.ndarray): time points
        tnode (np.ndarray): T-node measurements (or source voltages for older boards)
        knode (np.ndarray): K-node measurements (signal read after the electrode)
    """

    _times: np.ndarray = np.array([])
    _tnodes: np.ndarray = np.array([])
    _knodes: np.ndarray = np.array([])

    raw_tnodes: np.ndarray = np.array([])
    raw_knodes: np.ndarray = np.array([])
    raw_vsources: np.ndarray = np.array([])
    good_repeats: np.ndarray = None
    datatype: str = None
    nreps: int = 1

    @classmethod
    def read(
        cls,
        data: Union[h5py.Dataset, np.ndarray],
        interval: int = 1,
        source: str = "oscilloscope",
        **kwargs,
    ) -> "Signal":
        """
        Read provided raw data as a Signal instance

        Args:
            data (h5py.Dataset, np.ndarray): data to read
            datatype (str): where the data comes from. Options are "HDF" or "ADC"
            interval (int): sampling rate to read the data
        """
        if isinstance(data, h5py.Dataset) and source == "oscilloscope":
            return SignalHDF.read(data, interval=interval, **kwargs)
        elif isinstance(data, np.ndarray) and source == "device":
            return SignalADC.read(data, interval=interval, **kwargs)
        else:
            raise TypeError(
                f"Unknown data type {type(data)} or 'source' keyword - choose 'oscilloscope' or 'device'"
            )

    @property
    def times(self) -> np.ndarray:
        """
        Time points for time-series
        """
        return self._times

    @times.setter
    def times(self, array: np.ndarray):
        self._times = array

    @cached_property
    def tnodes(self) -> np.ndarray:
        """T-node voltage time-series"""
        if self.nreps > 1:
            if self.good_repeats is None:
                self._tnodes = self.raw_tnodes.mean(axis=0)
            elif self.good_repeats == np.array([]):
                self._tnodes = np.ones(self.raw_tnodes[0].shape) * np.nan
            else:
                logger.debug(f"Using good repeat values: {self.good_repeats}")
                self._tnodes = self.raw_tnodes[self.good_repeats].mean(axis=0)
        else:
            self._tnodes = self.raw_tnodes

        return self._tnodes

    @cached_property
    def knodes(self) -> np.ndarray:
        """K-node voltage time-series"""
        if self.nreps > 1:
            if self.good_repeats is None:
                self._knodes = self.raw_knodes.mean(axis=0)
            elif self.good_repeats == np.array([]):
                self._knodes = np.ones(self.raw_knodes[0].shape) * np.nan
            else:
                logger.debug(f"Using good repeat values: {self.good_repeats}")
                self._knodes = self.raw_knodes[self.good_repeats].mean(axis=0)
        else:
            self._knodes = self.raw_knodes

        return self._knodes

    @cached_property
    def voltages(self) -> np.ndarray:
        """Array of all voltages in signal"""
        return np.array([self.tnodes, self.knodes])

    def __eq__(self, other: "Signal") -> bool:
        try:
            np.testing.assert_equal(self.to_dict(), other.to_dict())
        except AssertionError:
            return False
        return True

    def plot(
        self,
        interval: int = 1,
        ax: plt.Axes = None,
        plot_t_node: bool = True,
        plot_k_node: bool = True,
        t_node_label: str = "T Node",
        k_node_label: str = "K Node",
        **kwargs,
    ) -> plt.Axes:
        """
        Plot all voltages in the given repetition of the signal to given axis.
        If no axis is given, an axis will be created.

        Args:
            repetition (int, default = 0): which repetition of the signal to plot
            interval (int, default = 1): interval filter for the time-series
            average (bool, default = False): whether to average across all repetitions
            ax (plt.Axes, default = None): Axes to plot to
        """
        if ax is None:
            _, ax = plt.subplots()

        _time = SECONDS_TO_MICROSECONDS * self.times[::interval]

        if plot_t_node:
            _tnode = self.tnodes[::interval]
            ax.plot(_time, _tnode, label=t_node_label, **kwargs)

        if plot_k_node:
            _knode = self.knodes[::interval]
            ax.plot(_time, _knode, label=k_node_label, **kwargs)

        ax.set(xlabel=r"Time [$\mu$s]", ylabel="Voltage [V]")
        ax.legend()

        return ax.get_figure()

    @abstractmethod
    def to_dict(self) -> Dict:
        """Convert self to a dict"""
        return dict(
            times=self.times,
            tnodes=self.tnodes,
            knodes=self.knodes,
            nreps=self.nreps,
        )

    def to_json(self, fpath: Union[str, os.PathLike]):
        """Dump self to a JSON file"""
        with open(fpath, "w") as file:
            json.dump(self.to_dict(), file, cls=CustomJsonEncoder, indent=4)

    @classmethod
    def from_dict(cls, datadict: Dict) -> "Signal":
        if datadict["datatype"].lower() == "hdf":
            return SignalHDF.from_dict(datadict)
        elif datadict["datatype"].lower() == "adc":
            return SignalADC.from_dict(datadict)
        elif datadict["datatype"].lower() == "synth":
            return SignalSynthetic.from_dict(datadict)
        else:
            raise TypeError(
                f"Unknown data type {datadict['datatype'].lower()}"
            )

    @classmethod
    def from_json(cls, jsonfile: Union[str, os.PathLike]) -> "Signal":
        """Load data from a JSON file"""
        if os.path.isfile(jsonfile):
            with open(jsonfile, "r") as file:
                jsondata = json.load(file, cls=CustomJsonDecoder)
                return Signal.from_dict(jsondata)
        else:
            raise FileNotFoundError(f"File {jsonfile} could not be found")


class SignalHDF(Signal):
    """
    Class to interface with HDF datasets for a single pair of transmit/receive electrodes
    """

    raw_times: np.ndarray = np.array([])

    @classmethod
    def read(
        cls,
        data: h5py.Dataset,
        interval: int = 1,
        channel_time: int = 0,
        channel_tnode: int = 1,
        channel_knode: int = 2,
        channel_vsource: int = 3,
        pulse_param_index: int = 0,
        good_repeats: np.ndarray = None,
    ) -> "SignalHDF":
        """
        Read a HDF dataset for a single electrode pair

        Args:
            data (h5py.Dataset): HDF dataset for a single transmission
            channel_time (int): Oscilloscope channel for time data.
                                 Defaults to 0.
            channel_tnode (int): Oscilloscope channel for T node voltage data.
                                 Defaults to 1.
            channel_knode (int): Oscilloscope channel for K node voltage data.
                                 Defaults to 2.
            channel_vsource (int): Oscilloscope channel for source voltage data.
                                 Defaults to 3.
            pulse_param_index (int): Oscilloscope pulse index. Defaults to 0.
            interval (int): Interval at which to read the time-arrays. Defaults to 1.
            good_repeats (np.ndarray): list of repeat indices that have passed the
                                       SNR quality checks
        """
        if pulse_param_index > data.shape[0]:
            raise ValueError(
                f"Cannot read pulse index {pulse_param_index} "
                f"because max = {data.shape[0]}"
            )
        if not (data.shape[2] == 3 or data.shape[2] == 4):
            raise TypeError(
                f"Could not read HDF dataset of shape {data.shape}."
            )

        # Read the data
        data_array: np.ndarray = data[
            pulse_param_index, :, :, :: int(interval)
        ]

        # Create signal
        signal = SignalHDF()
        if data.shape[2] == 3:
            logger.info(
                "Reading P1000-006 board, setting vsource as tnode voltage."
            )
            # Assuming indices are 0 = time, 1 = vsource, 2 = tnode = knode
            signal.raw_vsources = data_array[:, 1, :]
            signal.raw_tnodes = data_array[:, 2, :]
            signal.raw_knodes = data_array[:, 2, :]
        elif data.shape[2] == 4:
            # Assuming indices are 0 = time, 1 = tnode, 2 = knode, 3 = vsource
            signal.raw_tnodes = data_array[:, channel_tnode, :]
            signal.raw_knodes = data_array[:, channel_knode, :]
            signal.raw_vsources = data_array[:, channel_vsource, :]
        else:
            raise TypeError(
                f"Could not read HDF dataset of shape {data.shape}."
            )

        signal.raw_times = data_array[:, channel_time, :]
        signal.nreps = data_array.shape[0]
        signal.good_repeats = good_repeats
        signal.datatype = "hdf"
        return signal

    @cached_property
    def raw_voltages(self) -> np.ndarray:
        """Array of all voltages in signal"""
        return np.array([self.raw_tnodes, self.raw_knodes, self.raw_vsources])

    @cached_property
    def times(self) -> np.ndarray:
        """Time array for time-series"""
        if self.nreps > 1:
            if self.good_repeats is None:
                self._times = self.raw_times.mean(axis=0)
            elif self.good_repeats == np.array([]):
                self._times = np.ones(self.raw_times[0].shape) * np.nan
            else:
                logger.debug(f"Using good repeat values: {self.good_repeats}")
                self._times = self.raw_times[self.good_repeats].mean(axis=0)
        else:
            self._times = self.raw_times

        return super().times

    @cached_property
    def vsources(self) -> np.ndarray:
        """Source voltage time-series"""
        if self.nreps > 1:
            if self.good_repeats is None:
                return self.raw_vsources.mean(axis=0)
            elif self.good_repeats == np.array([]):
                return np.ones(self.raw_vsources[0].shape) * np.nan
            else:
                logger.debug(f"Using good repeat values: {self.good_repeats}")
                return self.raw_vsources[self.good_repeats].mean(axis=0)
        else:
            return self.raw_vsources

    def plot(
        self,
        repetition: int = 0,
        interval: int = 1,
        average: bool = False,
        ax: plt.Axes = None,
        plot_t_node: bool = True,
        plot_k_node: bool = True,
        plot_source: bool = True,
        t_node_label: str = "T Node",
        k_node_label: str = "K Node",
        source_label: str = "V source",
    ) -> plt.Figure:
        """
        Plot all voltages in the given repetition of the signal to given axis.
        If no axis is given, an axis will be created.

        Args:
            repetition (int, default = 0): which repetition of the signal to plot
            interval (int, default = 1): interval filter for the time-series
            average (bool, default = False): whether to average across all repetitions
            ax (plt.Axes, default = None): Axes to plot to
        """
        if ax is None:
            _, ax = plt.subplots()

        if average or self.nreps <= 1:
            _time = SECONDS_TO_MICROSECONDS * self.times[::interval]
            _tnode = self.tnodes[::interval]
            _knode = self.knodes[::interval]
            _vsource = self.vsources[::interval]
        else:
            _time = (
                SECONDS_TO_MICROSECONDS
                * self.raw_times[repetition, ::interval]
            )
            _tnode = self.raw_tnodes[repetition, ::interval]
            _knode = self.raw_knodes[repetition, ::interval]
            _vsource = self.raw_vsources[repetition, ::interval]

        if plot_t_node:
            ax.plot(_time, _tnode, label=t_node_label)
        if plot_k_node:
            ax.plot(_time, _knode, label=k_node_label)
        if plot_source:
            ax.plot(_time, _vsource, label=source_label)

        ax.set(xlabel=r"Time [$\mu$s]", ylabel="Voltage [V]")
        ax.legend()
        return ax.get_figure()

    def to_dict(self) -> Dict:
        return dict(
            datatype="hdf",
            raw_times=self.raw_times,
            raw_tnodes=self.raw_tnodes,
            raw_knodes=self.raw_knodes,
            raw_vsources=self.raw_vsources,
            nreps=self.nreps,
            good_repeats=self.good_repeats,
        )

    @classmethod
    def from_dict(cls, datadict: Dict) -> "SignalHDF":
        signal = SignalHDF()
        signal.raw_times = np.asarray(datadict["raw_times"])
        signal.raw_tnodes = np.asarray(datadict["raw_tnodes"])
        signal.raw_knodes = np.asarray(datadict["raw_knodes"])
        signal.raw_vsources = np.asarray(datadict["raw_vsources"])
        signal.nreps = int(datadict["nreps"])
        signal.datatype = "hdf"
        signal.good_repeats = datadict["good_repeats"]
        return signal


class SignalADC(Signal):
    """
    Class to interface with ADC datasets for a single pair of transmit/receive electrodes
    """

    @classmethod
    def read(
        cls,
        data_array: np.ndarray,
        interval: int = 1,
        pulse_duration: float = 75e-6,
        good_repeats: np.ndarray = None,
        motor_on: bool = False,
        rotation_id: int = 0,
        gains: tuple[float, float] = (1.0, 1.0),
        average_offset_to_zero: bool = True,
        offset_measure_window: tuple[float, float] = (0.5e-6, 1.5e-6),
    ) -> "SignalADC":
        """
        Read a ADC dataset for a single electrode pair

        Args:
            data_array (np.array): converted HDF dataset for a single transmission
            interval (int): Interval at which to read the time-arrays. Defaults to 1.
            pulse_duration (float): total duration of the measured signal.
                                    Defaults to 75e-6.
            good_repeats (np.ndarray): list of repeat indices that have passed the
                                       SNR quality checks
            motor_on (bool): flag for utilising rotations as repeats. Defaults to False.
            rotation_id (int): if motor_on is True, choose which rotation to process
            gains (tuple[float, float]): gain values to be applied to T and K nodes.
                                         Defaults to (1.0, 1.0)
            average_offset_to_zero (bool): whether to adjust the vertical offset to zero.
                                           Defaults to True
            offset_measure_window (tuple[float, float]): window which will be used to
                        perform vertical shift. Any signal before the first instant is
                        discarded, and the signal between first and second instant is
                        averaged and subtracted. Defaults to (0.5us, 1.5us).
        """
        assert (
            len(gains) == 2
        ), "Only two gain values (T/K) can be passed for a single signal"
        assert (gains[0] != 0) & (
            gains[1] != 0
        ), "Gains for signal cannot be zero"
        if average_offset_to_zero:
            if offset_measure_window is not None:
                # Check two instants have been passed
                assert len(offset_measure_window) == 2, (
                    "Offset measure window not of correct length "
                    f"({len(offset_measure_window)} != 2)"
                )
                # Check offset_measure_window has valid data
                assert isinstance(
                    offset_measure_window[0], float
                ) and isinstance(
                    offset_measure_window[1], float
                ), "Offset measure window can only contain floats"
                # Check second instant is after first
                assert (
                    offset_measure_window[1] >= offset_measure_window[0]
                ), "Offset measure window must have width >= 0"
            else:
                offset_measure_window = (-np.inf, -np.inf)

        # Read the data
        num_repeats, _, num_timepoints = data_array.shape
        # Create signal
        signal = SignalADC()

        signal.times = np.linspace(0, pulse_duration, num_timepoints)[
            ::interval
        ]

        if motor_on:
            signal.raw_tnodes = (
                data_array[rotation_id, 0, ::interval] / gains[0]
            )
            signal.raw_knodes = (
                data_array[rotation_id, 1, ::interval] / gains[1]
            )

            if average_offset_to_zero and (offset_measure_window is not None):
                # Signals may not exactly all start at the same level so subtract the
                # average of the first few time points as the y-axis offset.
                # Average using signal between given time 1 and given time 2
                offset_window = np.logical_and(
                    signal.times >= offset_measure_window[0],
                    signal.times <= offset_measure_window[1],
                )
                signal.raw_tnodes -= np.average(
                    signal.raw_tnodes[offset_window]
                )
                signal.raw_knodes -= np.average(
                    signal.raw_knodes[offset_window]
                )

            signal.nreps = 1

        else:
            signal.raw_tnodes = data_array[:, 0, ::interval] / gains[0]
            signal.raw_knodes = data_array[:, 1, ::interval] / gains[1]

            if average_offset_to_zero:
                # Signals may not exactly all start at the same level so subtract the
                # average of the first few time points as the y-axis offset.

                # Average using signal between given time 1 and given time 2
                offset_window = np.logical_and(
                    np.repeat(
                        signal.times[np.newaxis, :],
                        repeats=num_repeats,
                        axis=0,
                    )
                    >= offset_measure_window[0],
                    np.repeat(
                        signal.times[np.newaxis, :],
                        repeats=num_repeats,
                        axis=0,
                    )
                    <= offset_measure_window[1],
                )
                offset_tnode = signal.raw_tnodes[offset_window]
                offset_tnode = offset_tnode.reshape(num_repeats, -1)

                _, offset_window_length = offset_tnode.shape

                if offset_window_length > 0:
                    offset_knode = signal.raw_knodes[offset_window]
                    offset_knode = offset_knode.reshape(num_repeats, -1)

                    signal.raw_tnodes -= np.average(offset_tnode, axis=1)[
                        :, np.newaxis
                    ]
                    signal.raw_knodes -= np.average(offset_knode, axis=1)[
                        :, np.newaxis
                    ]

            signal.nreps = num_repeats

        signal.good_repeats = good_repeats
        signal.datatype = "adc"
        return signal


class SignalSynthetic(Signal):
    """
    Interface for synthetic data created from SolverForward
    """

    _vsources: np.ndarray
    tnodes: np.ndarray
    knodes: np.ndarray

    @classmethod
    def read(
        cls,
        data: np.ndarray,
        transmit: int,
        receive: int,
        interval: int = 1,
    ) -> "SignalSynthetic":
        """
        Read single electrode pair data from numpy array produced by forward solver
        Data should have the format
        [time, vsource, tnode_11, knode_11, tnode_12, knode_12, ...]

        Args:
            data (np.ndarray): data to be read
            transmit (int): transmit electrode
            receive (int): receive electrode
            interval (int, optional): subsampling interval to read the time-series.
                                      Defaults to 1.

        Returns:
            SignalSynthetic
        """
        M, num_timepoints = data.shape
        if M < 4:
            raise ValueError(
                "Incomplete data. Should have at least four columns, "
                "corresponding to [time, vsource, tnode, knode]."
            )

        num_electrodes = int(np.sqrt(0.5 * M - 1))
        num_timepoints = num_timepoints // interval

        # index on flattened num_electrodes x num_electrodes array
        idx = num_electrodes * (transmit - 1) + (receive - 1)

        signal = SignalSynthetic()
        signal.times = data[0, ::interval]
        signal.vsources = data[1, ::interval]
        signal.tnodes = data[2 + 2 * idx, ::interval]
        signal.knodes = data[3 + 2 * idx, ::interval]

        signal.nreps = 1
        signal.datatype = "synth"

        return signal

    @property
    def vsources(self) -> np.ndarray:
        return self._vsources

    @vsources.setter
    def vsources(self, array: np.ndarray):
        self._vsources = array

    def to_dict(self) -> Dict:
        return dict(
            times=self.times,
            tnodes=self.tnodes,
            knodes=self.knodes,
            vsources=self.vsources,
            nreps=self.nreps,
            datatype="synth",
        )

    @classmethod
    def from_dict(cls, datadict: Dict) -> "SignalADC":
        signal = SignalADC()
        for k, v in datadict.items():
            setattr(signal, k, v)
        return signal

    def plot(
        self, interval: int = 1, ax: plt.Axes = None, **kwargs
    ) -> plt.Axes:
        """
        Plot all voltages in the given repetition of the signal to given axis.
        If no axis is given, an axis will be created.

        Args:
            interval (int, default = 1): interval filter for the time-series
            average (bool, default = False): whether to average across all repetitions
            ax (plt.Axes, default = None): Axes to plot to
        """
        if ax is None:
            _, ax = plt.subplots()

        _time = SECONDS_TO_MICROSECONDS * self.times[::interval]
        _tnode = self.tnodes[::interval]
        _knode = self.knodes[::interval]
        _vsource = self.vsources[::interval]

        ax.plot(_time, _tnode, label="T Node")
        ax.plot(_time, _knode, label="K Node")
        ax.plot(_time, _vsource, label="V source")

        ax.set(xlabel=r"Time [$\mu$s]", ylabel="Voltage [V]")
        ax.legend()

        return ax.get_figure()


close_logger(logger)
