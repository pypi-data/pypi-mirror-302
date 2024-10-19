import matplotlib.pyplot as plt
import numpy as np

from forwardSolver.scripts.params.forward_solver_params import ForwardSolverParams
from forwardSolver.scripts.utils.logging import close_logger, get_logger
from forwardSolver.scripts.utils.modules import SimulationModule

logger = get_logger(__name__)


def trapezoidal_wave(t, t_rise, t_dwell, t_fall, t_period, V_max):
    mod_t = t % t_period
    if mod_t <= t_rise:
        # Rising period
        return mod_t * V_max / t_rise
    elif mod_t <= t_rise + t_dwell:
        # Dwell period
        return V_max
    elif mod_t <= t_rise + t_dwell + t_fall:
        # Falling period
        return ((t_rise + t_dwell + t_fall) - mod_t) / t_fall * V_max
    else:
        # Zero period
        return 0.0


class InputGeneratorP1000Pulse(SimulationModule):
    """
    Signal generator for a time signal and a 1D trapezoidal voltage pulse signal for the P1000 board
    """

    def __init__(self, params: ForwardSolverParams):
        self.t_rise = params.signal.t_rise
        self.t_dwell = params.signal.t_dwell
        self.t_fall = params.signal.t_fall
        self.t_period = params.signal.t_period
        self.V_max = params.signal.v_max
        self.P_noise = params.signal.noise_power
        self.N_seed = params.signal.noise_random_seed

        self.t_step = params.simulation.t_step
        self.t_end = params.simulation.t_end

        self.t = None
        self.signal = None
        self.metrics = None
        self.check_inputs()

    def check_inputs(self):
        if self.t_end <= 0:
            raise ValueError(
                "Input parameter unphysical. t_end must be larger than zero."
            )
        if self.t_step <= 0:
            raise ValueError(
                "Input parameter unphysical. t_step must be larger than zero."
            )

    def check_simulation(self):
        # Check if time or signal contain any infinities or NaNs
        t_invalid = np.isnan(self.t) + np.isinf(self.t)
        signal_invalid = np.isnan(self.signal) + np.isinf(self.signal)

        if True in t_invalid:
            raise ValueError(
                f"Input generator time contains invalid values.\n {self.t}"
            )
        elif True in signal_invalid:
            raise ValueError(
                f"Input generator signal contains invalid values.\n {self.signal}"
            )

    def simulate(self):
        self.t = np.linspace(
            0, self.t_end, int(self.t_end / self.t_step), endpoint=False
        )
        self.signal = np.zeros(len(self.t))
        for i, t in enumerate(self.t):
            self.signal[i] = trapezoidal_wave(
                t,
                self.t_rise,
                self.t_dwell,
                self.t_fall,
                self.t_period,
                self.V_max,
            )

        np.random.seed(self.N_seed)
        self.signal += np.random.normal(0, np.sqrt(self.P_noise), len(self.signal))

        logger.info("P1000 trapezoidal pulse generated.")

        self.check_simulation()
        return self.t, self.signal

    def visualise(self, save_fig=None):

        fig = plt.figure()
        plt.plot(self.t, self.signal)
        plt.title("Generated Signal")
        plt.xlabel(r"Time ($\mu$s)")
        plt.ylabel("Signal (V)")
        plt.grid()
        if save_fig is not None:
            plt.savefig(save_fig)
            plt.close(fig)
            return None
        return fig


close_logger(logger)
