import copy
from dataclasses import dataclass
from typing import Optional

import numpy as np
from PySpice.Spice.Netlist import Circuit

from forwardSolver.scripts.params.forward_solver_params import (
    ForwardSolverParams,
)
from forwardSolver.scripts.solver_forward_P1000 import SolverForwardP1000
from forwardSolver.scripts.utils.constants import (
    MEGA_OHM_TO_OHM,
    MICROSECONDS_TO_SECONDS,
    PICO_FARAD_TO_FARAD,
)
from forwardSolver.scripts.utils.device_data.device_data import DeviceData
from forwardSolver.scripts.utils.logging import close_logger, get_logger

logger = get_logger(__name__)

# Temporarily defined global variable to denote a large resistance value (open circuit)
LARGE_RESISTANCE_OHM = 1e20
SMALL_RESISTANCE_OHM = 1e-20
SMALL_CAPACITANCE_FARAD = 1e-30


def pwl_source_from_device_data(
    device_data: DeviceData, subsample_interval: int = 1
) -> list:
    """

    This function returns the piecewise linear voltage sourced derived from the
    measured T-node voltages, which can be then applied to the nodes of the spice model.

    Args:
        device_data: device data object with measured T-node source voltage.
        subsample_interval: Subsampling interval to be applied to the measured T-node
        voltage that is converted to piecewise linear source.

    Returns:
        List representing piecewise linear sources which are tuples of time instants and
        corresponding voltages.
    """
    source_list = []
    num_electrodes = device_data.knode_voltages.shape[0]
    for iloop in range(num_electrodes):
        source_list.append(
            list(
                zip(
                    device_data.times[iloop, iloop, ::subsample_interval],
                    device_data.tnode_voltages[
                        iloop, iloop, ::subsample_interval
                    ],
                )
            )
        )
    return source_list


@dataclass
class CircuitParameters:
    """A class that holds the circuit parameters like the resistance and
    capacitance values."""

    resistance_tnode_to_ground: Optional[np.ndarray] = None
    capacitance_tnode_to_ground: Optional[np.ndarray] = None
    resistance_tnode_to_knode: Optional[np.ndarray] = None
    resistance_knode_to_ground: Optional[np.ndarray] = None
    capacitance_knode_to_ground: Optional[np.ndarray] = None
    resistance_at_source: Optional[float] = None
    capacitance_source_to_ground: Optional[float] = None
    resistance_at_source: Optional[float] = None
    capacitance_source_to_ground: Optional[float] = None


@dataclass
class WaveformParameters:
    """A class that holds the source voltage waveform parameters.
    The parameters are used to define a piecewise constant voltage source in spice.
    """

    time_start: Optional[float] = None
    time_delay: Optional[float] = None
    time_rise: Optional[float] = None
    time_dwell: Optional[float] = None
    time_fall: Optional[float] = None
    time_end: Optional[float] = None
    time_step: Optional[float] = None
    voltage_max: Optional[float] = None
    voltage_start: Optional[float] = None
    voltage_end: Optional[float] = None


