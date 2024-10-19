import matplotlib.pyplot as plt
import numpy as np

from forwardSolver.scripts.params.forward_solver_params import (
    ForwardSolverParams,
)
from forwardSolver.scripts.solver_forward_P1000 import SolverForwardP1000
from forwardSolver.scripts.utils.utils_solver_forward_P1000 import (
    plot_capacitance,
)


def main():
    print("Running a simple simulation...")
    solver_forward, cap_matrix, params = test_simple_sim()
    print("Simulation succesful!")
    print("Capacitance matrix shape:", cap_matrix.shape)
    fig, axs = plt.subplots(1, 1, figsize=(10, 8))
    plot_capacitance(np.real(cap_matrix), ax=axs, plot_kwargs=dict(marker="s"))
    axs.set_title("Example Capacitance")
    axs.grid()
    plt.show()


def test_simple_sim():
    params = ForwardSolverParams.factory("P3000-005")
    params.signal.frequency = 20000
    params.pixels.num_pixel_rows = 5
    params.pixels.num_pixel_columns = 5

    # Permittivity data
    params.pixels.permittivity_matrix = 5 * np.ones(
        (params.pixels.num_pixel_rows, params.pixels.num_pixel_columns)
    )

    params.geometry.mesh_length_scale = 0.25
    params.geometry.domain_width = 220
    params.geometry.domain_height = 100
    params.geometry.material_width = 100
    params.geometry.material_height = 45
    params.geometry.material_gap = 0.5

    solver_forward = SolverForwardP1000(
        params,
        is_cap_calculated=True,
        is_full_cap_calculated=False,
        is_voltage_mat_calculated=False,
        physics_model=0,
    )
    return solver_forward, solver_forward.C_true, params


if __name__ == "__main__":
    main()
