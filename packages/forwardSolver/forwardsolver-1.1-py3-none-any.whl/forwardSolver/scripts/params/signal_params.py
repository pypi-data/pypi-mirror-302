from dataclasses import asdict, dataclass
from typing import Optional

import numpy as np


@dataclass(kw_only=True)
class SignalParams:
    """
    A class to represent the signal params.
    Attributes:
    ----------
    t_rise : Optional[float]
        The rise time of the signal.
    t_dwell : Optional[float]
        The dwell time of the signal.
    t_fall : Optional[float]
        The fall time of the signal.
    t_period : Optional[float]
        The period of the signal.
    v_max : Optional[float]
        The maximum voltage of the signal.
    noise_power : Optional[float]
        The power of the noise in the signal.
    noise_random_seed : Optional[int]
        The random seed for noise generation.
    frequency : Optional[float]
        The frequency of the signal.
    Methods:
    -------
    __eq__(self, other):
        Checks if two SignalParams instances are equal by comparing their dictionaries.
    as_dict(self):
        Converts the SignalParams instance to a dictionary.
    """

    t_rise: Optional[float] = None
    t_dwell: Optional[float] = None
    t_fall: Optional[float] = None
    t_period: Optional[float] = None
    v_max: Optional[float] = None
    noise_power: Optional[float] = None
    noise_random_seed: Optional[int] = None
    frequency: Optional[float] = None

    def __eq__(self, other):
        try:
            np.testing.assert_equal(self.as_dict(), other.as_dict())
        except AssertionError:
            return False
        return True

    def as_dict(self):
        return asdict(self)
