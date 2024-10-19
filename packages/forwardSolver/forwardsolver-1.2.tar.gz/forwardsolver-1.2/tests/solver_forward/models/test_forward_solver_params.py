import json
from pathlib import Path

import pytest

from forwardSolver.scripts.params.forward_solver_params import ForwardSolverParams
from forwardSolver.scripts.params.geometry_params import GeometryParams
from forwardSolver.scripts.utils.dict import check_all_keys_none
from forwardSolver.scripts.utils.json_coder import CustomJsonDecoder


def test_forward_parameters_initialise_empty():
    # Initialise without args should all be none
    forward_parameters = ForwardSolverParams(**{})
    assert check_all_keys_none(forward_parameters.as_dict())

    # Initialise with empty dict should all be none
    forward_parameters = ForwardSolverParams()
    assert check_all_keys_none(forward_parameters.as_dict())


def test_forward_parameters_initialise_key():
    # Should raise TypeError when an extra key is added to dict but not dataclass
    with pytest.raises(TypeError):
        ForwardSolverParams(**{"donkey123": 123})
    with pytest.raises(TypeError):
        ForwardSolverParams(**{"geometry": 123})
    with pytest.raises(TypeError):
        ForwardSolverParams(**{"geometry": {"donkey123": 12}})


def test_forward_parameters_equality():
    # test equality operator and as_dict() function
    forward_parameters1 = ForwardSolverParams(
        **{"board": "hello", "geometry": {"mesh_elements_on_border": 10}}
    )
    forward_parameters2 = ForwardSolverParams(**forward_parameters1.as_dict())
    assert forward_parameters1 == forward_parameters2

    forward_parameters1.board = "Hello"
    assert forward_parameters1 != forward_parameters2

    # test equality when initialising with dict or objects
    forward_parameters3 = ForwardSolverParams(
        **{"board": "hello", "geometry": {"mesh_elements_on_border": 10}}
    )
    forward_parameters4 = ForwardSolverParams(
        board="hello", geometry=GeometryParams(mesh_elements_on_border=10)
    )
    assert forward_parameters3 == forward_parameters4


def test_geometry_files_work():
    """
    Make sure that all geometry configurations work
    """
    for path in Path("src/params/solver_forward/geometries").rglob("*.json"):
        with open(path, "r") as f:
            forward_solver_params_dict = json.load(f, cls=CustomJsonDecoder)
            _ = ForwardSolverParams(**forward_solver_params_dict)

        # make sure files can be run using factory method
        config_name = path.name.replace(".json", "")
        ForwardSolverParams.factory(config_name)

    # make sure non-existent files raise error when using factory method
    with pytest.raises(ValueError):
        ForwardSolverParams.factory("donkey123")
