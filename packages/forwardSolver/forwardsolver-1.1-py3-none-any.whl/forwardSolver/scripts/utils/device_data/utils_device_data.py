import json
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np

from forwardSolver.scripts.utils.constants import ROOT_DIR
from forwardSolver.scripts.utils.device_data.device_data import (
    DeviceData,
    DeviceDataHDF,
)
from forwardSolver.scripts.utils.device_data.models.noise_data import (
    MeanData,
    NoiseData,
)
from forwardSolver.scripts.utils.logging import close_logger, get_logger

logger = get_logger(__name__)


def check_max_transmit_voltage(
    *,
    device_data: DeviceData,
    threshold: float = 2.4,
    plot_max_voltage: bool = True,
):
    """
    Check the maximum transmit voltage in the data and report any anomalies.
    This function iterates through the transmit and receive electrodes in the
    provided `device_data`, calculates the maximum voltage for each repeat, and
    checks if any of these maximum voltages fall below the specified `threshold`.
    If any voltages are below the threshold, a warning is logged. Optionally,
    the function can also plot the maximum voltages with error bars.
    Parameters:
    -----------
    device_data : DeviceData
        An instance of DeviceData containing the electrodes and signal data.
    threshold : float, optional
        The minimum acceptable voltage threshold. Default is 2.4 volts.
    plot_max_voltage : bool, optional
        If True, a plot of the maximum voltages with error bars will be generated.
        Default is True.
    Returns:
    --------
    None
    Logs:
    -----
    Logs warnings if any maximum voltages are below the specified threshold.
    Plots:
    ------
    If `plot_max_voltage` is True, generates a plot showing the average maximum
    voltage for each transmit-receive pair with error bars, and a line indicating
    the minimum voltage threshold.
    """

    logger.info("Starting check: max_transmit_voltage")

    # dict to store result TxRx: (mean, std)
    result = {}
    for transmit in device_data.electrodes:
        for receive in device_data.electrodes:
            # get maximum voltage for each repeat
            max_volts = np.max(
                device_data.signal(transmit, receive).raw_vsources, axis=1
            )

            result[f"T{transmit}R{receive}"] = (
                np.mean(max_volts),
                np.std(max_volts),
            )

            if (max_volts < threshold).any():
                indices = (max_volts < threshold).nonzero()
                logger.warn(
                    "Unexpected behaviour for"
                    f" T{transmit}R{receive}-repeats({indices})."
                    f" Transmit pulse voltage is too low:  "
                    f"{max_volts[indices]} < {threshold}."
                )

    if plot_max_voltage:
        num_elec = len(device_data.electrodes)

        fig, ax = plt.subplots(1, 1)
        ax.errorbar(
            x=list(result.keys()),
            y=[v[0] for v in list(result.values())],
            yerr=[v[1] for v in list(result.values())],
            fmt="b",
            ecolor="cornflowerblue",
            label="Maximum voltage Data",
        )
        ax.plot(
            [threshold] * len(result.keys()),
            "r-",
            label="minimum voltage threshold",
        )
        ax.set_ylabel("Average Maximum Voltage for Transmit Over Repeats [Volts]")
        ax.set_xticks(ax.get_xticks()[::num_elec])
        ax.tick_params(axis="x", rotation=90)
        ax.grid(visible=True, axis="both")
        ax.legend()
        fig.tight_layout()