class SpiceSolver:
    """
    A class that simulates the equivalent circuit from the forward model
    capacitances. If the capacitance matrix is provided, it is made use of directly.
    If capacitance matrix is not provided the forward model parameters are used to
    generate it.
    The class uses PySpice to solve the circuit voltages, which is a python API
    built on top of ngspice.
    The information about PySpice is available at the following link:
        https://pyspice.fabrice-salvaire.fr/releases/v1.4/
    """

    def __init__(
        self,
        params_forward_solver: ForwardSolverParams,
        capacitance_matrix: Optional[np.ndarray] = None,
        params_circuit: Optional[CircuitParameters] = None,
        params_waveform: Optional[WaveformParameters] = None,
        resistance_at_source: float = 10e3,
        capacitance_source_to_ground: float = 1e-15,
        time_start: float = 0.0,
        time_delay: float = 0.0,
        voltage_start: float = 0.0,
        voltage_end: float = 0.0,
        use_ground_capacitances: bool = False,
        physics_model: int = 0,
        pwl_source_list_at_tnode: Optional[list] = None,
    ) -> None:
        """

        Args:
            params_forward_solver: forward solver parameter object
            capacitance_matrix: the full forward solver capacitance matrix
                    with inter electrode and electrode to ground capacitances (pF)
            params_circuit: resistances and capacitances of the circuit (SI units)
            params_waveform: source voltage waveform parameters (SI units)
            resistance_at_source: the series resistance of the voltage source (ohm)
            capacitance_source_to_ground: capacitance from voltage source to ground (F)
            time_start: the start time of voltage signal (s)
            time_delay: the delay time of voltage signal (s)
            voltage_start: voltage level at the start (V)
            voltage_end: voltage level at the end (V)
            use_ground_capacitances: whether the ground capacitances are used in
                                        voltage calculation
            physics_model: physics model for capacitance calculation
            pwl_source_list_at_tnode: piecewise source list to be applied
                                        directly to the tnode
        """
        self.params_forward_solver = params_forward_solver

        # Capacitance matrix in SI units. It is assumed to be provided in pF and
        self.use_ground_capacitances = use_ground_capacitances
        self.physics_model = physics_model
        # converted to SI units.
        if capacitance_matrix is None:
            logger.info(
                "Calculated capacitances from forward solver parameters."
            )
            self.capacitance_matrix = (
                PICO_FARAD_TO_FARAD
                * self.calculate_capacitance(
                    use_ground_capacitances, physics_model
                )
            )
        else:
            self.capacitance_matrix = PICO_FARAD_TO_FARAD * copy.deepcopy(
                capacitance_matrix
            )
        self.num_electrodes = self.capacitance_matrix.shape[0]

        # Circuit parameters in SI units
        if params_circuit is None:
            self.params_circuit = self.get_circuit_parameters(
                resistance_at_source, capacitance_source_to_ground
            )
        else:
            self.params_circuit = copy.deepcopy(params_circuit)

        # Source waveform parameters
        if params_waveform is None:
            self.params_waveform = self.get_waveform_parameters(
                time_start, time_delay, voltage_start, voltage_end
            )
        else:
            self.params_waveform = copy.deepcopy(params_waveform)

        self.pwl_source_list_at_tnode = pwl_source_list_at_tnode

    def calculate_capacitance(
        self, use_ground_capacitances: bool = False, physics_model: int = 0
    ) -> None:
        """If the capacitance matrix is not provided, this function is used to
        compute it using the provided forward solver parameters."""

        if use_ground_capacitances:
            solver_forward = SolverForwardP1000(
                self.params_forward_solver,
                is_cap_calculated=False,
                is_full_cap_calculated=True,
                is_voltage_mat_calculated=False,
                physics_model=physics_model,
            )
            capacitance_matrix = solver_forward.C_full

        else:
            solver_forward = SolverForwardP1000(
                self.params_forward_solver,
                is_cap_calculated=True,
                is_full_cap_calculated=False,
                is_voltage_mat_calculated=False,
                physics_model=physics_model,
            )
            capacitance_matrix = solver_forward.C_true

        return capacitance_matrix

    def get_circuit_parameters(
        self, resistance_at_source: float, capacitance_source_to_ground: float
    ) -> CircuitParameters:
        """

        If the circuit parameters are not provided, this function is used to
        define it in SI units from the provided forward solver parameters.

        Args:
            resistance_at_source: the series resistance of the voltage source (ohm)
            capacitance_source_to_ground: source capacitance between the
                                          source resistance and ground (farad).
        Returns:
            params_circuit: circuit parameters defined using forward solver parameters
                            and the source resistance and capacitance values.

        """

        params_circuit = CircuitParameters()
        # Currently resister from tnode to ground is not present, so set to a hgh value
        params_circuit.resistance_tnode_to_ground = (
            LARGE_RESISTANCE_OHM * np.ones((self.num_electrodes))
        )

        params_circuit.capacitance_tnode_to_ground = (
            PICO_FARAD_TO_FARAD
            * self.params_forward_solver.sensor.c_transmit_multiplexer_off
        )

        params_circuit.resistance_tnode_to_knode = (
            MEGA_OHM_TO_OHM * self.params_forward_solver.sensor.r_series
        )

        params_circuit.resistance_knode_to_ground = (
            MEGA_OHM_TO_OHM
            * self.params_forward_solver.sensor.r_pulldown_on_receive
        )

        params_circuit.capacitance_knode_to_ground = (
            PICO_FARAD_TO_FARAD
            * self.params_forward_solver.sensor.c_receive_multiplexer_off
        )
        params_circuit.resistance_at_source = resistance_at_source
        params_circuit.capacitance_source_to_ground = (
            capacitance_source_to_ground
        )
        return params_circuit

    def get_waveform_parameters(
        self,
        time_start: float,
        time_delay: float,
        voltage_start: float,
        voltage_end: float,
    ) -> None:
        """

        If the waveform parameters are not provided, this function is used to
        define it in SI units from the provided forward solver parameters.

        Args:
            time_start: simulation start time(s)
            time_delay: delay between start of simulation and start of
                        pulse voltage source (s).
            voltage_start: voltage level at the start of the simulation
            voltage_end: voltage level and the end of simulation
        """

        params_waveform = WaveformParameters()
        params_waveform.time_start = time_start
        params_waveform.time_delay = time_delay
        params_waveform.time_rise = (
            self.params_forward_solver.signal.t_rise * MICROSECONDS_TO_SECONDS
        )
        params_waveform.time_dwell = (
            self.params_forward_solver.signal.t_dwell * MICROSECONDS_TO_SECONDS
        )
        params_waveform.time_fall = (
            self.params_forward_solver.signal.t_fall * MICROSECONDS_TO_SECONDS
        )
        params_waveform.time_end = (
            self.params_forward_solver.simulation.t_end
            * MICROSECONDS_TO_SECONDS
        )
        params_waveform.time_step = (
            self.params_forward_solver.simulation.t_step
            * MICROSECONDS_TO_SECONDS
        )
        params_waveform.voltage_max = self.params_forward_solver.signal.v_max
        params_waveform.voltage_start = voltage_start
        params_waveform.voltage_end = voltage_end
        return params_waveform

    def create_source_pwl_points_dict(self) -> list:
        """
        Function used to define the piecewise linear voltage source.

        Returns:
            A list of tuples of the form (time, voltage) that is used to define the
            piecewise linear voltage source in spice.
        """
        start_tuple = (
            self.params_waveform.time_start,
            self.params_waveform.voltage_start,
        )
        if self.params_waveform.time_delay != 0:
            delay_tuple = (
                self.params_waveform.time_start
                + self.params_waveform.time_delay,
                self.params_waveform.voltage_start,
            )
        else:
            delay_tuple = None
        rise_tuple = (
            self.params_waveform.time_start
            + self.params_waveform.time_delay
            + self.params_waveform.time_rise,
            self.params_waveform.voltage_max,
        )
        if self.params_waveform.time_dwell < self.params_waveform.time_end:
            dwell_tuple = (
                self.params_waveform.time_start
                + self.params_waveform.time_delay
                + self.params_waveform.time_rise
                + self.params_waveform.time_dwell,
                self.params_waveform.voltage_max,
            )
            fall_tuple = (
                self.params_waveform.time_start
                + self.params_waveform.time_delay
                + self.params_waveform.time_rise
                + self.params_waveform.time_dwell
                + self.params_waveform.time_fall,
                self.params_waveform.voltage_end,
            )
        else:
            dwell_tuple = None
            fall_tuple = None
        end_tuple = (
            self.params_waveform.time_start
            + self.params_waveform.time_delay
            + self.params_waveform.time_end,
            self.params_waveform.voltage_end,
        )
        source_pwl_points_dict = dict(
            start_tuple=start_tuple,
            delay_tuple=delay_tuple,
            rise_tuple=rise_tuple,
            dwell_tuple=dwell_tuple,
            fall_tuple=fall_tuple,
            end_tuple=end_tuple,
        )

        source_pwl_points_dict = {
            key: value
            for key, value in source_pwl_points_dict.items()
            if value is not None
        }

        return source_pwl_points_dict

    def create_spice_rc_network(self) -> Circuit:
        """

        This function defines the RC network that is simulated using spice solver.
        The network can be defined by the following:
        (Ti, Ki are T node and K node of the ith electrode)

            R_TGi Ti 0 resistance_tnode_to_ground
            C_TGi Ti 0 capacitance_tnode_to_ground
            R_TKi Ti Ki resistance_tnode_to_knode
            R_KGi Ki 0 resistance_knode_to_ground
            C_KGi Ki 0 capacitance_knode_to_ground
            C_ij Ki Kj capacitance_matrix[i,j]

        Returns:
            The PySpice Circuit object with RC network.
        """
        circuit = Circuit("spice_circuit")
        for iloop_electrode in range(1, self.num_electrodes + 1):
            # Resistance from T node to ground
            circuit.R(
                f"_TG{iloop_electrode}",
                f"T{iloop_electrode}",
                circuit.gnd,
                self.params_circuit.resistance_tnode_to_ground[
                    iloop_electrode - 1
                ],
            )

            # Capacitance from T node to ground
            circuit.C(
                f"_TG{iloop_electrode}",
                f"T{iloop_electrode}",
                circuit.gnd,
                self.params_circuit.capacitance_tnode_to_ground[
                    iloop_electrode - 1
                ],
            )

            # Resistance from T node to K node
            circuit.R(
                f"_TK{iloop_electrode}",
                f"T{iloop_electrode}",
                f"K{iloop_electrode}",
                self.params_circuit.resistance_tnode_to_knode[
                    iloop_electrode - 1
                ],
            )

            # Resistance from K node to ground
            circuit.R(
                f"_KG{iloop_electrode}",
                f"K{iloop_electrode}",
                circuit.gnd,
                self.params_circuit.resistance_knode_to_ground[
                    iloop_electrode - 1
                ],
            )

            # Capacitance from K node to ground
            capacitance_knode_to_ground_full = (
                self.params_circuit.capacitance_knode_to_ground[
                    iloop_electrode - 1
                ]
            )

            if self.use_ground_capacitances:
                capacitance_knode_to_ground_full += +np.real(
                    self.capacitance_matrix[
                        iloop_electrode - 1, iloop_electrode - 1
                    ]
                )

            circuit.C(
                f"_KG{iloop_electrode}",
                f"K{iloop_electrode}",
                circuit.gnd,
                capacitance_knode_to_ground_full,
            )

        for iloop_electrode in range(1, self.num_electrodes + 1):
            for jloop_electrode in range(
                iloop_electrode + 1, self.num_electrodes + 1
            ):
                circuit.C(
                    f"_{iloop_electrode}_{jloop_electrode}",
                    f"K{iloop_electrode}",
                    f"K{jloop_electrode}",
                    np.real(
                        self.capacitance_matrix[
                            iloop_electrode - 1, jloop_electrode - 1
                        ]
                    ),
                )
                if (
                    np.imag(
                        self.capacitance_matrix[
                            iloop_electrode - 1, jloop_electrode - 1
                        ]
                    )
                    != 0
                ):
                    circuit.R(
                        f"_{iloop_electrode}_{jloop_electrode}",
                        f"K{iloop_electrode}",
                        f"K{jloop_electrode}",
                        1.0
                        / (
                            2
                            * np.pi
                            * self.params_forward_solver.signal.frequency
                        )
                        / np.imag(
                            self.capacitance_matrix[
                                iloop_electrode - 1, jloop_electrode - 1
                            ]
                        ),
                    )

        return circuit

    def create_spice_netlist(self, source_node_index: int) -> Circuit:
        """
        This function forms the spice circuit netlist by attaching the piecewise linear
        voltage source to the RC network at the T node of the electrode specified
        by source_node_index.

        Args:
            source_node_index: the index of the electrode on which
                               the source voltage is applied.

        Returns:
            The PySpice Circuit object with the RC network and the voltage source.
        """
        circuit = self.create_spice_rc_network()
        if self.pwl_source_list_at_tnode is None:
            circuit.PieceWiseLinearVoltageSource(
                f"_source_{source_node_index}",
                f"E{source_node_index}",
                circuit.gnd,
                list(self.create_source_pwl_points_dict().values()),
            )
            circuit.R(
                f"_source_{source_node_index}",
                f"E{source_node_index}",
                f"T{source_node_index}",
                self.params_circuit.resistance_at_source,
            )
            circuit.C(
                f"_source_{source_node_index}",
                f"T{source_node_index}",
                circuit.gnd,
                self.params_circuit.capacitance_source_to_ground,
            )
        else:
            circuit.PieceWiseLinearVoltageSource(
                f"_source_{source_node_index}",
                f"E{source_node_index}",
                circuit.gnd,
                self.pwl_source_list_at_tnode[source_node_index - 1],
            )
            circuit.R(
                f"_source_{source_node_index}",
                f"E{source_node_index}",
                f"T{source_node_index}",
                SMALL_RESISTANCE_OHM,
            )
            circuit.C(
                f"_source_{source_node_index}",
                f"T{source_node_index}",
                circuit.gnd,
                SMALL_CAPACITANCE_FARAD,
            )

        return circuit

    def interpolate_spice_voltages(
        self,
        time: np.ndarray,
        tnode_voltage: np.ndarray,
        knode_voltage: np.ndarray,
    ) -> tuple:
        """
        The ODE solver in SPICE uses adaptive time steps to calculate the solution.
        Therefore, to convert the obtained solutions to have regular time points,
        interpolation is required.

        Args:
            time: The time points at which SPICE has found the solution.
            tnode_voltage: T node voltage solution obtained from SPICE.
            knode_voltage: K node voltage solution obtained from SPICE.

        Returns:
            tuple of numpy arrays with time, tnode and knode voltages at
            regular time instants obtained by interpolating the SPICE solution.
        """

        num_points_new = (
            int(
                (
                    self.params_waveform.time_end
                    - self.params_waveform.time_start
                )
                / self.params_waveform.time_step
            )
            + 1
        )
        time_interpolated = np.linspace(
            self.params_waveform.time_start,
            self.params_waveform.time_end,
            num_points_new,
        )
        tnode_voltage_interpolated = np.zeros(
            (self.num_electrodes, len(time_interpolated))
        )
        knode_voltage_interpolated = np.zeros(
            (self.num_electrodes, len(time_interpolated))
        )

        for iloop_electrode in range(self.num_electrodes):
            tnode_voltage_interpolated[iloop_electrode] = np.interp(
                time_interpolated, time, tnode_voltage[iloop_electrode]
            )
            knode_voltage_interpolated[iloop_electrode] = np.interp(
                time_interpolated, time, knode_voltage[iloop_electrode]
            )

        return (
            time_interpolated,
            tnode_voltage_interpolated,
            knode_voltage_interpolated,
        )

    def calculate_spice_voltages(self, source_node_index: int = 1) -> tuple:
        """
        Function to define and solves the spice model for the voltage source connected
        to the specified electrode and then interpolate the solution to a
        regular time interval.

        Args:
            source_node_index: the index of transmit electrode to which
                               the source is connected.

        Returns:
            Tuple of arrays with time, K node and T node data obtained
            after solving the spice model and interpolating.
        """

        circuit = self.create_spice_netlist(
            source_node_index,
        )
        simulator = circuit.simulator()
        analysis = simulator.transient(
            step_time=self.params_waveform.time_step,
            end_time=self.params_waveform.time_end,
            start_time=self.params_waveform.time_start,
            max_time=self.params_waveform.time_step,
        )
        time_spice = np.array(analysis.time)
        tnode_voltage_spice = np.zeros((self.num_electrodes, len(time_spice)))
        knode_voltage_spice = np.zeros((self.num_electrodes, len(time_spice)))
        for iloop_electrode in range(1, self.num_electrodes + 1):
            tnode_voltage_spice[iloop_electrode - 1] = np.array(
                analysis[f"T{iloop_electrode}"]
            )
            knode_voltage_spice[iloop_electrode - 1] = np.array(
                analysis[f"K{iloop_electrode}"]
            )

        (
            time_interpolated,
            tnode_voltage_interpolated,
            knode_voltage_interpolated,
        ) = self.interpolate_spice_voltages(
            time_spice, tnode_voltage_spice, knode_voltage_spice
        )

        return (
            time_interpolated,
            tnode_voltage_interpolated,
            knode_voltage_interpolated,
        )

    def create_spice_device_data(self) -> DeviceData:
        """
        Function that creates a DeviceData object with the SPICE solution for the given
        parameters.

        Returns:
            DeviceData object with the interpolated SPICE solution.
        """
        num_time_points = (
            int(
                (
                    self.params_waveform.time_end
                    - self.params_waveform.time_start
                )
                / self.params_waveform.time_step
            )
            + 1
        )

        times = np.zeros(
            (self.num_electrodes, self.num_electrodes, num_time_points)
        )
        tnode_voltages = np.zeros(
            (self.num_electrodes, self.num_electrodes, num_time_points)
        )
        knode_voltages = np.zeros(
            (self.num_electrodes, self.num_electrodes, num_time_points)
        )

        for transmit_electrode in range(1, self.num_electrodes + 1):
            (
                times[transmit_electrode - 1],
                tnode_voltages[transmit_electrode - 1],
                knode_voltages[transmit_electrode - 1],
            ) = self.calculate_spice_voltages(transmit_electrode)

        device_data = DeviceData()
        device_data.times = times
        device_data.knode_voltages = knode_voltages
        device_data.tnode_voltages = tnode_voltages

        return device_data


close_logger(logger)
