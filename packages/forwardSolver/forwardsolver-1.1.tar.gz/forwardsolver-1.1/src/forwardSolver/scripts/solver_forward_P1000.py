import copy
from dataclasses import asdict

import numpy as np
import scipy.sparse as sps

from forwardSolver.scripts.params.forward_solver_params import (
    ForwardSolverParams,
)
from forwardSolver.scripts.utils.cache import create_cache, find_cached
from forwardSolver.scripts.utils.constants import (
    CACHE_INPUT,
    CACHE_INPUT_VOLTAGE,
    CACHE_OUTPUT,
    CREATE_PARALLEL_SUBDIR,
    EPSILON_0,
    FREEFEM_DIR,
    IS_CAP_CALCULATED,
    IS_FULL_CAP_CALCULATED,
    IS_PYTHON_USED_AS_SOLVER,
    IS_VOLTAGE_MAT_CALCULATED,
    MICROSECONDS_TO_SECONDS,
    PHYSICS_MODEL,
)
from forwardSolver.scripts.utils.device_data.device_data import (
    DeviceDataSynthetic,
)
from forwardSolver.scripts.utils.hash import hash_dictionary
from forwardSolver.scripts.utils.logging import close_logger, get_logger
from forwardSolver.scripts.utils.modules import SimulationModule
from forwardSolver.scripts.utils.utils_solver_forward_P1000 import (
    compute_electric_field_DtoS,
    dot_product_lists,
    plot_boundary_values,
    plot_electric_field,
    plot_geometry,
    setup_solver_environment,
    timestep_electric_field_DtoS,
    timestep_potentials_at_all_nodes,
    timestep_potentials_for_all_transmitters,
)

logger = get_logger(__name__)