def check_transmit_voltages_are_highest(
    *,
    device_data: DeviceData,
    threshold_transmit: float = 0.9,
    noise_threshold: float = 0.01,
):
    """
    This function verifies that the transmit voltages are the highest in each set of
    data provided by the `device_data`. It compares the transmit and receive voltages
    within a specified time window determined by `threshold_transmit`, which is a
    fraction of the maximum voltage. The function ensures that the voltage on the
    receive electrodes does not exceed the voltage on the transmit electrodes by more
    than the `noise_threshold` (in volts).
    Parameters:
    -----------
    device_data : DeviceData
        The data object containing the voltage signals for the device.
    threshold_transmit : float, optional
        A fraction of the maximum voltage used to determine the time window for
        comparison (default is 0.9).
    noise_threshold : float, optional
        The maximum allowable voltage difference between transmit and receive
        electrodes (default is 0.01).
    Returns:
    --------
    None
        This function does not return any value. It logs a warning if the receive
        voltages exceed the transmit voltages within the specified thresholds.
    """

    # High threshold is chosen because there is a small delay between vsource and knode.
    # Lower threshold would mean that there is a small amount of time where the receive
    # voltage can be higher than the transmit.
    logger.info("Starting check: transmit_voltages_are_highest")

    for transmit in device_data.electrodes:
        for receive in device_data.electrodes:
            max_transmit_voltage = np.max(
                device_data.signal(transmit, receive).raw_vsources
            )
            time_window = (
                device_data.signal(transmit, receive).raw_vsources
                > threshold_transmit * max_transmit_voltage
            )

            repeats = device_data.signal(transmit, receive).raw_vsources.shape[0]
            for repeat in range(repeats):
                is_transmit_highest = np.all(
                    (
                        np.abs(
                            device_data.signal(transmit, receive).raw_vsources[repeat]
                        )[time_window[repeat]]
                        - np.abs(
                            device_data.signal(transmit, receive).raw_knodes[repeat]
                        )[time_window[repeat]]
                        > noise_threshold
                    )
                )
                if not is_transmit_highest:
                    logger.warn(
                        "Unexpected behaviour for"
                        f" T{transmit}R{receive}-repeat{repeat}. Receive voltages"
                        " exceed transmit voltages."
                    )


def check_noise_levels(
    *,
    device_data: DeviceData,
    noise_threshold: float = 6,
    plot_noise: bool = True,
    noise_type: str = "snr",
    plot_title=None,
) -> dict:
    """
    Check that the repeat measurements don't differ by more than the `noise_threshold`
    (V) from the average of all repeats. If `plot_noise` is set to `True`, a plot will
    be generated. `noise_type` is either 'rms or 'snr'.
    Returns a dict of all noise levels

    Parameters:
    -----------
    device_data : DeviceData
        The device data containing the measurements.
    noise_threshold : float, optional
        The threshold value for noise level comparison, by default 6.
    plot_noise : bool, optional
        If True, a plot of the noise levels will be generated, by default True.
    noise_type : str, optional
        The type of noise to check, either 'rms' or 'snr', by default "snr".
    plot_title : str, optional
        The title for the noise plot, by default None.
    Returns:
    --------
    dict
        A dictionary containing the noise levels for 'v_tnode', 'v_knode', and if applicable, 'v_source'.
        Also includes 'all_channels' which stores the good and bad repeats for all runs.
    Raises:
    -------
    NotImplementedError
        If an unrecognized `noise_type` is provided.
    Notes:
    ------
    - The function logs the start of the noise level check.
    - It iterates over all electrode pairs in `device_data` to perform noise analysis.
    - If `plot_noise` is True, it generates a plot of the noise levels.
    """

    logger.info("Starting check: noise_levels")

    if noise_type.lower() not in ["rms", "snr"]:
        raise NotImplementedError("Unrecognised noise_type. Please use rms or snr.")

    # list to store results (NoiseData)
    result_vsource = []
    result_knode = []
    result_tnode = []
    num_elec = len(device_data.electrodes)

    for transmit in device_data.electrodes:
        for receive in device_data.electrodes:
            if isinstance(device_data, DeviceDataHDF):
                result_vsource.append(
                    voltage_noise_analysis(
                        voltages=device_data.signal(transmit, receive).raw_vsources,
                        noise_threshold=noise_threshold,
                        transmit=transmit,
                        receive=receive,
                        noise_type=noise_type,
                    )
                )

            result_knode.append(
                voltage_noise_analysis(
                    voltages=device_data.signal(transmit, receive).raw_knodes,
                    noise_threshold=noise_threshold,
                    transmit=transmit,
                    receive=receive,
                    noise_type=noise_type,
                )
            )
            result_tnode.append(
                voltage_noise_analysis(
                    voltages=device_data.signal(transmit, receive).raw_tnodes,
                    noise_threshold=noise_threshold,
                    transmit=transmit,
                    receive=receive,
                    noise_type=noise_type,
                )
            )

    if plot_noise:
        if isinstance(device_data, DeviceDataHDF):
            fig, ax = plt.subplots(1, 3, figsize=(18, 5))
            plot_noise_result(
                noise_threshold,
                result_vsource,
                num_elec,
                ax[2],
                "v source",
                noise_type=noise_type,
            )
        else:
            fig, ax = plt.subplots(1, 2, figsize=(12, 5))

        plot_noise_result(
            noise_threshold,
            result_knode,
            num_elec,
            ax[0],
            "k node",
            noise_type=noise_type,
        )
        plot_noise_result(
            noise_threshold,
            result_tnode,
            num_elec,
            ax[1],
            "t node",
            noise_type=noise_type,
        )
        fig.tight_layout()

        fig.suptitle(plot_title)

    result_dict = {
        "v_tnode": result_tnode,
        "v_knode": result_knode,
    }
    if isinstance(device_data, DeviceDataHDF):
        result_dict["v_source"] = result_vsource

    # Store the good and bad repeats for all runs
    all_channels = join_bad_runs(result_dict)
    result_dict["all_channels"] = all_channels

    return result_dict


