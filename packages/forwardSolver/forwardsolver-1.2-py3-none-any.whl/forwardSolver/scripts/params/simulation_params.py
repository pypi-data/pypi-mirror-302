from dataclasses import asdict, dataclass
from typing import Optional

import numpy as np


@dataclass(kw_only=True)
class SimulationParams:
    """
    A class to represent the simulation parameters.
    Attributes:
    ----------
    t_step : Optional[float]
        The time step for the simulation.
    t_end : Optional[float]
        The end time for the simulation.
    compute_sensitivities : Optional[bool]
        Flag to determine if sensitivities should be computed.
    normalise_sensitivity_by_cap : Optional[bool]
        Flag to determine if sensitivities should be normalized by capacity.
    compute_sensitivity_sum : Optional[bool]
        Flag to determine if the sum of sensitivities should be computed.
    compute_single_sensitivity_sum : Optional[bool]
        Flag to determine if the sum of single sensitivities should be computed.
    compute_sensitivity_electrode_pair : Optional[bool]
        Flag to determine if sensitivities for electrode pairs should be computed.
    num_sensitivity_slice_points : Optional[int]
        Number of points to slice for sensitivity computation.
    Methods:
    -------
    __eq__(self, other):
        Checks if two SimulationParams instances are equal by comparing their dictionary representations.
    as_dict(self):
        Converts the SimulationParams instance to a dictionary.
    """

    t_step: Optional[float] = None
    t_end: Optional[float] = None
    compute_sensitivities: Optional[bool] = None
    normalise_sensitivity_by_cap: Optional[bool] = None
    compute_sensitivity_sum: Optional[bool] = None
    compute_single_sensitivity_sum: Optional[bool] = None
    compute_sensitivity_electrode_pair: Optional[bool] = None
    num_sensitivity_slice_points: Optional[int] = None

    def __eq__(self, other):
        try:
            np.testing.assert_equal(self.as_dict(), other.as_dict())
        except AssertionError:
            return False
        return True

    def as_dict(self):
        return asdict(self)