class SolverForwardP1000(SimulationModule):
    """
    Forward solver_artefacts for a 2D voltage signal for the solver_artefacts board
    Attributes:
        params (ForwardSolverParams): Parameters for the forward solver.
        use_cache_output (bool): Flag to use cached output.
        use_cache_input (bool): Flag to use cached input.
        create_parallel_subdir (bool): Flag to create parallel subdirectory.
        is_cap_calculated (bool): Flag to indicate if capacitance is calculated.
        is_full_cap_calculated (bool): Flag to indicate if full capacitance is calculated.
        is_voltage_mat_calculated (bool): Flag to indicate if voltage matrix is calculated.
        is_python_used_as_solver (bool): Flag to indicate if Python is used as solver.
        physics_model (str): The physics model to be used.
        export_mesh (bool): Flag to export mesh.
        solver_subdir (str): Subdirectory for the solver.
        sA, B, sL, mesh, eps, sig, C_true, C_full, sensitivities, pixels, A_tensor, K_tensor, LHSBC, Aback, Kback, sensitivity_mesh, v_slice_sens, h_slice_sens1, h_slice_sens2, h_slice_sens3, sensitivity_electrode_pair, sensitivity_single_electrode_sum, sensitivity_total_sum: Various attributes related to the solver environment.
        t, V, Q: Time, voltage, and charge attributes.
        voltage_knode, voltage_tnode, voltage_knode_for_all_transmitters, voltage_tnode_for_all_transmitters: Voltage attributes for nodes and transmitters.
    Methods:
        __init__(self, params, use_cache_output, use_cache_input, create_parallel_subdir, is_cap_calculated, is_full_cap_calculated, is_voltage_mat_calculated, is_python_used_as_solver, physics_model, export_mesh):
            Initializes the SolverForwardP1000 instance with the given parameters.
        check_inputs(self):
            Checks the validity of the input parameters.
        check_simulation(self):
            Checks if the voltage or charge contain any infinities or NaNs.
        calculate_voltages(self, t, V_transmit, specific_probe_position=None):
            Calculates the voltages for the given time and transmit voltage.
        calculate_voltages_at_all_nodes(self, t, V_transmit, specific_probe_position=None):
            Returns the T node and K node voltages for each electrode.
        calculate_voltages_for_all_transmitters(self, t, V_transmit, specific_probe_position=None, array_of_transmitters=None):
            Returns the T node and K node voltages for each electrode for all transmit electrodes in array_of_transmitters.
        cache(self):
            Saves the current state to file.
        simulate(self, t, V_transmit, specific_probe_position=None, use_cached_voltage=CACHE_INPUT_VOLTAGE):
            Simulates the forward problem and returns the voltages and charges.
        check_voltage_calculation_at_all_nodes(self):
            Checks if the calculated array contains any infinities for node voltages.
        export_voltages_at_all_nodes(self, t, V_transmit, specific_probe_position=None, use_cached_voltage=CACHE_INPUT_VOLTAGE):
            Exports the voltages at all nodes.
        check_voltage_calculation_for_all_transmitters(self):
            Checks if the calculated array contains any infinities for all transmitters.
        export_voltages_for_all_transmitters(self, t, V_transmit, array_of_transmitters=None, use_cached_voltage=CACHE_INPUT_VOLTAGE):
            Exports the voltages for all transmitters.
        export_voltages_for_all_transmitters_to_devicedata(self, t, V_transmit, array_of_transmitters=None, use_cached_voltage=CACHE_INPUT_VOLTAGE):
            Exports pre-computed voltages to DeviceData instance.
        get_board_height(self):
            Returns the height of the board (y coordinate) in FreeFem coordinate space.
        compute_mesh_epsilon(self, epsilon_matrix, update_eps=True):
            Computes the epsilon values of the mesh elements.
        build_FE_matrices(self, epsilon_matrix):
            Builds FEM matrices given epsilon distribution.
        calculate_capacitance_matrix(self, epsilon_matrix):
        calculate_sensitivity_matrix(self, epsilon_matrix, eps_step=0.1, scale_output=False, permittivity_max=1.0):
            Computes the sensitivity matrix (linearized Jacobian) about the current permittivity given by epsilon_vector.
    """

    def __init__(
        self,
        params: ForwardSolverParams,
        use_cache_output=CACHE_OUTPUT,
        use_cache_input=CACHE_INPUT,
        create_parallel_subdir=CREATE_PARALLEL_SUBDIR,
        is_cap_calculated=IS_CAP_CALCULATED,
        is_full_cap_calculated=IS_FULL_CAP_CALCULATED,
        is_voltage_mat_calculated=IS_VOLTAGE_MAT_CALCULATED,
        is_python_used_as_solver=IS_PYTHON_USED_AS_SOLVER,
        physics_model=PHYSICS_MODEL,
        export_mesh=True,
    ):
        self.params = copy.deepcopy(params)

        if self.params.solver_dir is not None:
            solver_dir = FREEFEM_DIR + f"/{self.params.solver_dir}/"
        else:
            solver_dir = FREEFEM_DIR + "/model_solver/"
            logger.info(
                f"Solver dir not set, using default solver: {solver_dir}"
            )

        if self.params.solver_file is not None:
            solver_file = self.params.solver_file
        else:
            solver_file = "model_solver.edp"
            logger.info(
                f"Solver file not set, using default solver: {solver_file}"
            )

        logger.info(f"Using default solver:{solver_dir}/{solver_file}")

        # Setup from cache if it exists and use_cache_input is true
        cached = find_cached(hash_dictionary(asdict(self.params)))
        if cached is None or not use_cache_input:
            (
                self.solver_subdir,
                self.sA,
                self.B,
                self.sL,
                self.mesh,
                self.eps,
                self.sig,
                self.C_true,
                self.C_full,
                self.sensitivities,
                self.pixels,
                self.A_tensor,
                self.K_tensor,
                self.LHSBC,
                self.Aback,
                self.Kback,
                self.sensitivity_mesh,
                self.v_slice_sens,
                self.h_slice_sens1,
                self.h_slice_sens2,
                self.h_slice_sens3,
                self.sensitivity_electrode_pair,
                self.sensitivity_single_electrode_sum,
                self.sensitivity_total_sum,
            ) = setup_solver_environment(
                self.params,
                solver_dir,
                solver_file,
                create_parallel_subdir=create_parallel_subdir,
                is_capacitance_calculated=is_cap_calculated,
                is_full_capacitance_calculated=is_full_cap_calculated,
                is_voltage_mat_calculated=is_voltage_mat_calculated,
                is_python_used_as_solver=is_python_used_as_solver,
                physics_model=physics_model,
                export_mesh=export_mesh,
            )

            self.t = None
            self.V = None
            self.Q = None
            self.voltage_knode = None
            self.voltage_tnode = None
            self.voltage_knode_for_all_transmitters = None
            self.voltage_tnode_for_all_transmitters = None

            self.use_cache_output = use_cache_output
            self.use_cache_input = use_cache_input

            # Save data
            if use_cache_output:
                self.cache()
        else:
            self.solver_subdir = cached.solver_subdir
            self.sA = cached.sA
            self.B = cached.B
            self.sL = cached.sL
            self.mesh = cached.mesh
            self.eps = cached.eps
            self.sig = cached.sig
            self.C_true = cached.C_true
            self.C_full = cached.C_full
            self.sensitivities = cached.sensitivities
            self.pixels = cached.pixels
            self.A_tensor = cached.A_tensor
            self.K_tensor = cached.K_tensor
            self.LHSBC = cached.LHSBC
            self.Aback = cached.Aback
            self.Kback = cached.Kback
            self.sensitivity_mesh = cached.sensitivity_mesh
            self.v_slice_sens = cached.v_slice_sens
            self.h_slice_sens1 = cached.h_slice_sens1
            self.h_slice_sens2 = cached.h_slice_sens2
            self.h_slice_sens3 = cached.h_slice_sens3
            self.sensitivity_electrode_pair = cached.sensitivity_electrode_pair
            self.sensitivity_single_electrode_sum = (
                cached.sensitivity_single_electrode_sum
            )
            self.sensitivity_total_sum = cached.sensitivity_total_sum

            self.t = cached.t
            self.V = cached.V
            self.Q = cached.Q

            self.use_cache_output = cached.use_cache_output
            self.use_cache_input = cached.use_cache_input

            self.params = params

            self.voltage_knode = cached.voltage_knode
            self.voltage_tnode = cached.voltage_tnode
            self.voltage_knode_for_all_transmitters = (
                cached.voltage_knode_for_all_transmitters
            )
            self.voltage_tnode_for_all_transmitters = (
                cached.voltage_tnode_for_all_transmitters
            )

        self.check_inputs()

    def check_inputs(self):
        if self.params.sensor.num_transmitter < 1:
            raise ValueError(
                "num_transmitter is less than 1. num_transmitter must be set to 1 or greater."
            )  # TODO implement maximum electrode number

        if self.params.sensor.c_probe is not None:
            if self.params.sensor.c_probe < 0:
                raise ValueError(
                    f"Probe capacitance is negative: c_probe: {self.params.sensor.c_probe}."
                )

        if any(x < 0 for x in self.params.sensor.c_receive_multiplexer_off):
            raise ValueError(
                f"Receive capacitance is negative: c_receive_multiplexer_off: {self.params.sensor.c_receive_multiplexer_off}."
            )

        if self.params.sensor.r_probe is not None:
            if self.params.sensor.r_probe < 0:
                raise ValueError(
                    f"Probe resistance is negative: r_probe: {self.params.sensor.r_probe}."
                )

        if any(x < 0 for x in self.params.sensor.r_pulldown_on_receive):
            raise ValueError(
                f"Receive resistance is negative: r_pulldown_on_receive: {self.params.sensor.r_pulldown_on_receive}."
            )

        if self.params.geometry.electrode_length <= 0:
            raise ValueError(
                f"Electrode length is too small. electrode_length: {self.params.geometry.electrode_length}"
            )

        if self.params.simulation.t_step <= 0:
            raise ValueError(
                f"Time step must be a positive number greater than zero. t_step: {self.params.simulation.t_step}"
            )

        if self.t is not None:
            if not np.isclose(
                self.params.simulation.t_step, self.t[1] - self.t[0]
            ):
                raise ValueError(
                    "Time step must be consistent with the input time series passed in."
                    + f" t_step from params: {self.params.simulation.t_step}, "
                    + f" t_step from input time series: {self.t[1] - self.t[0]}"
                )

    def check_simulation(self):
        # Check if voltage or charge contain any infinities or NaNs
        v_invalid = np.isinf(self.V)  # + np.isnan(self.V)
        q_invalid = np.isinf(self.Q)  # + np.isnan(self.Q)

        if True in v_invalid:
            raise ValueError(f"Voltages contain invalid values.\n {self.V}")
        elif True in q_invalid:
            raise ValueError(f"Charges contain invalid values.\n {self.Q}")

    def calculate_voltages(self, t, V_transmit, specific_probe_position=None):
        self.t = t
        self.V = np.zeros(
            [len(self.params.sensor.c_receive_multiplexer_off), len(t)]
        )
        self.Q = np.zeros(
            [
                len(self.params.sensor.c_receive_multiplexer_off)
                + self.params.sensor.num_wings,
                len(t),
            ]
        )
        self.Q[:] = np.NaN

        if (
            self.params.sensor.c_probe is None
        ):  # If no probe is present, can solve the forward problem in one probeless simulation
            logger.info(
                "No probe characteristics found - solving without a measurement probe"
            )
            self.V, self.Q = timestep_electric_field_DtoS(
                self.sA,
                self.B,
                self.sL,
                self.t,
                self.params.simulation.t_step,
                V_transmit,
                self.params.sensor.num_transmitter,
                self.params.sensor.c_receive_multiplexer_off,
                self.params.sensor.r_pulldown_on_receive,
                self.params.board,
                self.params.sensor.c_transmit_multiplexer_off,
                self.params.sensor.r_series,
                self.params.sensor.c_parasitic_forward_first_order,
                self.params.sensor.c_parasitic_backward_first_order,
            )
            logger.info(
                f"Forward solver finished for num_transmitter: {self.params.sensor.num_transmitter}"
            )

        else:  # Else will need to account for probe characteristics
            if (
                specific_probe_position is None
            ):  # If desired to find simulated solution with probe in one position
                for i in range(
                    len(self.params.sensor.c_receive_multiplexer_off)
                ):
                    if (
                        i != self.params.sensor.num_transmitter - 1
                    ):  # Probe each receive electrode in turn
                        C_electrode = copy.deepcopy(
                            self.params.sensor.c_receive_multiplexer_off
                        )
                        C_electrode[i] += self.params.sensor.c_probe
                        R_electrode = copy.deepcopy(
                            self.params.sensor.r_pulldown_on_receive
                        )
                        R_electrode[i] = 1 / (
                            (1 / R_electrode[i])
                            + (1 / self.params.sensor.r_probe)
                        )

                        V_solver, Q_solver = timestep_electric_field_DtoS(
                            self.sA,
                            self.B,
                            self.sL,
                            self.t,
                            self.params.simulation.t_step,
                            V_transmit,
                            self.params.sensor.num_transmitter,
                            C_electrode,
                            R_electrode,
                            self.params.board,
                            self.params.sensor.c_transmit_multiplexer_off,
                            self.params.sensor.r_series,
                            self.params.sensor.c_parasitic_forward_first_order,
                            self.params.sensor.c_parasitic_backward_first_order,
                        )

                        self.V[i, :] = V_solver[i, :]
                        self.Q[i, :] = Q_solver[i, :]

                        logger.info(
                            f"Forward solver finished for num_transmitter: {self.params.sensor.num_transmitter} with C_electrode: {C_electrode} and R_electrode: {R_electrode}"
                        )
                    else:
                        self.V[i, :] = V_transmit
                        self.Q[i, :] = None

                logger.info(
                    f"Forward solver finished for num_transmitter: {self.params.sensor.num_transmitter}"
                )
            else:
                C_electrode = copy.deepcopy(
                    self.params.sensor.c_receive_multiplexer_off
                )
                C_electrode[
                    specific_probe_position - 1
                ] += self.params.sensor.c_probe
                R_electrode = copy.deepcopy(
                    self.params.sensor.r_pulldown_on_receive
                )
                R_electrode[specific_probe_position - 1] = 1 / (
                    (1 / R_electrode[specific_probe_position - 1])
                    + (1 / self.params.sensor.r_probe)
                )

                self.V, self.Q = timestep_electric_field_DtoS(
                    self.sA,
                    self.B,
                    self.sL,
                    self.t,
                    self.params.simulation.t_step,
                    V_transmit,
                    self.params.sensor.num_transmitter,
                    C_electrode,
                    R_electrode,
                    self.params.board,
                    self.params.sensor.c_transmit_multiplexer_off,
                    self.params.sensor.r_series,
                    self.params.sensor.c_parasitic_forward_first_order,
                    self.params.sensor.c_parasitic_backward_first_order,
                )

                logger.info(
                    f"Forward solver finished for num_transmitter: {self.params.sensor.num_transmitter}"
                )

    def calculate_voltages_at_all_nodes(
        self, t, V_transmit, specific_probe_position=None
    ):
        """This function returns the T node and K node voltages for each electrode"""
        self.t = t
        self.voltage_knode = np.zeros(
            [len(self.params.sensor.c_receive_multiplexer_off), len(t)]
        )
        self.voltage_tnode = np.zeros(
            [len(self.params.sensor.c_receive_multiplexer_off), len(t)]
        )

        capacitance_knode_to_ground = copy.deepcopy(
            self.params.sensor.c_receive_multiplexer_off
        )
        resistance_knode_to_ground = copy.deepcopy(
            self.params.sensor.r_pulldown_on_receive
        )
        capacitance_tnode_to_ground = copy.deepcopy(
            self.params.sensor.c_transmit_multiplexer_off
        )
        resistance_tnode_to_knode = copy.deepcopy(self.params.sensor.r_series)

        if (
            self.params.sensor.c_probe is None
        ):  # If no probe is present, can solve the forward problem in one probeless simulation
            logger.info(
                "No probe characteristics found - solving without a measurement probe"
            )
            self.voltage_knode, self.voltage_tnode = (
                timestep_potentials_at_all_nodes(
                    A_sparse_fem_stiffness_matrix=self.sA,
                    B_sparse_fem_rhs_matrix=self.B,
                    L_sparse_fem_charge_matrix=self.sL,
                    time_vector=self.t,
                    time_step=self.params.simulation.t_step,
                    voltage_transmit=V_transmit,
                    num_transmitter=self.params.sensor.num_transmitter,
                    capacitance_knode_to_ground=capacitance_knode_to_ground,
                    resistance_knode_to_ground=resistance_knode_to_ground,
                    board_ID=self.params.board,
                    capacitance_tnode_to_ground=capacitance_tnode_to_ground,
                    resistance_tnode_to_knode=resistance_tnode_to_knode,
                    capacitance_parasitic_forward=self.params.sensor.c_parasitic_forward_first_order,
                    capacitance_parasitic_backward=self.params.sensor.c_parasitic_backward_first_order,
                )
            )
            logger.info(
                f"Forward solver finished for num_transmitter: {self.params.sensor.num_transmitter}"
            )
        else:
            raise NotImplementedError(
                "Option to consider c_probe is not implemented"
            )

    def calculate_voltages_for_all_transmitters(
        self,
        t,
        V_transmit,
        specific_probe_position=None,
        array_of_transmitters=None,
    ):
        """This function returns the T node and K node voltages for
        each electrode for all transmit electrodes in array_of_transmitters
        (all possible transmitters are considered if None is specified)"""
        self.t = t
        num_electrodes = len(self.params.sensor.c_receive_multiplexer_off)
        num_transmitters = num_electrodes
        self.voltage_knode_for_all_transmitters = np.zeros(
            [num_transmitters, num_electrodes, len(t)]
        )
        self.voltage_tnode_for_all_transmitters = np.zeros(
            [num_transmitters, num_electrodes, len(t)]
        )

        capacitance_knode_to_ground = copy.deepcopy(
            self.params.sensor.c_receive_multiplexer_off
        )
        resistance_knode_to_ground = copy.deepcopy(
            self.params.sensor.r_pulldown_on_receive
        )
        capacitance_tnode_to_ground = copy.deepcopy(
            self.params.sensor.c_transmit_multiplexer_off
        )
        resistance_tnode_to_knode = copy.deepcopy(self.params.sensor.r_series)

        if (
            self.params.sensor.c_probe is None
        ):  # If no probe is present, can solve the forward problem in one probeless simulation
            logger.info(
                "No probe characteristics found - solving without a measurement probe"
            )
            (
                self.voltage_knode_for_all_transmitters,
                self.voltage_tnode_for_all_transmitters,
            ) = timestep_potentials_for_all_transmitters(
                A_sparse_fem_stiffness_matrix=self.sA,
                B_sparse_fem_rhs_matrix=self.B,
                L_sparse_fem_charge_matrix=self.sL,
                time_vector=self.t,
                time_step=self.params.simulation.t_step,
                voltage_transmit=V_transmit,
                capacitance_knode_to_ground=capacitance_knode_to_ground,
                resistance_knode_to_ground=resistance_knode_to_ground,
                board_ID=self.params.board,
                capacitance_tnode_to_ground=capacitance_tnode_to_ground,
                resistance_tnode_to_knode=resistance_tnode_to_knode,
                capacitance_parasitic_forward=self.params.sensor.c_parasitic_forward_first_order,
                capacitance_parasitic_backward=self.params.sensor.c_parasitic_backward_first_order,
                array_of_transmitters=array_of_transmitters,
            )
            logger.info(
                f"Forward solver finished for num_transmitter: {self.params.sensor.num_transmitter}"
            )
        else:
            raise NotImplementedError(
                "Option to cosider c_probe is not implemented"
            )

    def cache(self):
        """
        Save current state to file.
        """
        create_cache(hash_dictionary(asdict(self.params)), self)

    def simulate(
        self,
        t,
        V_transmit,
        specific_probe_position=None,
        use_cached_voltage=CACHE_INPUT_VOLTAGE,
    ):
        # Calculate voltages if V is empty or use_cached = False
        if not use_cached_voltage or self.V is None:
            self.calculate_voltages(t, V_transmit, specific_probe_position)
            # Cache results
            if self.use_cache_output:
                self.cache()

        self.check_simulation()
        return self.V, self.Q

    def check_voltage_calculation_at_all_nodes(self):
        # Check if the calculated array contains any infinities
        voltage_knode_invalid = np.isinf(self.voltage_knode)
        voltage_tnode_invalid = np.isinf(self.voltage_tnode)

        if True in voltage_knode_invalid:
            raise ValueError(
                f"K node voltages contain invalid values.\n {self.voltage_knode}"
            )
        elif True in voltage_tnode_invalid:
            raise ValueError(
                f"T node voltages contain invalid values.\n {self.voltage_tnode}"
            )

    def export_voltages_at_all_nodes(
        self,
        t,
        V_transmit,
        specific_probe_position=None,
        use_cached_voltage=CACHE_INPUT_VOLTAGE,
    ):
        if not use_cached_voltage or self.voltage_knode is None:
            self.calculate_voltages_at_all_nodes(
                t,
                V_transmit,
                specific_probe_position,
            )
        self.check_voltage_calculation_at_all_nodes()
        return self.voltage_knode, self.voltage_tnode

    def check_voltage_calculation_for_all_transmitters(self):
        # Check if the calculated array contains any infinities
        voltage_knode_for_all_transmitters_invalid = np.isinf(
            self.voltage_knode_for_all_transmitters
        )
        voltage_tnode_for_all_transmitters_invalid = np.isinf(
            self.voltage_tnode_for_all_transmitters
        )

        if True in voltage_knode_for_all_transmitters_invalid:
            raise ValueError(
                f"K node voltages for all transmitters contain invalid values.\n {self.voltage_knode_for_all_transmitters}"
            )
        elif True in voltage_tnode_for_all_transmitters_invalid:
            raise ValueError(
                f"T node voltages for all transmitters contain invalid values.\n {self.voltage_tnode_for_all_transmitters}"
            )

    def export_voltages_for_all_transmitters(
        self,
        t,
        V_transmit,
        array_of_transmitters=None,
        use_cached_voltage=CACHE_INPUT_VOLTAGE,
    ):
        if (
            not use_cached_voltage
            or self.voltage_knode_for_all_transmitters is None
        ):
            self.calculate_voltages_for_all_transmitters(
                t, V_transmit, array_of_transmitters=array_of_transmitters
            )
        self.check_voltage_calculation_for_all_transmitters()

        return (
            self.voltage_knode_for_all_transmitters,
            self.voltage_tnode_for_all_transmitters,
        )

    def export_voltages_for_all_transmitters_to_devicedata(
        self,
        t: np.ndarray,
        V_transmit: np.ndarray,
        array_of_transmitters=None,
        use_cached_voltage=CACHE_INPUT_VOLTAGE,
    ) -> DeviceDataSynthetic:
        """Export pre-computed voltages to DeviceData instance."""

        self.export_voltages_for_all_transmitters(
            t, V_transmit, array_of_transmitters, use_cached_voltage
        )

        num_electrodes = len(self.params.sensor.c_receive_multiplexer_off)

        data = np.empty((2 + 2 * (num_electrodes * num_electrodes), len(t)))
        data[0, :] = t[:] * MICROSECONDS_TO_SECONDS
        data[1, :] = V_transmit[:]
        for i in range(num_electrodes):
            for j in range(num_electrodes):
                idx = i * num_electrodes + j
                data[2 + 2 * idx, :] = self.voltage_tnode_for_all_transmitters[
                    i
                ][j]
                data[2 + 2 * idx + 1, :] = (
                    self.voltage_knode_for_all_transmitters[i][j]
                )

        return DeviceDataSynthetic.create(
            data_signals=data, num_electrodes=num_electrodes
        )

    def get_board_height(self):
        """Function to get the height of the board (y coordinate).

        Returns:
            float: Board height (y coordinate) in FreeFem coordinate space
        """
        if self.params.board == "P1000_009":
            board_height = self.params.geometry.board_height
        elif self.params.board in [
            "P1000_001",
            "P1000_004",
            "P1000_006",
            "P3000_005",
        ]:
            board_height = self.params.geometry.pcb_substrate_height
        else:
            raise ValueError(f"Unknown board type {self.params.board}.")

        x_pcb_substrate_y = (
            -0.5 * board_height
            - (1.0 / 6.0) * self.params.geometry.domain_height
            + self.params.geometry.electrode_height
        )  # Derived parameter

        height_of_board = x_pcb_substrate_y + board_height
        return height_of_board

    def compute_mesh_epsilon(self, epsilon_matrix, update_eps=True):
        epsilon_array = np.transpose(epsilon_matrix).flatten()
        epsilon = dot_product_lists(self.pixels, epsilon_array)
        epsilon_indicator = dot_product_lists(
            self.pixels, np.ones(len(self.pixels))
        )  # Indices of mesh elements that are in the pixels

        # Update the eps values of the pixels only
        tmp = np.multiply(self.eps, (1 - epsilon_indicator)) + np.multiply(
            EPSILON_0 * epsilon_indicator, epsilon
        )

        # Choose if to return or update in object

        if update_eps:
            self.eps = tmp
        else:
            return tmp

    def build_FE_matrices(self, epsilon_matrix):
        """
        Builds FEM matrices given epsilon distribution
        """
        epsilon_vector = EPSILON_0 * np.transpose(epsilon_matrix).flatten()
        A = dot_product_lists(epsilon_vector, self.A_tensor)
        A = A + self.LHSBC + self.Aback

        K = dot_product_lists(epsilon_vector, self.K_tensor)
        K = K + self.Kback
        return A, K

    def calculate_capacitance_matrix(self, epsilon_matrix):
        """
        Computes the capacitance matrix given a pixel distribution and vector of permittivities.
        Args:
        epsilon_vector: vector of permittivites epsilon_vector[i] = permittivity of ith pixel.
        Output:
        C_matrix: matrix of capacitances. Size is N_electode*(N_electrode-1)/2
        """
        # Define solver
        A, K = self.build_FE_matrices(epsilon_matrix)
        iA = sps.linalg.splu(A)  # Set solver
        # Define RHS
        U = np.eye(
            np.shape(self.B)[1]
        )  # Identity matrix, size = number of electrodes
        b = self.B @ U  # Construct RHS
        # Solve
        uu = iA.solve(b)  # Execute solver. By default along each column of b.
        # Measure capacitance
        M = -1 * K.T * uu  # Measure charge
        M[np.eye(np.shape(M)[0], dtype=bool)] = (
            0.0  # Set self-capacitances to zero.
        )
        return M

    def calculate_sensitivity_matrix(
        self,
        epsilon_matrix,
        eps_step=0.1,
        scale_output=False,
        permittivity_max=1.0,
    ):
        """
        Function to compute the sensitivity matrix (linearised Jacobian) about the
        current permittivity given by epsilon_vector.
        Args:
        epsilon_vector: vector of permittivites epsilon_vector[i] = permittivity of ith pixel.
        Output:
        sensitivity_matrix: computed sensitivity matrix of size
        """
        # Compute reference measurements
        Mref = self.calculate_capacitance_matrix(epsilon_matrix)
        N_Electrodes = np.shape(self.B)[1]
        Nx, Ny = np.shape(epsilon_matrix)
        N_Pixels = Nx * Ny
        sensitivity_matrix = np.ndarray(
            [int(N_Electrodes * (N_Electrodes - 1) / 2), N_Pixels]
        )  # Initialise sensitivity matrix
        for i in range(Nx):
            for j in range(Ny):
                delta_epsilon = epsilon_matrix.copy()
                delta_epsilon[i, j] += eps_step
                M = self.calculate_capacitance_matrix(delta_epsilon)
                Mdiff = M - Mref
                Mdiff = Mdiff / eps_step  # Divide through by eps_step.
                sensitivity_matrix[:, i + Nx * j] = Mdiff[
                    np.triu_indices(N_Electrodes, k=1)
                ]
        if (
            scale_output
        ):  # If scaling the sensitivity matrix by the largest permittivity change
            delta_epsilon = epsilon_matrix.copy() + permittivity_max
            Mmax = self.calculate_capacitance_matrix(delta_epsilon)
            scale_factors = (
                Mmax[np.triu_indices(N_Electrodes, k=1)]
                - Mref[np.triu_indices(N_Electrodes, k=1)]
            )
            sensitivity_matrix = (
                sensitivity_matrix / scale_factors[:, np.newaxis]
            )

        return sensitivity_matrix

    def visualise(self, save_fig=None):
        return plot_boundary_values(
            self.t,
            self.V,
            self.Q,
            self.params.sensor.num_transmitter,
            save_fig=save_fig,
        )

    def visualise_field(self, t_inspect, save_fig=None):
        def find_nearest_idx(array, value):
            array = np.asarray(array)
            return (np.abs(array - value)).argmin()

        idx_inspect = find_nearest_idx(self.t, t_inspect)

        _, V_field = compute_electric_field_DtoS(
            self.V[:, idx_inspect],
            self.sA,
            self.B,
            self.sL,
        )
        return plot_electric_field(self.mesh, V_field, save_fig=save_fig)

    def visualise_epsilon(self, save_fig=None, plot_mesh=True, cmap="jet"):
        if self.eps is not None:
            return plot_geometry(
                self.mesh,
                self.eps,
                "Permittivity",
                save_fig=save_fig,
                plot_mesh=plot_mesh,
                cmap=cmap,
            )
        else:
            raise RuntimeError(
                "Epsilon values not available for visualisation!"
            )

    def visualise_sigma(self, save_fig=None, plot_mesh=True, cmap="jet"):
        if self.sig:
            return plot_geometry(
                self.mesh,
                self.sig,
                "Conductivity",
                save_fig=save_fig,
                plot_mesh=plot_mesh,
                cmap=cmap,
            )
        else:
            raise RuntimeError("Sigma values not available for visualisation!")

    def visualise_sensitivity(self, elec_1, elec_2, save_fig=None):
        if self.sensitivities is not None:
            if elec_1 < elec_2:
                sensitivity_key = f"E{elec_1-1}E{elec_2-1}"
            else:
                sensitivity_key = f"E{elec_2-1}E{elec_1-1}"
            return plot_geometry(
                self.mesh,
                self.sensitivities[sensitivity_key],
                "Sensitivity",
                save_fig=save_fig,
                plot_mesh=False,
            )
        else:
            raise RuntimeError(
                "Sensitivity map values not available for visualisation!"
            )


