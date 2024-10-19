import os
from distutils.util import strtobool
from dotenv import load_dotenv
from enum import Enum
from pathlib import Path

# Default configuration
EPSILON_0 = 8.854 * 1e-3  # Permittivity of free space (pF/mm)

# Conversion between units
SECONDS_TO_MICROSECONDS = 1e6  # Conversion from seconds to microseconds (-)
MICROSECONDS_TO_SECONDS = 1e-6  # Conversion from microseconds to seconds (-)
MEGA_OHM_TO_OHM = 1e6  # Conversion from mega ohms to ohms (-)
PICO_FARAD_TO_FARAD = 1e-12  # Conversion from pico farads to farads (-)

# Find the absolute path of the package root directory
ROOT_DIR = str(Path(__file__).absolute().parent.parent.parent)

# Set the directories
LOG_DIR = Path(ROOT_DIR, "logs")
CACHE_DIR = str(Path(ROOT_DIR, "cache"))
FREEFEM_DIR = str(Path(ROOT_DIR, "forwardSolver_2D"))
EXPERIMENTS_DIR = str(Path(ROOT_DIR, "experiments"))
CONFIG_TEMPLATE_PATH = str(Path(ROOT_DIR, ".env.template"))  # Path to the template

# Load default config from the .env.template file
load_dotenv(dotenv_path=CONFIG_TEMPLATE_PATH, override=False)

# Set up global variables from .env (or .env.template by default
CACHE_OUTPUT = bool(strtobool(os.getenv("CACHE_OUTPUT", "False")))
CACHE_INPUT = bool(strtobool(os.getenv("CACHE_INPUT", "False")))
CACHE_INPUT_VOLTAGE = bool(strtobool(os.getenv("CACHE_INPUT_VOLTAGE", "True")))

CREATE_PARALLEL_SUBDIR = bool(strtobool(os.getenv("CREATE_PARALLEL_SUBDIR", "True")))
DELETE_FREEFEM_FILES = bool(strtobool(os.getenv("DELETE_FREEFEM_FILES", "True")))
IS_CAP_CALCULATED = bool(strtobool(os.getenv("IS_CAP_CALCULATED", "False")))
IS_FULL_CAP_CALCULATED = bool(strtobool(os.getenv("IS_FULL_CAP_CALCULATED", "False")))
IS_VOLTAGE_MAT_CALCULATED = bool(strtobool(os.getenv("IS_VOLTAGE_MAT_CALCULATED", "True")))

IS_PYTHON_USED_AS_SOLVER = bool(strtobool(os.getenv("IS_PYTHON_USED_AS_SOLVER", "False")))
PHYSICS_MODEL = int(os.getenv("PHYSICS_MODEL", 0))

# Parameters for the numerical derivative
DERIVATIVE_EDGE_ORDER = (
    2  # Number of points to use to calculate derivative at each point.
)
NUM_ELEM_DERIVATIVE_IGNORE = 2  # Number of elements to ignore from the resulting array

ERROR_STRINGS = ["error", "erreur", "fail"]

# Data class to lookup relative permittivities
class RelativePermittivity:
    AIR = 1.0006
    PP3C = 2.26
    PC3C = 2.81
    AC3C = 3.01
    PA3C = 3.11
    FAT_PHANTOM = 1e3
    FIBROGLANDULAR_PHANTOM = 5e3
    WATER = 80
    TUMOUR_PHANTOM = 2e4
    SKIN_DRY = 1e4
    SKIN_WET = 1.2e4
    FAT = 1e3
    FIBROGLANDULAR = 5e3
    TUMOUR = 2e4
    ULTRASOUND_GEL = 80
    SOLDERCOAT = 3.0
    MINERAL_OIL = 3.2

# Enum to capture different types of problem aiming to be solved by the code
class SolverProblem(Enum):
    AIR = 1
    SINGLE_PHANTOM = 2

MAX_PARALLEL_CPU = 30  # Do not exceed this number even if logical cores are available

HDF_EXTENSIONS = (".h5", ".hdf", ".hdf5")

LINEARISED_INVERSE_APPROACHES = dict(
    InverseSolver=(
        "lstsq",
        "conjugate",
        "landweber",
    ),
    SolverInverseP1000=(
        "lstsq_trf",
        "lstsq_bvls",
        "landweber",
        "tikhonov",
    ),
)

NONLINEAR_INVERSE_APPROACHES = dict(
    InverseSolver=(
        "trf",
        "lm",
    ),
    SolverInverseP1000=(),
)

REGULARISATION_APPROACHES = dict(
    InverseSolver=(
        "tikhonov",
        "total_variation",
        "layer_dependent",
        "pixel_based",
    ),
    SolverInverseP1000=(
        "tikhonov",
        "landweber",
    ),
)

# Function to load custom config from a .env file
def load_custom_config(env_file=".env"):
    """
    Load custom configuration from a user-provided .env file.
    If no .env file is found, the package will continue to use default values.
    """
    env_path = Path(env_file)
    if env_path.exists():
        load_dotenv(env_file, override=True)
        print(f"Custom config loaded from {env_file}.")
    else:
        print(f"No custom .env file found at {env_file}, using default values.")