def plot_noise_result(
    noise_threshold: float,
    result_list: List[NoiseData],
    num_elec: int,
    ax: plt.Axes,
    title: str,
    noise_type: str = "snr",
):
    """
    Helper function to plot noise data.
    `noise_type` is either 'rms or 'snr'

    Parameters:
    noise_threshold (float): The threshold value for noise to be plotted as a red line.
    result_list (List[NoiseData]): A list of NoiseData objects containing noise measurement results.
    num_elec (int): Number of electrodes, used to set x-tick intervals.
    ax (plt.Axes): Matplotlib Axes object where the plot will be drawn.
    title (str): Title of the plot.
    noise_type (str, optional): Type of noise data to plot, either 'rms' or 'snr'. Defaults to 'snr'.
    Raises:
    NotImplementedError: If an unrecognized noise_type is provided.
    Returns:
    None
    """
    if noise_type.lower() == "rms":
        ylabel = "Average RMSE Over Repeats [Volts]"
        yvals = [v.rms_noise.mean for v in result_list]
        yerrs = [v.rms_noise.std for v in result_list]
    elif noise_type.lower() == "snr":
        ylabel = "SNR"
        yvals = [v.snr.mean for v in result_list]
        yerrs = [v.snr.std for v in result_list]
    else:
        raise NotImplementedError("Unrecognised noise_type. Please use rms or snr.")

    ax.errorbar(
        x=[f"T{v.transmit}R{v.receive}" for v in result_list],
        y=yvals,
        yerr=yerrs,
        fmt="b",
        ecolor="cornflowerblue",
        label="Noise Data",
    )
    ax.plot([noise_threshold] * len(result_list), "r-", label="noise threshold")
    ax.set_ylabel(ylabel)
    ax.set_xticks(ax.get_xticks()[::num_elec])
    ax.tick_params(axis="x", rotation=90)
    ax.grid(visible=True, axis="both")
    ax.legend()
    ax.set_title(title)


