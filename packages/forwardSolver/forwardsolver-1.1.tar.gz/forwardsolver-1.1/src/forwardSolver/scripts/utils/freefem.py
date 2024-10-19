import ast
import os

import numpy as np
import scipy

from forwardSolver.scripts.params.forward_solver_params import ForwardSolverParams
from forwardSolver.scripts.utils.logging import close_logger, get_logger

logger = get_logger(__name__)


def write_array_to_freefem_file(arr, filename):
    """
    Writes numpy array to `filename` so that FreeFem++ can import as a vector.
    The first line in the output file will show the size of the array.

    Parameters:
    arr (numpy.ndarray): The array to be written to the file.
    filename (str): The name of the file where the array will be saved.
    The array is saved with 15 decimal precision, tab-separated values, and a newline character at the end of each line.
    The file starts with a header containing the size of the array.
    """

    np.savetxt(
        filename,
        arr,
        fmt="%.15f",
        delimiter="\t ",
        newline="\n",
        header=f"{np.size(arr)}\n",
        comments="",
    )


def read_freefem_metrics_to_dict(filename):
    """
    Reads FreeFem++ output and populates a dictionary with the error metrics
    and the calculated values. Checks for any status msgs from FreeFem++
    Args:
        filename (str): The path to the file containing the FreeFEM metrics.
    Returns:
        dict: A dictionary containing the extracted metrics and a status message.
              The keys are the metric names (without the "metric_" prefix) and the values are the corresponding metric values.
              The dictionary also contains a "status_msg" key with a value of 1 if any "status_msg:" lines are found, otherwise 0.
    """
    error_dict = dict()
    with open(filename, "r") as f:
        lst = [p for p in f.readlines() if "metric_" in p]  # Find all error metrics
        for e in lst:  # Populate dictionary
            _key = e.split(":")[0].lower().replace("metric_", "")
            _value = float(e.split(":")[1].split("\n")[0])
            error_dict[_key] = _value
        lst = [p for p in f.readlines() if "status_msg:" in p]  # Find all error metrics
        if len(lst) > 0:
            error_dict["status_msg"] = 1
            for _msg in lst:
                logger.error(_msg)
        else:
            error_dict["status_msg"] = 0
            logger.info("Metrics calculated successfully.")

    return error_dict


def complexifyall(arr: np.ndarray) -> np.ndarray:
    """
    Applies _complexify_string to every element of an array. Does not need the size of the arr to be specified
    Args:
        arr (np.ndarray): A numpy array containing string representations of complex numbers.
    Returns:
        np.ndarray: A numpy array containing complex numbers.
    """

    return np.vectorize(lambda x: complex(*ast.literal_eval(x)))(arr)


def _read_1D_freefem_array(filename: str, dtype=float) -> np.ndarray:
    """
    Read in 1D array from file saved in FreeFem format
    Each row will have at most five elements,
    which means the last row may have a different number of elements than the rest of
    the lines. This is not liked by np.genfromtxt or np.loadtxt.
    Parameters:
    filename (str): The path to the FreeFem output file.
    dtype (type, optional): The desired data type of the returned array. Default is float.
    Returns:
    np.ndarray: The 1D array read from the FreeFem file.
    Raises:
    AssertionError: If the FreeFem array to be imported is not 1D.
    """

    file = open(filename, "r")
    lines = file.readlines()
    first_line = lines[0]
    last_line = lines[-1]
    p = np.array(first_line.strip().split(" "), dtype=int)

    assert len(p) == 1, "FreeFem array to be imported is not 1D"

    tmp_arr = np.loadtxt(lines[1:-1], dtype=dtype).flatten()
    list_values = list(tmp_arr)

    last_row_vals = [
        p for p in last_line.split("\t") if len(p) > 1
    ]  # removes tabs and empty strings

    list_values = list_values + last_row_vals
    if dtype == float:
        return np.array(list_values, dtype=float)
    else:
        arr = complexifyall(list_values)
        return arr


def read_freefem_array(filename: str) -> np.ndarray:
    """
    Reads in array from file saved in FreeFem format.
    The first row of file is the shape of the array and indicates dimensionality.
    1D array will call separate method
    2D array will use numpy.loadtxt to read in the array and convert to complex if need be
    Parameters:
    -----------
    filename : str
        The path to the file containing the FreeFem array.
    Returns:
    --------
    np.ndarray
        A NumPy array containing the data from the FreeFem array. The array can be either 1D or 2D and may contain real or complex numbers.
    Notes:
    ------
    - For 1D arrays, the function determines the type (real or complex) based on the first entry.
    - For 2D arrays, the function determines the type (real or complex) based on the first entry.
    - Complex numbers are handled by the `complexifyall` function for 2D arrays.
    - The file format is expected to have the dimensions on the first line, followed by the array data.
    """

    # Load in file
    file = open(filename, "r")
    lines = file.readlines()
    p = np.array(lines[0].strip().split(" "), dtype=int)
    arr = np.zeros(tuple(p))

    if len(p) == 1:
        # Loading in 1D FreeFem array. May be real or complex. (Note strange format)
        # determine type
        first_entry = lines[1].strip().split("\t")[0]
        if "(" not in first_entry:
            arr = _read_1D_freefem_array(filename, dtype=float)
        else:
            arr = _read_1D_freefem_array(filename, dtype=tuple)

    elif len(p) == 2:
        # Loading in 2D FreeFem array. May be real or complex.
        first_entry = lines[1].strip().split("\t")[0]
        if "(" not in first_entry:
            # Real 2D array
            arr = np.loadtxt(
                filename,
                skiprows=1,
                dtype=float,
            )
        else:
            # Complex 2D array
            tmp_arr = np.loadtxt(
                filename,
                skiprows=1,
                dtype=tuple,
            )

            arr = complexifyall(tmp_arr)

    return arr