class SolverForwardP1000_00X(SimulationModule):
    """
    Forward solver_artefacts for a 2D voltage signal for the solver_artefacts board
    Attributes:
        solver_subdir (str): Subdirectory for the solver.
        sA: Solver matrix A.
        B: Solver matrix B.
        sL: Solver matrix L.
        mesh: Mesh configuration.
        eps: Permittivity.
        sig: Conductivity.
        C_true: True capacitance.
        C_full: Full capacitance.
        sensitivities: Sensitivity values.
        pixels: Pixel configuration.
        A_tensor: Tensor A.
        K_tensor: Tensor K.
        LHSBC: Left-hand side boundary conditions.
        Aback: Background matrix A.
        Kback: Background matrix K.
        sensitivity_mesh: Sensitivity mesh.
        v_slice_sens: Vertical slice sensitivity.
        h_slice_sens1: Horizontal slice sensitivity 1.
        h_slice_sens2: Horizontal slice sensitivity 2.
        h_slice_sens3: Horizontal slice sensitivity 3.
        sensitivity_electrode_pair: Sensitivity for electrode pairs.
        sensitivity_single_electrode_sum: Sensitivity sum for single electrodes.
        sensitivity_total_sum: Total sensitivity sum.
        t_step (float): Time step for simulation.
        electrode_length (float): Length of the electrode.
        num_transmitter (int): Number of transmitters.
        c_receive_multiplexer_off (list): Capacitance of receive multiplexer when off.
        r_pulldown_on_receive (list): Resistance of pulldown on receive.
        c_probe (float): Capacitance of the probe.
        r_probe (float): Resistance of the probe.
        c_transmit_multiplexer_off (float): Capacitance of transmit multiplexer when off.
        r_series (float): Series resistance.
        c_parasitic_forward_first_order (float): Parasitic capacitance forward first order.
        c_parasitic_backward_first_order (float): Parasitic capacitance backward first order.
        params: Parameters for the forward solver.
        t: Time variable.
        V: Voltage variable.
        Q: Charge variable.
    Methods:
        __init__(params, solver_dir, solver_file):
            Initializes the solver with given parameters, solver directory, and solver file.
        check_inputs():
            Validates the input parameters for the solver.
        check_simulation():
            Checks if the voltage or charge contain any infinities or NaNs.
        calculate_voltages(t, V_transmit):
            Calculates the voltages for the given time and transmit voltage.
        simulate(t, V_transmit):
            Runs the simulation for the given time and transmit voltage.
        visualise():
            Visualizes the boundary values of the simulation.
    """

    def __init__(
        self,
        params: ForwardSolverParams,
        solver_dir=FREEFEM_DIR + "/model_solver/",
        solver_file="model_solver.edp",
    ):
        params.board = "P1000_00X"
        (
            self.solver_subdir,
            self.sA,
            self.B,
            self.sL,
            self.mesh,
            self.eps,
            self.sig,
            self.C_true,
            self.C_full,
            self.sensitivities,
            self.pixels,
            self.A_tensor,
            self.K_tensor,
            self.LHSBC,
            self.Aback,
            self.Kback,
            self.sensitivity_mesh,
            self.v_slice_sens,
            self.h_slice_sens1,
            self.h_slice_sens2,
            self.h_slice_sens3,
            self.sensitivity_electrode_pair,
            self.sensitivity_single_electrode_sum,
            self.sensitivity_total_sum,
        ) = setup_solver_environment(params, solver_dir, solver_file)

        self.t_step = params.simulation.t_step
        self.electrode_length = params.geometry.electrode_length

        self.num_transmitter = params.sensor.num_transmitter
        self.c_receive_multiplexer_off = (
            params.sensor.c_receive_multiplexer_off
        )
        self.r_pulldown_on_receive = params.sensor.r_pulldown_on_receive
        self.c_probe = params.sensor.c_probe
        self.r_probe = params.sensor.r_probe
        self.c_transmit_multiplexer_off = (
            params.sensor.c_transmit_multiplexer_off
        )
        self.r_series = params.sensor.r_series
        self.c_parasitic_forward_first_order = (
            params.sensor.c_parasitic_forward_first_order
        )
        self.c_parasitic_backward_first_order = (
            params.sensor.c_parasitic_backward_first_order
        )

        self.params = params
        self.t = None
        self.V = None
        self.Q = None
        self.check_inputs()

    def check_inputs(self):
        if self.num_transmitter < 1:
            raise ValueError(
                "num_transmitter is less than 1. num_transmitter must be set to 1 or greater."
            )  # TODO implement maximum electrode number

        if self.c_probe < 0:
            raise ValueError(
                f"Probe capacitance is negative: c_probe: {self.c_probe}."
            )

        if any(x < 0 for x in self.c_receive_multiplexer_off):
            raise ValueError(
                f"Receive capacitance is negative: c_receive_multiplexer_off: {self.c_receive_multiplexer_off}."
            )

        if self.r_probe < 0:
            raise ValueError(
                f"Probe resistance is negative: r_probe: {self.r_probe}."
            )

        if any(x < 0 for x in self.r_pulldown_on_receive) < 0:
            raise ValueError(
                f"Receive resistance is negative: r_pulldown_on_receive: {self.r_pulldown_on_receive}."
            )

        if self.electrode_length <= 0:
            raise ValueError(
                f"Electrode length is too small. electrode_length: {self.electrode_length}"
            )

        if self.t_step <= 0:
            raise ValueError(
                f"Time step must be a positive number greater than zero. t_step: {self.t_step}"
            )

    def check_simulation(self):
        # Check if voltage or charge contain any infinities or NaNs
        v_invalid = np.isnan(self.V) + np.isinf(self.V)
        q_invalid = np.isnan(self.Q) + np.isinf(self.Q)

        if True in v_invalid:
            raise ValueError(f"Voltages contain invalid values.\n {self.V}")
        elif True in q_invalid:
            raise ValueError(f"Charges contain invalid values.\n {self.Q}")

    def calculate_voltages(self, t, V_transmit):
        self.t = t

        # Configure electrode capacitances and resistances
        C_electrode = copy.deepcopy(self.c_receive_multiplexer_off)
        R_electrode = copy.deepcopy(self.r_pulldown_on_receive)
        if (
            self.num_transmitter == 1
        ):  # If transmitter is first electrode, set up probe on second electrode
            C_electrode[1] += self.c_probe
            R_electrode[1] = 1 / ((1 / R_electrode[1]) + (1 / self.r_probe))
        else:  # If transmitter is second electrode, set up probe on first electrode
            C_electrode[0] += self.c_probe
            R_electrode[0] = 1 / ((1 / R_electrode[0]) + (1 / self.r_probe))

        self.V, self.Q = timestep_electric_field_DtoS(
            self.sA,
            self.B,
            self.sL,
            self.t,
            self.t_step,
            V_transmit,
            self.num_transmitter,
            C_electrode,
            R_electrode,
            self.params.board,
            self.c_transmit_multiplexer_off,
            self.r_series,
            self.c_parasitic_forward_first_order,
            self.c_parasitic_backward_first_order,
        )
        logger.info(
            f"Forward solver finished for num_transmitter: {self.num_transmitter}"
        )

    def simulate(self, t, V_transmit):
        self.calculate_voltages(t, V_transmit)
        self.check_simulation()
        return self.V, self.Q

    def visualise(self):
        return plot_boundary_values(
            self.t,
            self.V,
            self.Q,
            self.num_transmitter,
        )


close_logger(logger)