def voltage_noise_analysis(
    *,
    voltages: np.ndarray,
    noise_threshold: float,
    transmit: int,
    receive: int,
    noise_type: str,
) -> NoiseData:
    """
    Helper function to take voltage data and calculate means and RMS across repeats.
    Populates `result` dictionary with values.
    Parameters:
    -----------
    voltages : np.ndarray
        A 2D array where each row represents a repeat and each column represents a voltage measurement.
    noise_threshold : float
        The threshold value to determine poor and good repeats based on noise levels.
    transmit : int
        The transmit channel identifier.
    receive : int
        The receive channel identifier.
    noise_type : str
        The type of noise analysis to perform. Can be 'snr' for Signal-to-Noise Ratio or 'rms' for Root Mean Square.
    Returns:
    --------
    NoiseData
        An object containing the analysis results, including transmit and receive identifiers, RMS noise, SNR,
        and arrays of indices for poor and good repeats.
    Raises:
    -------
    NotImplementedError
        If the provided noise_type is not recognized.
    Notes:
    ------
    - If noise_type is 'snr', the function calculates the Signal-to-Noise Ratio and identifies poor repeats where
      the SNR is below the noise_threshold.
    - If noise_type is 'rms', the function calculates the Root Mean Square noise and identifies poor repeats where
      the RMS noise is above the noise_threshold.
    - Logs a warning if any poor repeats are found.
    """
    averaged_signal = np.mean(voltages, axis=0)

    residuals = np.abs(voltages - averaged_signal)
    rms = np.sqrt(np.mean(np.square(residuals), axis=1))

    snr = 20 * np.log10(averaged_signal.std() / residuals.std(axis=1))

    if noise_type.lower() == "snr":
        noise = snr
        poor_repeats = np.flatnonzero(noise < noise_threshold)
        good_repeats = np.flatnonzero(noise >= noise_threshold)
        if len(poor_repeats) > 0:
            logger.warn(
                f"Unexpected behaviour for T{transmit}R{receive}-repeats"
                f"({poor_repeats}). SNR below threshold level {noise_threshold}."
            )

    elif noise_type.lower() == "rms":
        noise = rms
        poor_repeats = np.flatnonzero(noise > noise_threshold)
        good_repeats = np.flatnonzero(noise <= noise_threshold)
        if len(poor_repeats) > 0:
            logger.warn(
                f"Unexpected behaviour for T{transmit}R{receive}-repeats"
                f"({poor_repeats}). Noise above threshold level {noise_threshold}."
            )
    else:
        raise NotImplementedError("Unrecognised noise_type. Please use rms or snr.")

    return NoiseData(
        transmit=transmit,
        receive=receive,
        rms_noise=MeanData(np.mean(rms), np.std(rms)),
        snr=MeanData(np.mean(snr), np.std(snr)),
        poor_repeats=np.array(poor_repeats),
        good_repeats=np.array(good_repeats),
    )


def mask_poor_repeats(data: List[NoiseData]) -> dict:
    """
    Loop through all noise data and save the positions of good repeats

    Args:
        data (List[NoiseData]): A list of NoiseData objects to be processed.

    Returns:
        dict: A dictionary mapping "T{transmit}R{receive}" to the good repeats.
    """
    return {f"T{d.transmit}R{d.receive}": d.good_repeats for d in data}


def join_bad_runs(d: Dict[str, List[NoiseData]]) -> List[NoiseData]:
    """
    Discard a repeat if any of the voltage channels are too noisy.
    Return a list of good and poor repeats depending if any of the voltages had a bad
    repeat.
    e.g. if, for repeat 2, v_source and v_tnode are above the noise threshold but
    v_knode isn't then repeat 2 is discarded
    Args:
        d (Dict[str, List[NoiseData]]): A dictionary where keys are voltage channel
        names (e.g., 'v_source', 'v_tnode', etc.) and values are lists of `NoiseData`
        objects corresponding to each channel.
    Returns:
        List[NoiseData]: A list of `NoiseData` objects where each object contains
        good repeats that are not noisy in any channel and poor repeats that are
        noisy in at least one channel.
    """

    keys = list(d.keys())

    new_list = []
    num_elements = len(d[keys[0]])

    for i in range(num_elements):
        good_runs = np.unique(np.concatenate([d[k][i].good_repeats for k in keys]))
        bad_runs = np.unique(np.concatenate([d[k][i].poor_repeats for k in keys]))
        # new list will only contain good runs if none of the voltage sources
        # are too noisy
        new_list.append(
            NoiseData(
                transmit=d[keys[0]][i].transmit,
                receive=d[keys[0]][i].receive,
                good_repeats=np.array(good_runs[~np.isin(good_runs, bad_runs)]),
                poor_repeats=np.array(bad_runs),
            )
        )

    return new_list


