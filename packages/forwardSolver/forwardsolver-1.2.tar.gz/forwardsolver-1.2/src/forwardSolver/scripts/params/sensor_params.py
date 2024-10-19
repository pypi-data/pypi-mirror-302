from dataclasses import asdict, dataclass
from typing import Optional

import numpy as np


@dataclass(kw_only=True)
class SensorParams:
    """
    A class to represent the parameters for a sensor for the Forward Simulator.
    Attributes:
    -----------
    num_transmitter : Optional[int]
        Number of transmitters.
    c_receive_multiplexer_off : Optional[np.ndarray]
        Capacitance when the receive multiplexer is off.
    r_pulldown_on_receive : Optional[np.ndarray]
        Resistance of the pulldown on receive.
    c_probe : Optional[float]
        Capacitance of the probe.
    r_probe : Optional[float]
        Resistance of the probe.
    c_transmit_multiplexer_off : Optional[np.ndarray]
        Capacitance when the transmit multiplexer is off.
    r_series : Optional[np.ndarray]
        Series resistance.
    c_parasitic_forward_first_order : Optional[np.ndarray]
        Parasitic capacitance in the forward direction (first order).
    c_parasitic_backward_first_order : Optional[np.ndarray]
        Parasitic capacitance in the backward direction (first order).
    c_sensor : Optional[float]
        Capacitance of the sensor.
    num_wings : Optional[int]
        Number of wings.
    noise_random_seed : Optional[int]
        Seed for the random noise generator.
    noise_power_pulldown_on_receive : Optional[float]
        Noise power when pulldown is on receive.
    noise_power_transmit : Optional[float]
        Noise power during transmission.
    voltage_resolution_receive : Optional[float]
        Voltage resolution during receive.
    voltage_resolution_transmit : Optional[float]
        Voltage resolution during transmit.
    frequency_oscillation_receive : Optional[float]
        Frequency of oscillation during receive.
    phase_oscillation_receive : Optional[float]
        Phase of oscillation during receive.
    amplitude_oscillation_receive : Optional[float]
        Amplitude of oscillation during receive.
    Methods:
    __eq__(self, other):
        Checks if two SensorParams objects are equal by comparing their dictionary representations.
    as_dict(self):
        Converts the SensorParams object to a dictionary.
    """

    num_transmitter: Optional[int] = None
    c_receive_multiplexer_off: Optional[np.ndarray] = None
    r_pulldown_on_receive: Optional[np.ndarray] = None
    c_probe: Optional[float] = None
    r_probe: Optional[float] = None
    c_transmit_multiplexer_off: Optional[np.ndarray] = None
    r_series: Optional[np.ndarray] = None
    c_parasitic_forward_first_order: Optional[np.ndarray] = None
    c_parasitic_backward_first_order: Optional[np.ndarray] = None
    c_sensor: Optional[float] = None
    num_wings: Optional[int] = None
    noise_random_seed: Optional[int] = None
    noise_power_pulldown_on_receive: Optional[float] = None
    noise_power_transmit: Optional[float] = None
    voltage_resolution_receive: Optional[float] = None
    voltage_resolution_transmit: Optional[float] = None
    frequency_oscillation_receive: Optional[float] = None
    phase_oscillation_receive: Optional[float] = None
    amplitude_oscillation_receive: Optional[float] = None

    def __eq__(self, other):
        try:
            np.testing.assert_equal(self.as_dict(), other.as_dict())
        except AssertionError:
            return False
        return True

    def as_dict(self):
        return asdict(self)
