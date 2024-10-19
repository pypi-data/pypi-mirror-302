from copy import deepcopy
from logging import getLogger

import numpy as np
from scipy.signal import savgol_filter

from forwardSolver.scripts.utils.device_data.device_data import DeviceData

_logger = getLogger(__name__)


def decompose_sig_and_snr(
    voltages: np.ndarray, use_low_res: bool = False, use_subset: tuple = None
) -> tuple[np.ndarray, float, float]:
    """Calculate the signal and SNR of a given voltage trace. This function uses a
    Savitzky-Golay filter to smooth the voltage trace and then calculates the residuals
    between the original trace and the smoothed trace. The RMS of the residuals
    is used to calculate the SNR.

    Args:
        voltages (np.ndarray): The voltage trace to be analyzed.
        use_low_res (bool, optional): If True, a lower resolution Savitzky-Golay filter
        is used. Defaults to False.
        use_subset (tuple, optional): A tuple of length 2 that specifies the start and
        end indices of the trace to be analyzed. If None, the entire trace is used.
        Defaults to None.

    Raises:
        ValueError: If use_subset is not a tuple of length 2.

    Returns:
        tuple[np.ndarray, float, float]: The smoothed voltage trace, the RMS of the
        residuals, and the SNR.
    """
    if use_low_res:
        averaged_signal = savgol_filter(voltages, len(voltages) // 30, 1)
    else:
        averaged_signal = savgol_filter(voltages, len(voltages) // 200, 1)

    residuals = np.abs(voltages - averaged_signal)

    if use_subset is not None:
        if len(use_subset) != 2:
            raise ValueError("use_subset should be a tuple of length 2")
        ind1, ind2 = use_subset
        if ind1 is None:
            ind1 = 0
        if ind2 is None:
            ind2 = len(voltages)
        averaged_signal = averaged_signal[ind1:ind2]
        residuals = residuals[ind1:ind2]

    rms = np.sqrt(np.mean(np.square(residuals)))

    snr = 20 * np.log10(averaged_signal.std() / rms)

    return averaged_signal, rms, snr


def create_snr_dict(data: DeviceData) -> dict:
    """Create a dictionary of SNR values for each trace in the device data.

    Args:
        data (DeviceData): The device data to be analyzed.

    Returns:
        dict: A dictionary of SNR values for each trace in the device data.
    """

    def snr_only(voltages, use_low_res: bool = False, use_subset: tuple = None):
        """Helper function to calculate the SNR of a given voltage trace. This function
        throws away the smoothed voltage trace and the RMS of the residuals, and only
        returns the SNR.
        """
        _, _, snr = decompose_sig_and_snr(
            voltages, use_low_res=use_low_res, use_subset=use_subset
        )
        return snr

    result = {}
    num_electrodes = len(data.electrodes)
    for i in range(num_electrodes):
        for j in range(num_electrodes):
            tnodes = data.signal(i + 1, j + 1).raw_tnodes
            knodes = data.signal(i + 1, j + 1).raw_knodes
            result[f"T{i+1}R{j+1}t"] = np.array(
                [snr_only(tnode, use_low_res=(i != j)) for tnode in tnodes]
            )
            result[f"T{i+1}R{j+1}k"] = np.array(
                [snr_only(knode, use_low_res=(i != j)) for knode in knodes]
            )

    return result


def choose_snr_index(arr: np.ndarray, thresh: float) -> int:
    """Choose a random index from the array of SNR values that is greater than the
    specified threshold. If no such index exists, the index with the highest SNR is
    chosen.

    Args:
        arr (np.ndarray): The array of SNR values.
        thresh (float): The threshold for the SNR values.

    Returns:
        int: The chosen index.
    """
    good_repeats = np.where(arr > thresh)[0]
    if len(good_repeats) == 0:
        _logger.warning(f"No good repeats will use best snr available {arr.max()}")
        return np.argmax(arr)
    else:
        return np.random.choice(good_repeats)


# lets do some resampling of the experimental data and assess the variation in the capacitance
def resample_device_data(
    data: DeviceData, snr_thresh=-np.inf, snr_dict: dict = None
) -> tuple[DeviceData, np.ndarray, np.ndarray]:
    """Resample the device data and return the resampled data. The resampling is done
    by choosing a random trace from the repeated traces of each signal that has an SNR
    greater than the specified threshold. If no such trace exists, the trace with the
    highest SNR is chosen.


    Args:
        data (DeviceData): The device data to be resampled.
        snr_thresh (_type_, optional): The threshold for the SNR values. Defaults to -np.inf.
        snr_dict (dict, optional): A dictionary of SNR values for each trace in the device.
        If None, the SNR values are calculated using the create_snr_dict function. Defaults to None.

    Returns:
        tuple[DeviceData, np.ndarray, np.ndarray]: _description_
    """
    device_data = DeviceData()
    num_time_points = device_data.signal(1, 1).raw_tnodes.shape[-1]
    num_electrodes = len(device_data.electrodes)
    times = np.zeros((num_electrodes, num_electrodes, num_time_points))
    tnode_voltages = np.zeros((num_electrodes, num_electrodes, num_time_points))
    knode_voltages = np.zeros((num_electrodes, num_electrodes, num_time_points))
    snrs_tnode = np.zeros((num_electrodes, num_electrodes))
    snrs_knode = np.zeros((num_electrodes, num_electrodes))

    if snr_dict is None or not isinstance(snr_dict, dict):
        _logger.info("SNR dict not provided, will create one")
        snr_dict = create_snr_dict(data)

    for i in range(num_electrodes):
        for j in range(num_electrodes):
            times[i, j] = data.times[i, j]

            rand_int = choose_snr_index(snr_dict[f"T{i+1}R{j+1}t"], snr_thresh)
            t_voltages = data.signal(i + 1, j + 1).raw_tnodes[rand_int]
            tnode_voltages[i, j] = t_voltages
            snrs_tnode[i, j] = snr_dict[f"T{i+1}R{j+1}t"][rand_int]

            rand_int = choose_snr_index(snr_dict[f"T{i+1}R{j+1}k"], snr_thresh)
            k_voltages = data.signal(i + 1, j + 1).raw_knodes[rand_int]
            knode_voltages[i, j] = k_voltages
            snrs_knode[i, j] = snr_dict[f"T{i+1}R{j+1}k"][rand_int]

    device_data.times = times
    device_data.tnode_voltages = tnode_voltages
    device_data.knode_voltages = knode_voltages
    return device_data, snrs_tnode, snrs_knode


# NOISE CODE
def apply_noise(signal: np.ndarray, snr: float) -> np.ndarray:
    """Apply noise to a given signal using the specified SNR.

    Args:
        signal (np.ndarray): The signal to which noise is to be applied.
        snr (float): The SNR value.

    Returns:
        np.ndarray: The noisy signal.
    """
    rms = signal.std() / (10 ** (snr / 20))
    noise = np.random.normal(0, rms, len(signal))
    return signal + noise


def apply_noise_to_device_data(
    device_data: DeviceData, snr_dict: dict, snr_threshold: float = -np.inf
) -> DeviceData:
    """Apply noise to the device data using the specified SNR values.

    Args:
        device_data (DeviceData): The device data to which noise is to be applied.
        snr_dict (dict): A dictionary of SNR values for each trace in the device data.
        snr_threshold (float, optional): The threshold for the SNR values. Defaults to -np.inf.

    Returns:
        DeviceData: The device data with noise applied.
    """

    device_data_noisy = deepcopy(device_data)
    num_electrodes = len(device_data.electrodes)

    for i in range(num_electrodes):
        for j in range(num_electrodes):

            tnodes = device_data.tnode_voltages[i, j]
            snr_list = snr_dict[f"T{i+1}R{j+1}t"]

            all_tnodes = np.zeros((len(snr_list), tnodes.shape[0]))
            print(f"{all_tnodes.shape = }")
            for count, snr in enumerate(snr_list):
                if snr < snr_threshold:
                    # put nans in the array
                    all_tnodes[count] = np.nan * np.ones(tnodes.shape[0])
                else:
                    # lets apply the noise and get an average tnode signal after the for loop
                    all_tnodes[count] = apply_noise(tnodes, snr)
            # device_data_noisy.tnode_voltages[i,j] = all_tnodes.mean(axis=0)
            device_data_noisy.tnode_voltages[i, j] = np.nanmean(all_tnodes, axis=0)

            knodes = device_data.knode_voltages[i, j]
            snr_list = snr_dict[f"T{i+1}R{j+1}k"]
            all_knodes = np.zeros((len(snr_list), knodes.shape[0]))
            for count, snr in enumerate(snr_list):
                if snr < snr_threshold:
                    # put nans in the array
                    all_knodes[count] = np.nan * np.ones(knodes.shape[0])
                else:
                    # lets apply the noise and get an average knode signal after the for loop
                    all_knodes[count] = apply_noise(knodes, snr)
            device_data_noisy.knode_voltages[i, j] = np.nanmean(all_knodes, axis=0)
    return device_data_noisy