def mask_unusable_capacitance_by_noise(
    noise: List[NoiseData], capacitances: np.ndarray
) -> np.ndarray:
    """
    Return a new matrix copy of `capacitances` which has poor (noisy) data set to NaN.
    Parameters:
    noise (List[NoiseData]): A list of NoiseData objects, each containing information about
                             good and bad repeats for specific transmit and receive pairs.
    capacitances (np.ndarray): A 2D numpy array representing the capacitance values.
    Returns:
    np.ndarray: A new 2D numpy array with the same shape as `capacitances`, where the
                capacitance values corresponding to noisy data are set to NaN.
    """

    result = np.zeros(capacitances.shape)

    for noise_data in noise:
        if len(noise_data.good_repeats) > 0:
            result[noise_data.transmit - 1, noise_data.receive - 1] = 1

    cap = np.copy(capacitances)
    cap[result == 0] = np.nan
    return cap


def mask_unusable_capacitances_by_span(
    max_span: int, capacitances: np.ndarray
) -> np.ndarray:
    """
    Return a new matrix copy of `capacitances` which has far-span data set to NaN.

    Parameters:
    max_span (int): The maximum allowable span between indices. Elements with a span greater than this value will be set to NaN.
    capacitances (np.ndarray): A 2D numpy array representing the capacitances.
    Returns:
    np.ndarray: A new 2D numpy array with the same shape as `capacitances`, where elements with a span greater than `max_span` are set to NaN.
    """

    cap = np.copy(capacitances)

    for i in range(capacitances.shape[0]):
        for j in range(capacitances.shape[1]):
            if np.abs(i - j) > max_span:
                cap[i, j] = np.nan
    return cap


def check_transmit_time_spread(
    *,
    device_data: DeviceData,
    threshold_transmit: float = 0.9,
    expected_window: List[float] = [2.05, 2.055],
    plot_times: bool = True,
):
    """
    Check the average time it takes for the transmit signals to reach
    `threshold_transmit` * maximum voltage. Also calculate the standard deviation in
    these times across repeats. Return a warning if the trigger times are outside of
    the `expected_window` (us)

    Parameters:
    -----------
    device_data : DeviceData
        An instance of DeviceData containing the signal data for the device.
    threshold_transmit : float, optional
        The threshold as a fraction of the maximum voltage to determine the trigger time.
        Default is 0.9.
    expected_window : List[float], optional
        The expected time window (in microseconds) within which the transmit signals should
        reach the threshold voltage. Default is [2.05, 2.055].
    plot_times : bool, optional
        If True, plot the average transmit times with error bars. Default is True.
    Returns:
    --------
    None
    Logs:
    -----
    Logs warnings if the trigger times are outside of the `expected_window`.
    Plots:
    ------
    If `plot_times` is True, plots the average transmit times with error bars and the expected
    window bounds.
    """

    logger.info("Starting check: transmit_time_spread")

    # dict to store result TxRx: (mean, std)
    result = {}

    num_elec = len(device_data.electrodes)

    for transmit in device_data.electrodes:
        for receive in device_data.electrodes:
            voltages_receive = device_data.signal(transmit, receive).raw_vsources
            times = device_data.signal(transmit, receive).raw_times
            repeats = device_data.signal(transmit, receive).raw_vsources.shape[0]
            trigger_times = []
            for repeat in range(repeats):
                max_transmit_voltage = np.max(voltages_receive[repeat])
                trigger_time = times[repeat][
                    np.argmax(
                        voltages_receive[repeat]
                        > threshold_transmit * max_transmit_voltage
                    )
                ]
                trigger_time *= 1e6  # s -> us
                trigger_times.append(trigger_time)

            trigger_times = np.array(trigger_times)
            if (trigger_times < expected_window[0]).any():
                logger.warn(
                    "Unexpected behaviour for"
                    f" T{transmit}R{receive}-repeats"
                    f"({(trigger_times < expected_window[0]).nonzero()})."
                    " Transmit pulse too early.Expected transmit voltage threshold to"
                    f" be reached within range {expected_window}us, instead threshold"
                    " passed at time"
                    f" {trigger_times[trigger_times < expected_window[0]]}us."
                )
            if (trigger_times > expected_window[1]).any():
                logger.warn(
                    "Unexpected behaviour for"
                    f" T{transmit}R{receive}-repeats"
                    f"({(trigger_times > expected_window[1]).nonzero()})."
                    " Transmit pulse too late.Expected transmit voltage threshold to"
                    f" be reached within range {expected_window}us, instead threshold"
                    " passed at time"
                    f" {trigger_times[trigger_times > expected_window[1]]}us."
                )

            result[f"T{transmit}R{receive}"] = (
                np.mean(trigger_times),
                np.std(trigger_times),
            )

    if plot_times:
        fig, ax = plt.subplots(1, 1)
        ax.errorbar(
            x=list(result.keys()),
            y=[v[0] for v in list(result.values())],
            yerr=[v[1] for v in list(result.values())],
            fmt="b",
            ecolor="cornflowerblue",
            label="Mean Transmit Time",
        )
        ax.plot([expected_window[0]] * len(result.keys()), "r-", label="bounds")
        ax.plot([expected_window[1]] * len(result.keys()), "r-")
        ax.set_ylabel(r"Average Transmit Time Spread [$\mu$s]")
        ax.set_xticks(ax.get_xticks()[::num_elec])
        ax.tick_params(axis="x", rotation=90)
        ax.grid(visible=True, axis="both")
        fig.tight_layout()
        ax.legend()


