import os
import shutil

import numpy as np

# from forwardSolver.scripts.solver_forward_P1000 import SolverForwardP1000
from forwardSolver.scripts.utils.constants import DELETE_FREEFEM_FILES, FREEFEM_DIR
from forwardSolver.scripts.utils.freefem import (
    read_freefem_metrics_to_dict,
    write_array_to_freefem_file,
)
from forwardSolver.scripts.utils.logging import close_logger, get_logger
from forwardSolver.scripts.utils.signal_processing_P1000 import SignalProcessorP1000

logger = get_logger(__name__)


class ExperimentMetric:
    """
    Module contains static methods which return dictionaries.
    Each key of the dict will be logged as the name of the metric and the value will be recorded alongside it in MLFlow
    """

    # Metrics for the (physical) Experimental data
    @staticmethod
    def peak_voltage_ratio(V_sim, V_exp):
        """
        Calculate ratio difference in peak values between simulated and experimental voltages
        """
        N_electrodes = V_sim.shape[0]

        max_voltages_sim = [max(V_sim[i, :]) for i in range(N_electrodes)]
        max_voltages_exp = [max(V_exp[i, :]) for i in range(N_electrodes)]
        peak_voltage_ratio = np.array(max_voltages_sim) / np.array(max_voltages_exp)

        result = {
            f"peak_voltage_ratio_electrode_{i:02}": peak_voltage_ratio[i]
            for i in range(len(peak_voltage_ratio))
        }
        return result

    @staticmethod
    def estimated_capacitance(params, t, V):
        """
        Return the estimated capacitances from the signal processor module
        """
        trans = params.sensor.num_transmitter - 1
        c_mean = SignalProcessorP1000().calculate(
            t,
            V,
            trans + 1,
            params.sensor.c_receive_multiplexer_off,
            params.sensor.r_pulldown_on_receive,
        )

        return {f"cap_est_{trans}_{rec}": c_mean[rec] for rec in range(c_mean.shape[0])}

    @staticmethod
    def peak_voltages(V):
        """
        Return the maximum (absolute) voltage on each electrode and wing
        """

        result = {
            f"peak_voltage_electrode_{i}": np.abs(V[i]).max() for i in range(V.shape[0])
        }
        return result

    @staticmethod
    def sum_voltage(V):
        """
        Return the sum of absolute voltages over all electrodes
        """
        return {"sum_volts": np.nansum(np.absolute(V))}

    @staticmethod
    def calculate_voltage_metrics(t, V_air_raw, V_raw, num_transmitter):
        def find_idx_last_value_above(array, value):
            flipped_array = np.flip(array)
            flipped_index = np.argmax(flipped_array > value)
            if flipped_index == 0:
                return 0
            return (len(array) - 1) - flipped_index

        V_air = np.delete(V_air_raw, num_transmitter - 1, axis=0)
        V = np.delete(V_raw, num_transmitter - 1, axis=0)

        max_V = np.amax(V, axis=1)
        max_V_air = np.amax(V_air, axis=1)

        diff_max_V = max_V - max_V_air

        V_diff = abs(V - V_air)
        max_V_diff = np.amax(V_diff, axis=1)

        tau = [
            t[find_idx_last_value_above(V[i, :], max_V[i] / np.exp(1))]
            for i in range(len(max_V))
        ]
        tau_air = [
            t[find_idx_last_value_above(V_air[i, :], max_V_air[i] / np.exp(1))]
            for i in range(len(max_V))
        ]

        mean_tau = -1 if any(elem == 0 for elem in tau) else np.mean(tau)
        mean_tau_air = -1 if any(elem == 0 for elem in tau) else np.mean(tau_air)
        diff_tau = mean_tau - mean_tau_air

        return {
            "mean_max_receive_volt_phantom": np.mean(
                max_V
            ),  # mean of maximum voltages on all except trans electrode (w phantom)
            "mean_max_receive_volt_air": np.mean(
                max_V_air
            ),  # mean of maximum voltages on all except trans electrode (w/o phantom)
            "mean_max_receive_volt_phantom_air_diff": np.mean(
                max_V_diff
            ),  # elementwise diff between phantom and air -> calc max -> calc mean
            "mean_tau_phantom": mean_tau,  # calc tau from exponential decay 1/e (w phantom)
            "mean_tau_air": mean_tau_air,  # calc tau from exponential decay 1/e (w/o phantom)
            "max_receive_volt_phantom_air_diff": diff_max_V,
            "mean_tau_phantom_air_diff": diff_tau,
        }

    # Metrics for the Forward Solver
    @staticmethod
    def true_capacitance(params, C_true):
        """
        Return the true capacitances from FreeFem
        """
        cap_true_dict = {}
        num_electrodes = len(params.sensor.c_receive_multiplexer_off)

        for transmit_electrode in range(num_electrodes):
            for receive_electrode in range(num_electrodes):
                if transmit_electrode <= receive_electrode:
                    cap_true_dict[
                        f"cap_true_{transmit_electrode}_{receive_electrode}"
                    ] = C_true[transmit_electrode, receive_electrode]
        return cap_true_dict

    # Peak charges
    @staticmethod
    def peak_charges(params, Q):
        """
        Return the maximum (absolute) charge on each electrode and wing
        """
        n_wings = params.sensor.num_wings

        result = {
            f"peak_charge_electrode_{i}": np.abs(Q[i]).max()
            for i in range(Q.shape[0] - n_wings)
        }
        result.update(
            {
                f"peak_charge_wing_{i}": np.abs(Q[i]).max()
                for i in range(Q.shape[0] - n_wings, Q.shape[0])
            }
        )
        return result

    @staticmethod
    def sum_charge(Q):
        """
        Return the sum of the absolute charge over all electrodes and wings
        """
        return {"sum_charge": np.nansum(np.absolute(Q))}

    # Metrics for the Inverse Solver
    @staticmethod
    def rms_permittivity_difference(eps_true, eps_reco):
        """
        Returns a simple RMS percentage error between the true and estimated pixel permittivities (normalised to initial permittivities).
        """
        relative_error = np.divide(eps_reco, eps_true) - 1.0

        return {
            "reco_rms_percentage_error": np.sqrt(np.nanmean(np.square(relative_error)))
            * 100
        }

    @staticmethod
    def most_deviant_pixel(eps_true, eps_reco):
        """
        Returns the percentage error in the most incorrectly estimated pixel.
        """
        relative_error = np.divide(eps_reco, eps_true) - 1.0
        relative_error = relative_error.flatten()
        max_deviation = relative_error[np.nanargmax(np.abs(relative_error))] * 100
        return {"most_deviant_pixel_error": max_deviation}

    @staticmethod
    def iterations_to_specific_percent_error(eps_true, solver_inverse, error=20):
        """
        Returns the number of iterations taken to reach a specific RMS percentage error
        """
        for count, estimate in enumerate(solver_inverse.eps_estimated):
            # function returns dict with only one key, value pair. Extract the value.
            rmspe = list(
                ExperimentMetric.rms_permittivity_difference(
                    eps_true, estimate
                ).values()
            )[0]
            if rmspe <= error:
                return {f"iterations_to_{error}_percent_error": count}

        # Return NaN if specific percent error is not reached
        return {f"iterations_to_{error}_percent_error": np.nan}

    @staticmethod
    def reco_iterations(eps_true, solver_inverse):
        """
        Returns the capacitance error and RMS percentage error for each inverse solver iteration.
        """
        output_dict = {}
        for count, estimate in enumerate(solver_inverse.eps_estimated):
            # function returns dict with only one key, value pair. Extract the value.
            rmspe = list(
                ExperimentMetric.rms_permittivity_difference(
                    eps_true, estimate
                ).values()
            )[0]

            output_dict.update(
                {
                    f"reco_iter_{count}_capacitance_error": solver_inverse.error[count],
                    f"reco_iter_{count}_rms_percentage_error": rmspe,
                }
            )

        return output_dict

    @staticmethod
    def compute_epsilon_errors_between_forward_solvers(
        forward_solver_1, forward_solver_2
    ):
        """Compares two forward solver permittivity maps and returns dictionary of L1 and L2 errors between them.

        Args:
            forward_solver_1 (SolverForwardP1000):

            forward_solver_2 (SolverForwardP1000):

        Returns:
            dict: Dictionary of L1 and L2 errors between the two forward solver epsilon maps
        """

        height_of_board = forward_solver_1.get_board_height()

        return ExperimentMetric._compute_mesh_func_diff(
            forward_solver_1.mesh,
            forward_solver_2.mesh,
            forward_solver_1.eps,
            forward_solver_2.eps,
            height_of_board,
        )

    @staticmethod
    def _compute_mesh_func_diff(mesh_1, mesh_2, func_1, func_2, ycutoff):
        """Takes two functions defined on separate meshes and interpolates to get the difference between the two.

        Args:
            mesh_1 (mesh): Mesh for first object
            mesh_2 (mesh): Mesh for second object
            func_1 (array): Values defined on first mesh
            func_2 (array): Values defined on second mesh

        Returns:
            dict: Dictionary of L1 and L2 errors between the two functions (defined on meshes)
        """
        temporary_path = FREEFEM_DIR + "/temp"

        if not os.path.exists(temporary_path):
            os.makedirs(temporary_path)

        # Write meshes to file
        mesh1_filename = os.path.join(temporary_path, "Th1.vtk")
        mesh2_filename = os.path.join(temporary_path, "Th2.vtk")

        mesh_1.write(mesh1_filename)
        mesh_2.write(mesh2_filename)

        # Write eps functions to file
        eps1_filename = os.path.join(temporary_path, "eps1.txt")
        eps2_filename = os.path.join(temporary_path, "eps2.txt")

        write_array_to_freefem_file(func_1, eps1_filename)
        write_array_to_freefem_file(func_2, eps2_filename)

        # Run FreeFem++ metrics compute
        metrics_file = os.path.join(temporary_path, "metrics.txt")

        os_command = (
            f"FreeFem++ -nw -ne {FREEFEM_DIR+'/FreeFemMetrics.edp'} "
            f"Th1 {mesh1_filename} "
            f"f1 {eps1_filename} "
            f"Th2 {mesh2_filename} "
            f"f2 {eps2_filename} "
            f"ycutoff {ycutoff} "
            f"tempdirec {temporary_path} "
            f"> {metrics_file} "
        )
        os.system(os_command)

        # Read metrics file
        metrics_file = os.path.join(temporary_path, "metrics.txt")
        error_dict = read_freefem_metrics_to_dict(metrics_file)

        # Clean up temporary files generated
        if DELETE_FREEFEM_FILES:
            try:
                shutil.rmtree(temporary_path)
            except Exception as err:
                logger.error(f"Unable to change directory!\n{err}")
        return error_dict

    @staticmethod
    def shape_similarity():
        """
        Returns some measure of the correlation between the shape of the true and esimated permittivity maps. Ignores absolute permittivity values.
        """
        raise NotImplementedError

    @staticmethod
    def matrix_norm_of_difference(C1, C2, ord=None):
        """
        Computes norm between two matrices C1 and C2.
        "Ord = None" means Frobenius norm is used. Others are possible, see: https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html

        Args:
            C1 matrix of shape (n, m)
            C2 matrix of shape (n, m)

        Returns:
            Frobenius norm of C1-C2.

        """
        C = C1 - C2  # Compute difference between capacitance matrices
        norm = np.linalg.norm(C, ord=ord)
        norm2 = np.linalg.norm(C1, ord=ord)
        return {
            "capacitance_matrix_norm_diff": norm,
            "capacitance_matrix_norm_diff_relative": 100 * norm / norm2,
        }

    @staticmethod
    def compute_capactiance_matrix_difference(forward_solver_1, forward_solver_2):
        """Computes the Frobenius norm between the computed capacitance matrices from two Forward Solvers

        Args:
            forward_solver_1 (SolverForwardP1000):

            forward_solver_2 (SolverForwardP1000):

        Returns:
            list: norm, relative norm
        """
        return ExperimentMetric.matrix_norm_of_difference(
            forward_solver_1.C_true, forward_solver_2.C_true
        )


# TODO split this module up into Inverse and Forward solver metrics
close_logger(logger)
