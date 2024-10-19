import os
import shutil
import subprocess
from dataclasses import asdict
from glob import glob
from typing import List, Tuple

import matplotlib.pyplot as plt
import meshio
import numpy as np
import scipy.sparse
import scipy.sparse.linalg
from matplotlib.colors import LogNorm

from forwardSolver.scripts.params.forward_solver_params import (
    ForwardSolverParams,
)
from forwardSolver.scripts.utils.constants import (
    CACHE_DIR,
    CREATE_PARALLEL_SUBDIR,
    DELETE_FREEFEM_FILES,
    EPSILON_0,
    ERROR_STRINGS,
)
from forwardSolver.scripts.utils.copy_files_to_subdir import (
    copy_files_to_subdir,
)
from forwardSolver.scripts.utils.create_pixelation import create_pixelation
from forwardSolver.scripts.utils.freefem import (
    params_to_freefem_command,
    read_freefem_array,
    read_freefem_sparsemat,
)
from forwardSolver.scripts.utils.hash import hash_dictionary
from forwardSolver.scripts.utils.logging import close_logger, get_logger

logger = get_logger(__name__)


def compute_electric_field_DtoS(V, sA, B, sL):
    """
    Solves the electrostatic problem given Dirichlet conditions.
    Computes and returns the average charge on the elec. surf.
    Arguments:
    V: N vector of voltages used as boundary conditions
    sA: sparse matrix (requires a isA.solve() operator)
    B: Matrix to apply boundary conditions
    sL: sparse Matrix to compute charges.
    Returns:
    Q: N vector of charges on elec. surface.
    Optional argument:
    RFlag: if True will return whole electric field in domain
    TW: 09/07/2021
    """
    isA = scipy.sparse.linalg.splu(sA)
    b = np.dot(B, V)  # Apply boundary condition
    V_field = isA.solve(b)  # Solve system
    Q = sL.T * V_field  # Compute charge on electrode surfaces
    return Q, V_field


def compute_electric_field_StoD(Q, sA, B, sL):
    """
    Solves the electrostatic problem given Shunt boundary conditions.
    Computes and returns the voltage on the electrodes
    Arguments:
    U: N vector of voltages used as boundary conditions
    sA: Sparse matrix
    B: Matrix to apply boundary conditions
    sL: sparse Matrix to compute charges.
    NE: Number of electrodes
    Returns:
    U: N vector of charges on elec. surface.
    Optional argument:
    RFlag: if True will return whole electric field in domain
    TW: 09/07/2021
    """
    # Build matrix system
    N = sL.T.shape[0]
    AAA = scipy.sparse.bmat([[sA, B], [sL.T, None]], format="csc")
    iAAA = scipy.sparse.linalg.splu(AAA)
    b = np.zeros(np.shape(sA)[0] + N)
    b[-N:] = Q  # Add in shunt conditions
    x = iAAA.solve(b)  # Solve system
    V_field = x[:N]
    V_electrode = x[-N:]
    return V_electrode, V_field