def check_voltage_dropoff(
    *,
    device_data: DeviceData,
    threshold_transmit: float = 0.9,
    plot_integrals: bool = True,
):
    """
    Check that the voltages on electrodes reduce as the electrodes get further from the
    transmit. `threshold_transmit` is the fraction of the maximum transmit voltage used
    to determine the integration window. Return a warning if not the case.

    Args:
        device_data (DeviceData): An instance of DeviceData containing electrode and signal information.
        threshold_transmit (float, optional): The fraction of the maximum transmit voltage used to determine the integration window. Defaults to 0.9.
        plot_integrals (bool, optional): If True, plots the mean T-node and K-node voltages for each repeat. Defaults to True.
    Returns:
        None
    Raises:
        None
    Logs:
        Info: Starting check: voltage_dropoff
        Warn: Unexpected behaviour for T{transmit electrode}-repeat{repeat}. T-node voltages not decreasing with span.
        Warn: Unexpected behaviour for T{transmit electrode}-repeat{repeat}. K-node voltages not decreasing with span.
    """

    logger.info("Starting check: voltage_dropoff")

    # High threshold is chosen because there is a small delay between vsource and knode.
    # Lower threshold would mean that there is a small amount of time where the receive
    # voltage can be higher than the transmit.
    num_electrodes = len(device_data.electrodes)

    # Get number of repeats in dataset.
    # Assumes all electrode measurements have same number of repeats
    repeats = device_data.signal(
        device_data.electrodes[0], device_data.electrodes[0]
    ).raw_vsources.shape[0]
    for repeat in range(repeats):
        means_t = np.ones((num_electrodes, num_electrodes)) * np.nan
        means_k = np.ones((num_electrodes, num_electrodes)) * np.nan
        for count_trans, transmit in enumerate(device_data.electrodes):
            for count_rec, receive in enumerate(device_data.electrodes):
                # Get integration window
                max_transmit_voltage = np.max(
                    device_data.signal(transmit, receive).raw_vsources[repeat]
                )
                time_window = (
                    device_data.signal(transmit, receive).raw_vsources[repeat]
                    > threshold_transmit * max_transmit_voltage
                )

                mean_voltage_t_node = np.mean(
                    device_data.signal(transmit, receive).raw_tnodes[repeat][
                        time_window
                    ]
                )
                mean_voltage_k_node = np.mean(
                    device_data.signal(transmit, receive).raw_knodes[repeat][
                        time_window
                    ]
                )

                means_t[count_trans, count_rec] = mean_voltage_t_node
                means_k[count_trans, count_rec] = mean_voltage_k_node

        if plot_integrals:
            fig, ax = plt.subplots(2, 1)
            fig.suptitle(f"Repeat - {repeat+1}")
            fig.tight_layout()

        for count, row in enumerate(means_t):
            # check right side decreasing from transmit to end receive
            right_side_desc = np.all(row[count:-1] >= row[count + 1 :])  # noqa: E203
            # check left side increasing from receive to transmit
            left_side_asc = np.all(row[:count] <= row[1 : count + 1])  # noqa: E203

            if plot_integrals:
                labels = [f"R{x}" for x in range(1, len(row) + 1)]
                ax[0].errorbar(x=labels, y=row, label=f"T{count+1}")
                ax[0].set_ylabel("Mean T-node voltage")
                ax[0].set_xlabel("Receive Electrode")
                ax[0].tick_params(axis="x", rotation=90)
                ax[0].grid(visible=True, axis="both")
                ax[0].legend(bbox_to_anchor=(1.04, 1), loc="center left")

            if not right_side_desc or not left_side_asc:
                logger.warn(
                    "Unexpected behaviour for"
                    f" T{device_data.electrodes[count]}-repeat{repeat}. "
                    "T-node voltages not decreasing with span."
                )

        for count, row in enumerate(means_k):
            # check right side decreasing from transmit to end receive
            right_side_desc = np.all(row[count:-1] >= row[count + 1 :])  # noqa: E203
            # check left side increasing from receive to transmit
            left_side_asc = np.all(row[:count] <= row[1 : count + 1])  # noqa: E203

            if plot_integrals:
                labels = [f"R{x}" for x in range(1, len(row) + 1)]
                ax[1].errorbar(x=labels, y=row, label=f"T{count+1}")
                ax[1].set_ylabel("Mean K-node voltage")
                ax[1].set_xlabel("Receive Electrode")
                ax[1].tick_params(axis="x", rotation=90)
                ax[1].grid(visible=True, axis="both")
                ax[1].legend(bbox_to_anchor=(1.04, 1), loc="center left")

            if not right_side_desc or not left_side_asc:
                logger.warn(
                    "Unexpected behaviour for"
                    f" T{device_data.electrodes[count]}-repeat{repeat}. "
                    "K-node voltages not decreasing with span."
                )


