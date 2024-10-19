import numpy as np

from forwardSolver.scripts.utils.constants import (
    DERIVATIVE_EDGE_ORDER,
    NUM_ELEM_DERIVATIVE_IGNORE,
)
from forwardSolver.scripts.utils.logging import close_logger, get_logger
from forwardSolver.scripts.utils.modules import CalculationModule

logger = get_logger(__name__)


class SignalProcessorP1000(CalculationModule):
    """
    Capacitance estimation between electrodes, based on the FEM_intro.lyx file
    """

    def calculate_single_capacitance(
        self,
        t,
        V,
        num_transmitter,
        N_receiver,
        c_receive_multiplexer_off,
        r_pulldown_on_receive,
    ):
        """
        Simple approach to extract capacitance estimate based on entire signal
        """
        if num_transmitter == N_receiver:
            C_material = np.nan
        else:
            B = V[N_receiver - 1, -1] - V[N_receiver - 1, 0]
            D = V[num_transmitter - 1, -1] - V[num_transmitter - 1, 0]
            F = (
                np.trapz(V[N_receiver - 1, :], x=t)
                / r_pulldown_on_receive[N_receiver - 1]
            )

            C_material = -(
                F + B * c_receive_multiplexer_off[N_receiver - 1]
            ) / (B - D)
        return C_material

    def calculate(
        self,
        t,
        V,
        num_transmitter,
        c_receive_multiplexer_off,
        r_pulldown_on_receive,
    ):
        """
        Calculate an array of capacitances between the transmit electrode num_transmitter and each receive electrode.
        The function requires
        t = np lin space
        V = np matrix [ len(c_receive_multiplexer_off), len(t) ]
        """
        capacitance_array = np.zeros(
            len(c_receive_multiplexer_off)
        )  # create an empty array
        receiver = 1  # receiver numbers start from 1 -> N
        for i in range(len(capacitance_array)):
            capacitance_array[i] = self.calculate_single_capacitance(
                t,
                V,
                num_transmitter,
                receiver + i,
                c_receive_multiplexer_off,
                r_pulldown_on_receive,
            )
        logger.info(
            f"Effective capacitance array estimate: {capacitance_array}"
        )
        return capacitance_array

    def calculate_alt(
        self,
        t,
        V,
        num_transmitter,
        N_receiver,
        c_receive_multiplexer_off,
        r_pulldown_on_receive,
    ):
        """
        Replicating simple approach but manipulating the equation to be more similar to an A'Ax=A'b formulation
        """
        VT = V[num_transmitter - 1, :]
        VR = V[N_receiver - 1, :]

        X1 = VT[-1] - VT[0]
        X2 = VR[-1] - VR[0]

        Y = np.trapz(VR, x=t) / r_pulldown_on_receive[N_receiver - 1]

        A = X1 - X2
        B = Y + c_receive_multiplexer_off[N_receiver - 1] * X2

        AA = A * A
        BB = A * B

        C_material = BB / AA

        logger.info(
            f"Effective capacitance estimate between electrodes {num_transmitter} and {N_receiver}: {C_material:.3e}"
        )
        return C_material

    def calculate_derivative(self, y, x, order=DERIVATIVE_EDGE_ORDER):
        """
        Numerical derivative taken with `order` number of points.
        """
        return np.gradient(y, x, edge_order=order)

    def calculate_true_capacitance(self, V, Q, electrode_1, electrode_2):
        """
        Calculation of mutual capacitance between two electrodes, given true voltages and charges.
        See: https://en.wikipedia.org/wiki/Capacitance#Mutual_capacitance

        Note: time_step should be small
        """
        p11 = self.calculate_derivative(
            V[electrode_1], Q[electrode_1]
        )  # Qmat[:11,:]
        p22 = self.calculate_derivative(V[electrode_2], Q[electrode_2])
        p12 = self.calculate_derivative(V[electrode_1], Q[electrode_2])
        p21 = self.calculate_derivative(V[electrode_2], Q[electrode_1])

        cap_array = np.ones((len(p11))) * np.nan
        for i in range(len(p11)):
            cap_array[i] = 1 / ((p11[i] + p22[i]) - (p12[i] + p21[i]))
        return cap_array

    def calculate_true_capacitance_array(self, V, Q, transmit_electrode):
        def c(i, j):
            return self.calculate_true_capacitance(V, Q, i, j)

        num_e = V.shape[0]
        c_mean = np.ones((num_e)) * np.nan
        c_std = np.ones((num_e)) * np.nan
        for i in range(num_e):
            c_mean[i] = np.mean(
                c(transmit_electrode, i)[
                    NUM_ELEM_DERIVATIVE_IGNORE:-NUM_ELEM_DERIVATIVE_IGNORE
                ]
            )  # ignore some elements from the beginning and end.
            # Two reasons: derivative taken differently than middle numbers and first points suffer from NaN (due to zero)
            c_std[i] = np.std(
                c(transmit_electrode, i)[
                    NUM_ELEM_DERIVATIVE_IGNORE:-NUM_ELEM_DERIVATIVE_IGNORE
                ]
            )
        return c_mean, c_std

    def calculate_true_capacitance_matrix(self, V, Q):
        """
        Given voltages and charges on electrodes, returns the mutual capacitance matrix (symmetric about the diagonal).

        Returns the mutual capacitance matrix mean values and standard deviation as two matrices:
        Capacitance between electrodes 6 and 5 is: c_mean[5, 4] +- c_std[5, 4]
        """

        num_e = V.shape[0]
        c_mean = np.ones((num_e, num_e)) * np.nan
        c_std = np.ones((num_e, num_e)) * np.nan

        cap_vs_time = self.calculate_true_capacitance_matrix_over_time(V, Q)

        # Can be sped up by just making i,j == j,i
        for i in range(num_e):
            for j in range(num_e):
                c_mean[i, j] = np.mean(
                    cap_vs_time[
                        i,
                        j,
                        NUM_ELEM_DERIVATIVE_IGNORE:-NUM_ELEM_DERIVATIVE_IGNORE,
                    ]
                )  # ignore some elements from the beginning and end.
                # Two reasons: derivative taken differently than middle numbers and first points suffer from NaN (due to zero)
                c_std[i, j] = np.std(
                    cap_vs_time[
                        i,
                        j,
                        NUM_ELEM_DERIVATIVE_IGNORE:-NUM_ELEM_DERIVATIVE_IGNORE,
                    ]
                )
        return c_mean, c_std

    def calculate_true_capacitance_matrix_over_time(self, V, Q):
        """
        Given voltages and charges on electrodes, returns the mutual capacitance matrix for each timestep(symmetric about the diagonal).
        """

        def c(i, j):
            return self.calculate_true_capacitance(V, Q, i, j)

        num_e = V.shape[0]
        num_t = V.shape[1]
        capacitance = np.ones((num_e, num_e, num_t)) * np.nan
        for i in range(num_e):
            for j in range(num_e):
                capacitance[i, j] = c(i, j)
        return capacitance

    # def calculate_least_squares(
    #     self, t, V, num_transmitter, N_receiver, c_receive_multiplexer_off, r_pulldown_on_receive
    # ):
    #     """
    #     Capacitance estimation based on least squares approach (A'Ax=A'b formulation)
    #     """
    #     VT = V[num_transmitter - 1, :]
    #     VR = V[N_receiver - 1, :]
    #
    #     X1 = VT[1:] - VT[:-1]
    #     X2 = VR[1:] - VR[:-1]
    #
    #     Y = np.gradient(cumtrapz(VR, t)) / r_pulldown_on_receive[N_receiver - 1]
    #
    #     A = X1 - X2
    #     B = Y + c_receive_multiplexer_off[N_receiver - 1] * X2
    #
    #     AA = np.matmul(np.transpose(A), A)
    #     BB = np.matmul(np.transpose(A), B)
    #
    #     C_material = BB / AA
    #
    #     logger.info(
    #         f"Effective capacitance estimate between electrodes {num_transmitter} and {N_receiver}: {C_material:.3e}"
    #     )
    #     return C_material


close_logger(logger)