def plot_geometry(
    mesh,
    vals,
    val_string,
    save_fig=None,
    plot_mesh=True,
    cmap="jet",
    ax=None,
    plot_relative: bool = True,
):
    """
    Plots the permittivity over the mesh.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 5))
    else:
        fig = ax.get_figure()

    if plot_relative:
        epsilon_vals = np.array(vals) / EPSILON_0
    else:
        epsilon_vals = vals

    mesh_plot(
        mesh=mesh,
        vals=epsilon_vals,
        val_string=val_string,
        plot_mesh=plot_mesh,
        cmap=cmap,
        fig=fig,
        ax=ax,
    )
    ax.set_title(val_string)
    ax.set_xlabel("Horizontal Axis (mm)")
    ax.set_ylabel("Vertical Axis (mm)")
    if save_fig is not None:
        plt.savefig(save_fig)
        plt.close(fig)
        return None
    return fig


def mesh_plot(
    *,
    mesh,
    vals,
    fig,
    ax,
    plot_mesh,
    val_string="",
    cmap="jet",
    plot_log=False,
):
    if plot_mesh:
        ax.triplot(mesh.points[:, 0], mesh.points[:, 1], lw=0.1, color="grey")
    im = ax.tripcolor(
        mesh.points[:, 0],
        mesh.points[:, 1],
        vals,
        triangles=mesh.cells[0][1],
        cmap=cmap,
        norm=LogNorm() if plot_log else None,
    )
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label(val_string, rotation=90)


def plot_electric_field(mesh, u, save_fig=None):
    """
    Plots the function u over the mesh.
    Requires the mesh to be the same len as u.

    Overlays the structure of the geometry according to "geometry" cmd
    Electrodes have vertical caps at the moment in overlay.

    TW: 09/07/2021
    """

    fig, ax = plt.subplots(figsize=(10, 5))

    plt.triplot(mesh.points[:, 0], mesh.points[:, 1], lw=0.1, color="grey")
    im = plt.tricontourf(
        mesh.points[:, 0], mesh.points[:, 1], u, levels=100, cmap="jet"
    )
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("V", rotation=0)
    ax.axis("equal")
    plt.title("Static Electric field")
    plt.xlabel("Horizontal Axis (mm)")
    plt.ylabel("Vertical Axis (mm)")
    if save_fig is not None:
        plt.savefig(save_fig)
        plt.close(fig)
        return None
    return fig


def plot_boundary_values(t, V, Q, num_transmitter, save_fig=None):
    """
    Given a matrix V of voltages and Q a matrix of charges
    Plots the voltage and charge on each electrode.

    Arguments:
    t: time array
    V(i,j): matrix of voltages. i = elec. index, j = time index
    Q: matrix of charges. i = elec. index, j = time index
    num_transmitter: ID of the transmitter

    TW: 09/07/2021
    """

    N_electrodes = V.shape[0]
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))

    ax_0_twin = ax[0].twinx()
    for i in range(N_electrodes):
        if i == num_transmitter - 1:
            ax_0_twin.plot(t, V[i, :], "k--", label=f"E{i+1}")
            ax_0_twin.set_ylabel("Transmitter Voltage (V)")
        else:
            ax[0].plot(t, V[i, :], label=f"E{i+1}")
    ax[0].set_ylabel("Voltage (V)")
    ax[0].set_xlabel(r"Time ($\mu$s)")
    ax[0].grid()
    ax[0].legend()
    ax[0].set_title("Electrode Voltages")

    ax_1_twin = ax[1].twinx()
    for i in range(Q.shape[0]):
        if i == num_transmitter - 1:
            ax_1_twin.plot(t, Q[i, :], "k--", label=f"E{i + 1}")
            ax_1_twin.set_ylabel("Transmitter Charge (pC)")
        else:
            ax[1].plot(
                t,
                Q[i, :],
                label=(
                    f"W{i - N_electrodes + 1}"
                    if i >= N_electrodes
                    else f"E{i + 1}"
                ),
            )
    ax[1].set_ylabel("Charge (pC)")
    ax[1].set_xlabel(r"Time ($\mu$s)")
    ax[1].grid()
    ax[1].legend()
    ax[1].set_title("Electrode Charges")

    plt.tight_layout()
    if save_fig is not None:
        plt.savefig(save_fig)
        plt.close(fig)
        return None
    return fig


def setup_solver_environment(
    params: ForwardSolverParams,
    solver_dir,
    solver_file,
    create_parallel_subdir=CREATE_PARALLEL_SUBDIR,
    is_voltage_mat_calculated=True,
    is_capacitance_calculated=False,
    is_full_capacitance_calculated=False,
    is_python_used_as_solver=False,
    physics_model=0,
    export_mesh=True,
):
    """
    Set up the matrices for a solution.
    Only needs to be run once per live instance.

    Arguments:
    permittivity_pcb_substrate: Rel. perm. of the pcb_substrate

    Returns:
    sA: Sparse A matrix
    B: matrix B used to apply boundary conditions
    isL: Sparse matrix to compute average charge on elec. surf.
    mesh: (x,y) coords of nodes in mesh.

    TW: 09/07/2021
    """
    dup_count = 0  # duplicate counter for parallel subdirectories
    solver_subdir = (
        "run_"
        + hash_dictionary(asdict(params))
        + "_count_"
        + str(dup_count)
        + "/"
        if create_parallel_subdir
        else "run_0/"
    )

    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    artefacts_dir = os.path.abspath(
        solver_dir + solver_subdir + "solver_artefacts"
    )
    # Don't use old artifacts
    while os.path.exists(artefacts_dir):
        if create_parallel_subdir:
            dup_count += 1
            solver_subdir = (
                solver_subdir.rsplit("_", 1)[0] + "_" + str(dup_count) + "/"
            )
            artefacts_dir = os.path.abspath(
                solver_dir + solver_subdir + "solver_artefacts"
            )
        else:
            shutil.rmtree(artefacts_dir)

    # Create empty directory to store new artefacts
    os.makedirs(artefacts_dir + "/pixels", exist_ok=True)

    log_path = os.path.abspath(solver_dir + solver_subdir + "freefem.log")

    copy_files_to_subdir(solver_dir, solver_dir + solver_subdir, "edp")

    if params.board.lower() in [
        "imported",
        "p1000_001",
        "p1000_004",
        "p1000_006",
        "p1000_009",
        "p3000_005",
        "p1000_014",
    ]:
        os_command = params_to_freefem_command(
            params,
            os.path.abspath(solver_dir + solver_subdir),
            log_path,
            is_capacitance_calculated=is_capacitance_calculated,
            is_full_capacitance_calculated=is_full_capacitance_calculated,
            is_voltage_mat_calculated=is_voltage_mat_calculated,
            is_python_used_as_solver=is_python_used_as_solver,
            physics_model=physics_model,
            export_mesh=export_mesh,
        )

        if params.board.startswith("P"):
            extra_layers_components = (
                params.geometry.oil_thickness,
                params.geometry.mylar_thickness,
                params.geometry.mylar_gap,
                params.geometry.plastic_thickness,
                params.geometry.gel_thickness,
            )

            # extra_layers = all(x is not None for x in extra_layers_components)
            extra_layers = [
                x for x in extra_layers_components if x is not None
            ]

            # Check the pixels params consistency
            validate_pixels(params)

            # Call the function to create pixelation
            create_pixelation(
                params_pixels=params.pixels,
                subdir=solver_dir + solver_subdir,
                extra_layers=extra_layers,
            )

    elif params.board.lower() == "p1000_00x":
        os_command = (
            f"FreeFem++ -nw -ne {os.path.abspath(solver_dir + solver_file)} "
            f"boardGeometry P1000-00X "
            f"freefemDir {solver_dir+solver_subdir} "
            f"BPlot 0 "
            f"BComputeVolt {int(is_voltage_mat_calculated)} "
            f"BExportMesh {int(export_mesh)} "
            f"MM {params.geometry.mesh_elements_on_border} "
            f"xElecW {params.geometry.electrode_width} "
            f"xElecSep {params.geometry.electrode_separation} "
            f"eBackground {params.geometry.permittivity_background} "
            f"> {log_path}"
        )

    else:
        raise ValueError(f"Unrecognised board type: {params.board}!")

    logger.info(f"FreeFem++ Command: {os_command}")
    print(f"FreeFem++ Command: {os_command}")

    cwd = os.getcwd()  # current working directory
    try:
        os.chdir(
            solver_dir + solver_subdir
        )  # enter subdir to use relevant files
        logger.debug(f'Changed directory to "{solver_dir + solver_subdir}"')
        sp_result = subprocess.run(
            os_command, shell=True, check=True, capture_output=True
        )
        logger.debug(f"FreeFem++ Output: {sp_result.stdout.decode('utf-8')}")
        logger.debug(f"FreeFem++ Error: {sp_result.stderr.decode('utf-8')}")
        logger.debug(f"FreeFem++ Return Code: {sp_result.returncode}")
    except OSError as err:
        logger.error(
            f'Error changing directory to "{solver_dir + solver_subdir}". {err}'
        )
        raise err
    except subprocess.CalledProcessError as err:
        logger.error(f"Error running FreeFem++ command! {err}")
        logger.error(f"FreeFem++ Output: {err.stdout.decode('utf-8')}")
        logger.error(f"FreeFem++ Error: {err.stderr.decode('utf-8')}")
        logger.error(f"FreeFem++ Return Code: {err.returncode}")
        raise err
    finally:
        os.chdir(cwd)  # exit subdir to allow deletion of subdir

    with open(log_path, "r") as f:
        contents = f.read()
    if any(error_string in contents.lower() for error_string in ERROR_STRINGS):
        raise ArithmeticError(
            "Error found in FreeFem log file when attempting to"
            f" generate meshes and matrices: \n{contents})"
        )

    sA, B, sL, pixels, A_tensor, K_tensor, LHSBC, Aback, Kback = (
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    )

    artefacts_dir = solver_dir + solver_subdir + "solver_artefacts/"

    if os.path.isfile(artefacts_dir + "Amatrix.txt"):
        sA = read_freefem_sparsemat(
            artefacts_dir + "Amatrix.txt",
            sparse=True,
        )  # stiffness matrix of the background reference

    if os.path.isfile(artefacts_dir + "Bmatrix.txt"):
        B = read_freefem_sparsemat(
            artefacts_dir + "Bmatrix.txt"
        )  # matrix that imposes the boundary conditions

    if os.path.isfile(artefacts_dir + "Lmatrix.txt"):
        sL = read_freefem_sparsemat(
            artefacts_dir + "Lmatrix.txt",
            sparse=True,
        )  # charge flux in/out of all pcb_substrate mesh elements
        if params.dimension == 2:
            sL *= params.geometry.electrode_length

    if os.path.isfile(artefacts_dir + "pixels/pixel_0.txt"):
        pixels = build_indicators_pixels(
            artefacts_dir + "pixels",
            params.pixels.num_total_pixels,
        )

    if os.path.isfile(artefacts_dir + "pixels/A_0.txt"):
        A_tensor = build_list_of_matrices(
            artefacts_dir + "pixels",
            "A",
            params.pixels.num_total_pixels,
        )

    if os.path.isfile(artefacts_dir + "pixels/K_0.txt"):
        K_tensor = build_list_of_matrices(
            artefacts_dir + "pixels",
            "K",
            params.pixels.num_total_pixels,
        )
        if params.dimension == 2:
            for mat in K_tensor:
                mat *= params.geometry.electrode_length

    if os.path.isfile(artefacts_dir + "BCLHS.txt"):
        LHSBC = read_freefem_sparsemat(
            artefacts_dir + "BCLHS.txt",
            sparse=True,
        )

    if os.path.isfile(artefacts_dir + "K_back.txt"):
        Kback = read_freefem_sparsemat(
            artefacts_dir + "K_back.txt",
            sparse=True,
        )
        if params.dimension == 2:
            Kback *= params.geometry.electrode_length

    if os.path.isfile(artefacts_dir + "A_back.txt"):
        Aback = read_freefem_sparsemat(
            artefacts_dir + "A_back.txt",
            sparse=True,
        )

    mesh = None
    if os.path.isfile(artefacts_dir + "Th.vtk"):
        mesh = meshio.read(
            artefacts_dir + "Th.vtk"
        )  # spatial information about mesh elements (node information)

    eps = None
    if os.path.isfile(artefacts_dir + "eps.txt"):
        eps = read_freefem_array(artefacts_dir + "eps.txt")
    else:
        logger.warning("Epsilon file not found!")

    sig = None
    if os.path.isfile(artefacts_dir + "sig.txt"):
        with open(artefacts_dir + "sig.txt") as f:
            contents = f.read()
        sig = [
            float(val)
            for val in contents.replace("\n", "").replace(" ", "").split("\t")
            if val != ""
        ][1:]
    else:
        logger.warning("Sigma file not found!")

    sensitivities = {}
    sensitivity_map_paths = glob(os.path.join(artefacts_dir, "sens_*.txt"))
    if sensitivity_map_paths is not None:
        for sensitivity_map_path in sensitivity_map_paths:
            electrode_pair = os.path.basename(sensitivity_map_path)[4:-4]
            with open(sensitivity_map_path) as f:
                contents = f.read()
            sensitivity = [
                float(val)
                for val in contents.replace("\n", "")
                .replace(" ", "")
                .split("\t")
                if val != ""
            ][1:]
            sensitivities[electrode_pair] = sensitivity
    else:
        logger.warning("Sensitivity maps not found!")

    C_true = None
    if os.path.isfile(artefacts_dir + "C.txt"):
        C_true = read_freefem_array(artefacts_dir + "C.txt")
        if params.dimension == 2:
            C_true *= params.geometry.electrode_length
    else:
        logger.warning("True capacitance file not found!")

    C_full = None
    if os.path.isfile(artefacts_dir + "C_full.txt"):
        C_full = read_freefem_array(artefacts_dir + "C_full.txt")
        if params.dimension == 2:
            C_full *= params.geometry.electrode_length
    else:
        logger.warning("Full capacitance file not found!")

    sensitivity_mesh = None
    if os.path.isfile(artefacts_dir + "sensitivity_mesh.vtk"):
        sensitivity_mesh = meshio.read(
            artefacts_dir + "sensitivity_mesh.vtk"
        )  # spatial information about sensitivity mesh elements (node information)
    else:
        logger.warning("Sensitivity mesh not found")

    v_slice_sens = None
    if os.path.isfile(artefacts_dir + "vslice_sensitivity.txt"):
        v_slice_sens = np.loadtxt(
            artefacts_dir + "vslice_sensitivity.txt",
            skiprows=1,
        )
    else:
        logger.warning("Vertical sensitivity slice not found")

    h_slice_sens1 = None
    if os.path.isfile(artefacts_dir + "hslice1_sensitivity.txt"):
        h_slice_sens1 = np.loadtxt(
            artefacts_dir + "hslice1_sensitivity.txt",
            skiprows=1,
        )
    else:
        logger.warning("Horizontal sensitivity slice (1) not found")

    h_slice_sens2 = None
    if os.path.isfile(artefacts_dir + "hslice2_sensitivity.txt"):
        h_slice_sens2 = np.loadtxt(
            artefacts_dir + "hslice2_sensitivity.txt",
            skiprows=1,
        )
    else:
        logger.warning("Horizontal sensitivity slice (2) not found")

    h_slice_sens3 = None
    if os.path.isfile(artefacts_dir + "hslice3_sensitivity.txt"):
        h_slice_sens3 = np.loadtxt(
            artefacts_dir + "hslice3_sensitivity.txt",
            skiprows=1,
        )
    else:
        logger.warning("Horizontal sensitivity slice (3) not found")

    sensitivity_electrode_pair = None
    if os.path.isfile(artefacts_dir + "sensitivity_electrode_pair.txt"):
        sensitivity_electrode_pair = read_freefem_array(
            artefacts_dir + "sensitivity_electrode_pair.txt"
        )
    else:
        logger.warning("Electrode pair sensitivity not found")

    sensitivity_single_electrode_sum = None
    if os.path.isfile(artefacts_dir + "sensitivity_single_electrode_sum.txt"):
        sensitivity_single_electrode_sum = read_freefem_array(
            artefacts_dir + "sensitivity_single_electrode_sum.txt"
        )
    else:
        logger.warning("Single electrode sensitivity sum not found")

    sensitivity_total_sum = None
    if os.path.isfile(artefacts_dir + "sensitivity_totalSum.txt"):
        sensitivity_total_sum = read_freefem_array(
            artefacts_dir + "sensitivity_totalSum.txt"
        )
    else:
        logger.warning("Total sum sensitivity not found")

    if DELETE_FREEFEM_FILES and os.path.exists(solver_dir + solver_subdir):
        shutil.rmtree(solver_dir + solver_subdir)

    return (
        solver_subdir,
        sA,
        B,
        sL,
        mesh,
        eps,
        sig,
        C_true,
        C_full,
        sensitivities,
        pixels,
        A_tensor,
        K_tensor,
        LHSBC,
        Aback,
        Kback,
        sensitivity_mesh,
        v_slice_sens,
        h_slice_sens1,
        h_slice_sens2,
        h_slice_sens3,
        sensitivity_electrode_pair,
        sensitivity_single_electrode_sum,
        sensitivity_total_sum,
    )


def validate_pixels(params: ForwardSolverParams):
    """
    Check that the pixelation in given parameters is valid for simulation
    """
    valid_pixels = [
        "curved_rectangle",
        "curved_rectangle_nonuniform",
        "circular_phantom",
    ]

    if params.pixels.pixel_type not in valid_pixels:
        raise ValueError(
            f"The pixel type {params.pixels.pixel_type} does not fall in the list "
            + f"of valid choices:{valid_pixels}"
        )

    if params.pixels.pixel_type == "circular_phantom":
        num_background_pixels = (
            2 if params.pixels.circular_phantom_thickness is not None else 1
        )
        num_bores = (
            len(params.pixels.circular_phantom_bore_radii)
            if params.pixels.circular_phantom_bore_radii is not None
            else 0
        )
        if (
            params.pixels.num_pixel_rows != 1
            or params.pixels.num_pixel_columns
            != num_bores + num_background_pixels
        ):
            raise ValueError(
                f"The num_pixel_rows {params.pixels.num_pixel_rows} "
                + f"and pixel columns {params.pixels.num_pixel_columns} "
                + "are inconsistent with the phantom parameters."
                + f"Should be 1x{num_bores + num_background_pixels}."
            )

        if (
            params.pixels.permittivity_matrix is not None
            and len(params.pixels.permittivity_matrix)
            != params.pixels.num_pixel_columns
        ):
            raise ValueError(
                "The permittivity matrix should have a length equal to"
                "number of pixel columns."
                "The order of the entries are "
                "filling, border, bore1, bore 2, ..., bore N."
            )

        if (
            params.pixels.conductivity_matrix is not None
            and len(params.pixels.conductivity_matrix)
            != params.pixels.num_pixel_columns
        ):
            raise ValueError(
                "The conductivity matrix should have a length equal to"
                "number of pixel columns."
                "The order of the entries are "
                "filling, border, bore1, bore 2, ..., bore N."
            )
        if params.pixels.circular_phantom_bore_radii is not None:
            for iloop_bore_radius in params.pixels.circular_phantom_bore_radii:
                if iloop_bore_radius > (
                    params.pixels.circular_phantom_radius
                    - params.pixels.circular_phantom_bore_centre_distance
                ):
                    raise ValueError(
                        f"The value {params.pixels.circular_phantom_bore_radii} is inconsistent"
                    )

            # This condition on radius of the phantom is slightly stricter than
            # necessary in some cases and is kept as such for now for
            # simplicity
        if params.pixels.circular_phantom_radius is not None:
            if (
                params.geometry.curvature_radius
                < params.pixels.circular_phantom_radius
            ):
                logger.warning(
                    f"The phantom radius {params.pixels.circular_phantom_radius}"
                    + "is greater than the board curvature "
                    + f"{params.geometry.curvature_radius}"
                )


def build_indicators_pixels(dir: os.PathLike, num_pixels: int):
    """
    Loads all pixel indicators from dir
    Returns a list of arrays.
    """
    pixel_files = [
        os.path.join(dir, f"pixel_{i}.txt") for i in range(num_pixels)
    ]
    return list(map(read_freefem_array, pixel_files))


def build_list_of_matrices(dir: os.PathLike, matrix: str, num_pixels: int):
    """
    Returns a list of arrays
    """
    matrix_files = [
        os.path.join(dir, f"{matrix}_{i}.txt") for i in range(num_pixels)
    ]
    return list(map(read_freefem_sparsemat, matrix_files))


def dot_product_lists(L, K):
    # Efficiently computes the dot product of two lists
    assert len(K) == len(L)
    return sum(i[0] * i[1] for i in zip(K, L))


# TODO: [TES-434] Remove this calculation and replace with the more accurate voltage calculation
def timestep_electric_field_DtoS(
    sA,
    B,
    sL,
    t,
    t_step,
    V_transmit,
    num_transmitter,
    C,
    R,
    board_ID,
    C2,
    R2,
    CparF1,
    CparB1,
):
    """
    Computes the time-dependent E field given transmit pulse
    the capacitance/receiver load on electrodes.

    Arguments:
    sA: is sparse matrix
    B: Matrix to apply BCs
    sL: Matrix to compute boundary charges
    t: time
    t_step: time step
    V_transmit: input transmit signal
    num_transmitter: transmitter ID (1...)
    C: capacitance for each electrode
    R: resistance for each electrode

    Returns:
    V: matrix of voltages
    Q: matrix of voltages

    TW: 09/07/2021
    """
    N_electrodes = len(C)
    N_steps = len(t)

    # Initialise outputs
    V = np.zeros([N_electrodes, N_steps])
    Q = np.zeros([sL.shape[1], N_steps])

    # Initial condition (Q = 0 implicit as no voltage difference assumed initially)
    V[num_transmitter - 1, :] = V_transmit

    diagvec = np.zeros(N_electrodes)
    diagvec[1:] += CparF1
    diagvec[:-1] += CparB1

    AA = (
        np.diag(C)
        + np.diag(diagvec)
        - np.diag(CparB1, 1)
        - np.diag(CparF1, -1)
        + t_step * np.diag(1.0 / R)
    )
    AA[num_transmitter - 1, :] = 0.0
    AA[num_transmitter - 1, num_transmitter - 1] = (
        1.0  # Identity on transmitter (fixed, but retained to maintain indices)
    )

    # Build RHS matrix
    RHS_matrix = (
        np.diag(C)
        + np.diag(diagvec)
        - np.diag(CparB1, 1)
        - np.diag(CparF1, -1)
    )
    RHS_matrix[num_transmitter - 1, :] = 0.0
    RHS_matrix[num_transmitter - 1, num_transmitter - 1] = (
        1.0  # Identity on transmitter (fixed, but retained to maintain indices)
    )

    diags = np.ones(N_electrodes)
    diags[num_transmitter - 1] = 0.0
    I1 = scipy.sparse.diags(diags)

    # Drop charge compute on the transmitter in the system
    sL2 = I1 * sL[:, :N_electrodes].T
    # Setting up as coupled PDE solver_artefacts (solving the PDE and ODE at once)
    AAA = scipy.sparse.bmat(
        [[sA, -B], [sL2, AA]], format="csc"
    )  # 4x4 block matrix (non-diagonal so PDEs & ODEs interact)
    iAAA = scipy.sparse.linalg.splu(AAA)

    x = np.zeros(AAA.shape[0])
    b = np.zeros(np.shape(sA)[0] + N_electrodes)
    if board_ID in ["P1000_00X", "P1000_001", "P1000_004"]:
        for i in range(N_steps - 1):
            V[num_transmitter - 1, i] = V_transmit[i]
            b[-N_electrodes:] = sL2 * x[:-N_electrodes] + np.matmul(
                RHS_matrix, V[:, i]
            )

            x = iAAA.solve(b)  # Voltages at every mesh node and the electrodes
            V[:, i + 1] = x[-N_electrodes:]
            Q[:, i + 1] = sL.T * x[:-N_electrodes]

    elif board_ID in [
        "P1000_006",
        "P1000_009",
        "P3000_005",
        "P1000_014",
        "Imported",
    ]:  # Boards with RC series on receiver
        V_cap_series = np.zeros(
            N_electrodes
        )  # Initialise charge on capacitor in series

        AA_series_RC = np.diag(C2) + t_step * np.diag(1 / R2)
        iAA_series_RC = np.linalg.inv(AA_series_RC)

        for i in range(1, N_steps - 1):
            V[num_transmitter - 1, i] = V_transmit[i]

            bvec = np.diag(C2) @ (V_cap_series + V[:, i] - V[:, i - 1])
            V_cap_series = iAA_series_RC @ bvec

            b[-N_electrodes:] = (
                sL2 * x[:-N_electrodes]
                + np.matmul(RHS_matrix, V[:, i])
                - t_step * np.diag(1.0 / R2) @ V_cap_series
            )

            x = iAAA.solve(b)  # Voltages at every mesh node and the electrodes
            V[:, i + 1] = x[-N_electrodes:]
            Q[:, i + 1] = sL.T * x[:-N_electrodes]
    else:
        raise NotImplementedError(f"Board type: {board_ID} not recognised!")
    return V, Q


def timestep_potentials_at_all_nodes(
    *,
    A_sparse_fem_stiffness_matrix: scipy.sparse.csc_matrix,
    B_sparse_fem_rhs_matrix: scipy.sparse.csc_matrix,
    L_sparse_fem_charge_matrix: scipy.sparse.csc_matrix,
    time_vector: np.ndarray,
    time_step: float,
    voltage_transmit: np.ndarray,
    num_transmitter: int,
    capacitance_knode_to_ground: np.ndarray,
    resistance_knode_to_ground: np.ndarray,
    board_ID: str,
    capacitance_tnode_to_ground: np.ndarray,
    resistance_tnode_to_knode: np.ndarray,
    capacitance_parasitic_forward: np.ndarray,
    capacitance_parasitic_backward: np.ndarray,
    resistance_tnode_to_ground=1e30,  # Currently this resistance is not present and hence set to a high value
) -> tuple[np.ndarray, np.ndarray]:
    """
    Computes the time-dependent electric potential given transmit pulse.
    Please check the following link for the details on the implemented equation:
    https://zedsen.atlassian.net/wiki/spaces/ZED/pages/617119755/
    Returns:
    voltage_knode: matrix of K node voltages
    voltage_tnode: matrix of T node voltages
    """
    if board_ID in [
        "P1000_006",
        "P1000_009",
        "P3000_005",
        "P1000_014",
    ]:  # Boards with RC series on receiver
        # Size of parameters
        num_electrodes = len(capacitance_knode_to_ground)
        num_time_steps = len(time_vector)

        # Initialise voltage vectors
        voltage_knode = np.zeros([num_electrodes, num_time_steps])
        voltage_tnode = np.zeros([num_electrodes, num_time_steps])

        # Rescale the matrix with the length and permittivity constant
        L_sparse_fem_charge_matrix = L_sparse_fem_charge_matrix[
            :, :num_electrodes
        ].T

        # Form the matrix M_capacitance_matrix_knode_to_ground_with_parasitics
        diagonal_vector_parasitic = capacitance_knode_to_ground
        diagonal_vector_parasitic[:-1] += capacitance_parasitic_forward
        diagonal_vector_parasitic[1:] += capacitance_parasitic_backward
        M_capacitance_matrix_knode_to_ground_with_parasitics = (
            np.diag(diagonal_vector_parasitic)
            - np.diag(capacitance_parasitic_backward, -1)
            - np.diag(capacitance_parasitic_forward, 1)
        )

        # Form the system matrix with coupled PDE-ODE
        A_sparse_ode_knode_knode = scipy.sparse.csc_matrix(
            M_capacitance_matrix_knode_to_ground_with_parasitics
            + np.diag(
                time_step
                * (
                    1 / resistance_tnode_to_knode
                    + 1 / resistance_knode_to_ground
                )
            )
        )
        A_sparse_ode_knode_tnode = scipy.sparse.diags(
            -time_step / resistance_tnode_to_knode
        )
        diagonal_vector_ode_tnode_knode = (
            -time_step / resistance_tnode_to_knode
        )
        # Adjustment for the electrode index with the source connected
        diagonal_vector_ode_tnode_knode[num_transmitter - 1] = 0.0

        A_sparse_ode_tnode_knode = scipy.sparse.diags(
            diagonal_vector_ode_tnode_knode
        )
        diagonal_vector_ode_tnode_tnode = (
            capacitance_tnode_to_ground
            + time_step
            * (1 / resistance_tnode_to_knode + 1 / resistance_tnode_to_ground)
        )
        # Adjustment for the electrode index with the source connected
        diagonal_vector_ode_tnode_tnode[num_transmitter - 1] = 1.0

        A_sparse_ode_tnode_tnode = scipy.sparse.diags(
            diagonal_vector_ode_tnode_tnode
        )
        A_matrix_system = scipy.sparse.bmat(
            [
                [
                    A_sparse_fem_stiffness_matrix,
                    -B_sparse_fem_rhs_matrix,
                    None,  # Entry of None specifies an all zero block matrix of compatible size
                ],
                [
                    L_sparse_fem_charge_matrix,
                    A_sparse_ode_knode_knode,
                    A_sparse_ode_knode_tnode,
                ],
                [
                    None,  # Entry of None specifies an all zero block matrix of compatible size
                    A_sparse_ode_tnode_knode,
                    A_sparse_ode_tnode_tnode,
                ],
            ],
            format="csc",
        )
        # Factorize the system matrix
        inverse_A_matrix_system = scipy.sparse.linalg.splu(
            A_matrix_system
        )  # The LU factorization of the sparse system matrix
        # Initialize the RHS matrix for the system
        b_vector_system = np.zeros(A_matrix_system.shape[0])
        u_system_solution = np.zeros(
            A_matrix_system.shape[0]
        )  # Vector of the solution of the linear system
        for time_index in range(1, num_time_steps):
            # Form the RHS ,matrix for the system
            electrode_slice = slice(-2 * num_electrodes, -num_electrodes)
            b_vector_system[electrode_slice] = (
                (
                    L_sparse_fem_charge_matrix
                    @ u_system_solution[: -2 * num_electrodes]
                )
                + M_capacitance_matrix_knode_to_ground_with_parasitics
                @ voltage_knode[:, time_index - 1]
            )
            b_vector_system[-num_electrodes:] = (
                capacitance_tnode_to_ground * voltage_tnode[:, time_index - 1]
            )
            b_vector_system[-num_electrodes + num_transmitter - 1] = (
                voltage_transmit[time_index - 1]
            )
            u_system_solution = inverse_A_matrix_system.solve(b_vector_system)
            voltage_knode[:, time_index] = u_system_solution[
                -2 * num_electrodes : -num_electrodes  # noqa E203
            ]
            voltage_tnode[:, time_index] = u_system_solution[-num_electrodes:]
    else:
        raise NotImplementedError(f"Board type: {board_ID} not recognised!")
    return voltage_knode, voltage_tnode


def make_xlabels(num_electrodes: int) -> Tuple[List[str], List[str]]:
    """
    Create the lists of labels which will be used in the capacitances plot

    First output is a full list of labels
    Second output is a reduced list of labels
    """
    # Make the xlabel name of the capacitances
    num_upper_tri = int(num_electrodes * (num_electrodes - 1) / 2)
    x_labels = [" "] * num_upper_tri
    x_labels_reduced = [" "] * (num_electrodes - 1)
    num_loop = 0
    for iloop in range(num_electrodes - 1):
        x_labels_reduced[iloop] = f"{iloop+1}" + "-" + f"{iloop+2}"
        for jloop in range(iloop + 1, num_electrodes):
            x_labels[num_loop] = f"{iloop+1}" + "-" + f"{jloop+1}"
            num_loop += 1
    return x_labels, x_labels_reduced


def plot_capacitance(
    capacitance_matrix: np.ndarray,
    is_upper_triangular: bool = False,
    ax: plt.Axes = None,
    plot_kwargs: dict = dict(marker="s", label="Estimated Capacitances"),
    ax_kwargs: dict = dict(
        yscale="log", ylabel="Capacitance (F)", xlabel="Electrode pairs"
    ),
    add_legend: bool = True,
    use_xlabels_reduced: bool = True,
    output_filename: str = None,
    **kwargs,
) -> plt.Figure:
    """Create a capacitance plot to given axis.
    If no axis is given it will generate a figure.

    Args:
        capacitance_matrix (np.ndarray): capacitance to plot
        is_upper_triangular (bool): whether the input capacitance matrix is already
                                flattened upper triangular form
        ax (plt.Axes, optional): axis to plot to. Defaults to None.
        plot_kwargs (dict): plot key word arguments with default marker and plot label
        ax_kwargs (dict): ax key word arguments with default yscale and ylabel

    Returns:
        plt.Figure
    """

    # Calculate the error in the upper triangular part of capacitance matrix
    if is_upper_triangular:
        capacitance_upper_triangular = capacitance_matrix
        # Recover num_electrodes using n*(n-1)/2 = len(capacitance_upper_triangular)
        num_electrodes = int(
            (1 + np.sqrt(1 + 8 * len(capacitance_upper_triangular))) / 2
        )
    else:
        num_electrodes = capacitance_matrix.shape[0]
        capacitance_upper_triangular = capacitance_matrix[
            np.triu_indices(num_electrodes, k=1)
        ]

    # Make the xlabel name of the capacitances
    x_labels, x_labels_reduced = make_xlabels(num_electrodes)
    if not use_xlabels_reduced:
        x_labels_reduced = x_labels

    if ax is None:
        _, ax = plt.subplots()

    plot_kwargs["marker"] = (
        plot_kwargs.get("marker") if plot_kwargs.get("marker") else "s"
    )
    plot_kwargs["label"] = (
        plot_kwargs.get("label")
        if plot_kwargs.get("label")
        else "Estimated Capacitance"
    )

    ax.plot(x_labels, capacitance_upper_triangular, **plot_kwargs)

    ax.set_xticks(x_labels_reduced)
    ax.set_xticklabels(x_labels_reduced, rotation=90)
    ax.set(**ax_kwargs)
    if add_legend:
        ax.legend()

    if output_filename is not None:
        ax.get_figure().savefig(output_filename, dpi=1000)

    return ax.get_figure()


def timestep_potentials_for_all_transmitters(
    *,
    A_sparse_fem_stiffness_matrix: scipy.sparse.csc_matrix,
    B_sparse_fem_rhs_matrix: scipy.sparse.csc_matrix,
    L_sparse_fem_charge_matrix: scipy.sparse.csc_matrix,
    time_vector: np.ndarray,
    time_step: float,
    voltage_transmit: np.ndarray,
    capacitance_knode_to_ground: np.ndarray,
    resistance_knode_to_ground: np.ndarray,
    board_ID: str,
    capacitance_tnode_to_ground: np.ndarray,
    resistance_tnode_to_knode: np.ndarray,
    capacitance_parasitic_forward: np.ndarray,
    capacitance_parasitic_backward: np.ndarray,
    resistance_tnode_to_ground=1e30,  # Currently this resistance is not present and hence set to a high value
    array_of_transmitters=None,
) -> tuple[np.ndarray, np.ndarray]:
    """This function returns 3D arrays with K node and T node voltages
    for each transmit electrode specified in array_of_transmitters"""
    if board_ID in [
        "P1000_006",
        "P1000_009",
        "P3000-005",
        "P1000_014",
    ]:  # Boards with RC series on receiver
        # Size of parameters
        num_electrodes = len(capacitance_knode_to_ground)
        num_time_steps = len(time_vector)
        num_transmitters = num_electrodes
        # If an array of transmitters in not passed produce the output for
        # all possible cases
        if array_of_transmitters is None:
            array_of_transmitters = np.arange(1, num_electrodes + 1)
        voltages_tnode_for_all_transmitters = np.zeros(
            (num_transmitters, num_electrodes, num_time_steps)
        )
        voltages_knode_for_all_transmitters = np.zeros(
            (num_transmitters, num_electrodes, num_time_steps)
        )

        for iloop_transmit_electrode in array_of_transmitters:
            print(
                f"Currently calculating the voltages with the transmit electrode number: {iloop_transmit_electrode}"
            )
            (
                voltages_knode_for_all_transmitters[
                    iloop_transmit_electrode - 1
                ],
                voltages_tnode_for_all_transmitters[
                    iloop_transmit_electrode - 1
                ],
            ) = timestep_potentials_at_all_nodes(
                A_sparse_fem_stiffness_matrix=A_sparse_fem_stiffness_matrix,
                B_sparse_fem_rhs_matrix=B_sparse_fem_rhs_matrix,
                L_sparse_fem_charge_matrix=L_sparse_fem_charge_matrix,
                time_vector=time_vector,
                time_step=time_step,
                voltage_transmit=voltage_transmit,
                num_transmitter=iloop_transmit_electrode,
                capacitance_knode_to_ground=capacitance_knode_to_ground,
                resistance_knode_to_ground=resistance_knode_to_ground,
                board_ID=board_ID,
                capacitance_tnode_to_ground=capacitance_tnode_to_ground,
                resistance_tnode_to_knode=resistance_tnode_to_knode,
                capacitance_parasitic_forward=capacitance_parasitic_forward,
                capacitance_parasitic_backward=capacitance_parasitic_backward,
                resistance_tnode_to_ground=resistance_tnode_to_ground,
            )

    else:
        raise NotImplementedError(f"Board type: {board_ID} not recognised!")

    return (
        voltages_knode_for_all_transmitters,
        voltages_tnode_for_all_transmitters,
    )


close_logger(logger)