def read_freefem_sparsemat(filename: str, sparse=True):
    """
    Imports a sparse matrix from FreeFem++.

    Note: Requires matrix to be saved in CSR format.
    FreeFem++ changed to a different format, but a matrix can be cast
    to CSR using the FreeFem command "A.CSR;".
    TW
    Parameters:
    filename (str): The path to the FreeFEM output file containing the sparse matrix data.
    sparse (bool): If True, returns the matrix in Compressed Sparse Column (CSC) format.
                   If False, returns the matrix in List of Lists (LIL) format. Default is True.
    Returns:
    scipy.sparse.csc_matrix or scipy.sparse.lil_matrix: The sparse matrix read from the file.
    """

    file = open(filename, "r")
    line = file.readlines()[3].split(" ")[:2]  # Get size of sparse matrix
    A2 = scipy.sparse.lil_matrix((int(line[0]), int(line[1])))

    A = np.genfromtxt(filename, skip_header=4)

    A2[A[:, 0] - 1, A[:, 1] - 1] = A[:, 2]

    if sparse:
        return A2.tocsc()
    else:
        return A2


def params_to_freefem_command(
    params: ForwardSolverParams,
    solver_subdir,
    log_path,
    is_capacitance_calculated=0,
    is_full_capacitance_calculated=0,
    is_voltage_mat_calculated=0,
    is_python_used_as_solver=0,
    physics_model=0,
    export_mesh=0,
):
    """
    Constructs a command string to run a FreeFem++ simulation based on the provided parameters.
    Args:
        params (ForwardSolverParams): The parameters for the forward solver, including dimension, board type, solver file, etc.
        solver_subdir (str): The subdirectory where the solver is located.
        log_path (str): The path to the log file where the output will be written.
        is_capacitance_calculated (int, optional): Flag to indicate if capacitance calculation is enabled. Defaults to 0.
        is_full_capacitance_calculated (int, optional): Flag to indicate if full capacitance calculation is enabled. Defaults to 0.
        is_voltage_mat_calculated (int, optional): Flag to indicate if voltage matrix calculation is enabled. Defaults to 0.
        is_python_used_as_solver (int, optional): Flag to indicate if Python is used as the solver. Defaults to 0.
        physics_model (int, optional): The physics model to be used. Defaults to 0.
        export_mesh (int, optional): Flag to indicate if the mesh should be exported. Defaults to 0.
    Raises:
        ValueError: If the dimension is 3 and the board type is not "imported".
    Returns:
        str: The constructed command string to run the FreeFem++ simulation.
    """
    if params.dimension == 3 and params.board.lower() != "imported":
        raise ValueError("With three dimensions, only imported geometries can be used.")

    os_command = (
        f"FreeFem++ -nw -ne {params.solver_file} "
        f"freefemDir {solver_subdir} "
        "BPlot 0 "
        f"BComputeCap {int(is_capacitance_calculated)} "
        f"BComputeCapFull {int(is_full_capacitance_calculated)} "
        f"BComputeVolt {int(is_voltage_mat_calculated)} "
        f"BComputePython {int(is_python_used_as_solver)} "
        f"physicsModel {physics_model} "
        f"BExportMesh {int(export_mesh)} "
        f"nDims {int(params.dimension)} "
    )

    if params.board.lower() == "imported":
        os_command += "boardGeometry Imported "
        os_command += f"meshFile {os.path.abspath(params.mesh_file)} "
        os_command += (
            f"permittivityFile {os.path.abspath(params.material_parameter_file)} "
        )

    else:
        os_command += f"boardGeometry {params.board.replace('_', '-')} "

        if params.geometry is not None:
            # Geometric calls (defined in geometry_params.py)
            os_command += params.geometry.to_freefem()

        os_command += "BReadPixelEpsilon 1 BReadPixelSigma 1 "

    os_command += f"frequency {params.signal.frequency} > {log_path}"
    logger.info(f'Running FreeFem++ with command: "{os_command}"')
    return os_command


close_logger(logger)
