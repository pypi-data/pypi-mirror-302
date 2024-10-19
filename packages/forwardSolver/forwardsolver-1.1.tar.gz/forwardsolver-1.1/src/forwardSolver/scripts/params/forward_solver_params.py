import json
from dataclasses import asdict, dataclass
from pathlib import Path
from types import NoneType
from typing import Optional

import numpy as np

from forwardSolver.scripts.params.geometry_params import GeometryParams
from forwardSolver.scripts.params.sensor_params import SensorParams
from forwardSolver.scripts.params.signal_params import SignalParams
from forwardSolver.scripts.params.simulation_params import SimulationParams
from forwardSolver.scripts.utils.constants import ROOT_DIR
from forwardSolver.scripts.utils.json_coder import CustomJsonDecoder
from forwardSolver.scripts.utils.pixels import Pixels


@dataclass(kw_only=True)
class ForwardSolverParams:
    """
    Params to define forward solver problem.
    Attributes:
        board (Optional[str]): Board model name, default is None.
        solver_dir (Optional[str]): Directory where FreeFEM script for the specific board is stored.
        solver_file (Optional[str]): Name of the FreeFEM script.
        mesh_file (Optional[str]): Mesh file if board == "Imported".
        material_parameter_file (Optional[str]): Material parameter file if board == "Imported".
        dimension (Optional[int]): Dimensionality of the problem, defaults to 2. 3D only works with imported geometry.
        simulation (Optional[SimulationParams]): Simulation parameters defining what time quantities and what to compute.
        signal (Optional[SignalParams]): Parameters to define the input signal (by default a trapezoidal wave).
        geometry (Optional[GeometryParams]): Parameters to define the geometry of everything in the system.
        sensor (Optional[SensorParams]): Parameters related to the electrical characteristics of the sensor.
        pixels (Optional[Pixels]): Parameters that define the region under study.
        solver_subdir (Optional[str]): Folder where specific run data is stored.
    Methods:
        __post_init__(): Initializes nested parameter objects and validates imported geometry parameters.
        __eq__(other): Checks equality by comparing the dictionary representation of the objects.
        as_dict(): Returns the dictionary representation of the object.
        factory(geometry): Creates a `ForwardSolverParams` object from a geometry file name.
    """

    # Board model name, default = P1000-001
    board: Optional[str] = None

    # INFO: FreeFEM requires that the scripts to solve for different geometries
    #       must be stored in different folders. Therefore, each forward solver
    #       needs to know where the script for the specific board is stored

    # Directory where FreeFEM script for the specific board is stored
    solver_dir: Optional[str] = None

    # Name of the FreeFEM script
    solver_file: Optional[str] = None

    # mesh file if board == "Imported"
    mesh_file: Optional[str] = None

    # material parameter file if board == "Imported"
    material_parameter_file: Optional[str] = None

    # dimensionality of the problem. Defaults to 2. 3D only works with imported geometry
    dimension: Optional[int] = None

    # Simulation parameters defining what time quantities and what to compute
    simulation: Optional[SimulationParams] = None

    # Parameters to define the input signal (by default a trapezoidal wave)
    signal: Optional[SignalParams] = None

    # Parameters to define the geometry of everything in the system
    geometry: Optional[GeometryParams] = None

    # Parameters related to the electrical characteristics of the sensor
    sensor: Optional[SensorParams] = None

    # Parameters that define the region under study
    pixels: Optional[Pixels] = None

    # Folder where specific run data is stored
    solver_subdir: Optional[str] = None

    def __post_init__(self):
        if not isinstance(self.simulation, (NoneType, SimulationParams)):
            self.simulation = SimulationParams(**self.simulation)
        if not isinstance(self.signal, (NoneType, SignalParams)):
            self.signal = SignalParams(**self.signal)
        if not isinstance(self.geometry, (NoneType, GeometryParams)):
            self.geometry = GeometryParams(**self.geometry)
        if not isinstance(self.sensor, (NoneType, SensorParams)):
            self.sensor = SensorParams(**self.sensor)
        if not isinstance(self.pixels, (NoneType, Pixels)):
            self.pixels = Pixels(**self.pixels)

        if self.board is not None:
            if self.board.lower().startswith("p"):
                self.dimension = 2
            elif self.board.lower() == "Imported":
                if (
                    self.mesh_file is None
                    or self.material_parameter_file is None
                    or self.dimension is None
                ):
                    raise ValueError(
                        "If using an imported geometry, you must specify "
                        "mesh_file, material_parameter_file, and dimensions."
                    )

    def __eq__(self, other):
        try:
            np.testing.assert_equal(self.as_dict(), other.as_dict())
        except AssertionError:
            return False
        return True

    def as_dict(self):
        return asdict(self)

    @staticmethod
    def factory(geometry):
        """
        Create a `ForwardSolverParams` object from a geometry file name.
        Note that the file must exist in the geometries folder:
        "src/scripts/params/geometries/{`geometry`}.json"
        """
        file = Path(ROOT_DIR, f"scripts/params/geometries/{geometry}.json")
        if file.exists():
            with open(file, "r") as f:
                forward_solver_params_dict = json.load(f, cls=CustomJsonDecoder)
                return ForwardSolverParams(**forward_solver_params_dict)
        raise ValueError(
            f"File ({ROOT_DIR}/scripts/params/geometries/{geometry}.json) does not exist"
        )