def read_gain_settings(
    device: str = "SH03",
    settings_per_span: list = [
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
):
    """
    Read gain factors for given settings_per_span per span
    for a specific calibrated device

    As of 2024-09-11, the sensor heads are calibrated according to the following
      span | 0   | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | 10  | 11  | 12  | 13  | 14
      -----------------------------------------------------------------------------------------------
      SH01 | 100 | 111 | 111 | 001 | 001 | 001 | 001 | 001 | 001 | 001 | 001 | 001 | 001 | 001 | 001
      SH02 | 100 | 111 | 111 | 001 | 001 | 001 | 001 | 001 | 001 | 001 | 001 | 001 | 001 | 001 | 001
      SH03 | 100 | 111 | 111 | 001 | 001 | 001 | 001 | 001 | 001 | 001 | 001 | 001 | 001 | 001 | 001
      SH04 | 100 | 111 | 111 | 001 | 001 | 001 | 001 | 001 | 001 | 001 | 001 | 001 | 001 | 001 | 001
      SH05 | 100 | 111 | 111 | 010 | 010 | 010 | 010 | 010 | 010 | 010 | 010 | 010 | 010 | 010 | 010

      Parameters:
    -----------
    device : str, optional
        The device identifier (default is "SH03").
    settings_per_span : list, optional
        List of gain settings per span (default is a predefined list).
    Returns:
    --------
    np.ndarray
        Calibrated gain factors. The shape of the array depends on the
        calibration type ("span" or "electrode").
    Raises:
    -------
    ValueError
        If the device is not calibrated or if the gain settings are not calibrated.
    """
    calibrated_gains = json.load(
        open(f"{ROOT_DIR}/scripts/utils/device_data/calibrated_gains.json", "r")
    )
    if device not in calibrated_gains.keys():
        raise ValueError(f"Uncalibrated device {device}")
    else:
        device_gains = calibrated_gains[device]
        gain_settings: dict = device_gains["settings"]

        error = []
        for setting in np.unique(settings_per_span):
            if setting not in gain_settings.keys():
                error.append(setting)
        if len(error) > 0:
            raise ValueError(f"Gain settings {error} not calibrated.")

        match device_gains["calibration"]:
            case "span":
                # Return calibrated gains per span
                return np.array(
                    [
                        [
                            gain_settings[setting]["tnode"]
                            for setting in settings_per_span
                        ],
                        [
                            gain_settings[setting]["knode"]
                            for setting in settings_per_span
                        ],
                    ]
                )

            case "electrode":
                # Gains calibrated per electrode using the logic analyser
                gain_factors = np.empty(
                    (2, len(settings_per_span), len(settings_per_span))
                )
                for t in range(len(settings_per_span)):
                    for r in range(len(settings_per_span)):
                        span = abs(t - r)
                        setting = settings_per_span[span]
                        factors = gain_settings[setting]
                        for tk, node in enumerate(["tnode", "knode"]):
                            gain_factors[tk, t, r] = factors[node][t]

                # return calibrated gains per pair
                return gain_factors

        # Uncalibrated device
        return np.ones((2, len(settings_per_span), len(settings_per_span)))


def is_valid_gain_span_calibration(d: dict) -> bool:
    """
    Validates if the given dictionary represents a valid gain span calibration.
    The function checks for the following conditions:
    1. The "calibration" key must have the value "span".
    2. The "date" key must be present and its value must be a string.
    3. The "settings" key must be present and its value must be a dictionary.
    4. The "settings" dictionary must contain the keys "001", "100", and "111".
    5. Each of the keys "001", "100", and "111" in the "settings" dictionary must map to another dictionary.
    6. Each of these nested dictionaries must contain the keys "knode" and "tnode".
    7. The values of "knode" and "tnode" must be either integers or floats.
    Args:
        d (dict): The dictionary to validate.
    Returns:
        bool: True if the dictionary is a valid gain span calibration, False otherwise.
    """

    if d.get("calibration") != "span":
        return False

    date = d.get("date")
    if date is None or not isinstance(date, str):
        return False

    settings = d.get("settings")

    if settings is None:
        return False

    if not isinstance(settings, dict):
        return False

    required_keys = ["001", "100", "111"]
    for k in required_keys:
        v = settings.get(k)
        if v is None:
            return False
        if not isinstance(v, dict):
            return False

        required_nodes = ["knode", "tnode"]
        for node in required_nodes:
            value = v.get(node)
            if value is None:
                return False
            if not isinstance(value, (int, float)):
                return False
    return True


def is_valid_gain_electrode_calibration(d: dict) -> bool:
    """
    Validates the structure and content of a dictionary representing gain electrode calibration data.
    Args:
        d (dict): The dictionary to validate. Expected to contain the following keys:
            - "calibration" (str): Should be "electrode".
            - "date" (str): A string representing the date.
            - "settings" (dict): A dictionary containing calibration settings with keys "001", "100", "111".
                Each of these keys should map to another dictionary with the following structure:
                    - "knode" (list): A list of 15 integers or floats.
                    - "tnode" (list): A list of 15 integers or floats.
    Returns:
        bool: True if the dictionary is valid according to the specified structure and content, False otherwise.
    """
    if d.get("calibration") != "electrode":
        return False

    date = d.get("date")
    if date is None or not isinstance(date, str):
        return False

    settings = d.get("settings")

    if settings is None:
        return False

    if not isinstance(settings, dict):
        return False

    required_keys = ["001", "100", "111"]
    for k in required_keys:
        v = settings.get(k)
        if v is None:
            return False
        if not isinstance(v, dict):
            return False

        required_nodes = ["knode", "tnode"]
        for node in required_nodes:
            value = v.get(node)
            if value is None:
                return False
            if not isinstance(value, list):
                return False
            if len(value) != 15:
                return False
            for i in value:
                if not isinstance(i, (int, float)):
                    return False
    return True


def is_valid_gain_calibration(d: dict) -> bool:
    return is_valid_gain_span_calibration(d) or is_valid_gain_electrode_calibration(d)


close_logger(logger)
