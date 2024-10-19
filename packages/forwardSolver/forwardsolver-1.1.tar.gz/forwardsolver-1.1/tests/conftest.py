# import os

# import pytest

from forwardSolver.tests.fixtures.device_data import *  # noqa: F401 F403
from forwardSolver.tests.fixtures.forward_solver import *  # noqa: F401 F403

# @pytest.fixture(autouse=True)
# def set_path():
#     freefem_path = (
#         "C:\Program Files (x86)\FreeFem++"  # Update this with the actual path
#     )
#     os.environ["PATH"] += os.pathsep + freefem_path
