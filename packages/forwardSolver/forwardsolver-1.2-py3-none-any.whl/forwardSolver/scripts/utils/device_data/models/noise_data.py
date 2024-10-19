from dataclasses import asdict, dataclass
from typing import Dict, List


@dataclass
class MeanData:
    """
    A class to store a mean value along with its uncertainty.

    Args:
        mean (float): mean value
        std (float): standard deviation associated with the mean
    """

    mean: float = None
    std: float = None

    def to_dict(self):
        return asdict(self)


@dataclass(kw_only=True)
class NoiseData:
    """
    A class to store noise data from a device.

    Args:
        transmit (int): transmit electrode number
        receive (int): receive electrode number
        rms_noise (MeanData): mean and standard deviation of the rms noise
        snr (MeanData): mean and standard deviation of the signal-to-noise ratio (dB)
        poor_repeats (List[int]): a list of repeats which are too noisy
        good_repeats (List[int]): a list of repeats which are not too noisy
    """

    transmit: int = None
    receive: int = None
    rms_noise: MeanData = None
    snr: MeanData = None
    poor_repeats: List[int] = None
    good_repeats: List[int] = None

    def __post_init__(self):
        if isinstance(self.snr, Dict):
            self.snr = MeanData(**self.snr)
        if isinstance(self.rms_noise, Dict):
            self.rms_noise = MeanData(**self.rms_noise)

    def to_dict(self):
        return asdict(self)
