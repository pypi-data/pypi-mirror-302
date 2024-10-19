import pytest

from forwardSolver.scripts.params.geometry_params import GeometryParams
from forwardSolver.scripts.utils.dict import check_all_keys_none


def test_geometry_params_initialise_empty():
    # Initialise without args should all be none
    geometry_params = GeometryParams(**{})
    assert check_all_keys_none(geometry_params.as_dict())

    # Initialise with empty dict should all be none
    geometry_params = GeometryParams()
    assert check_all_keys_none(geometry_params.as_dict())


def test_geometry_params_initialise_key():
    # Should raise TypeError when an extra key is added to dict but not dataclass
    with pytest.raises(TypeError):
        GeometryParams(**{"donkey123": 123})


def test_geometry_params_equality():
    # test equality operator and as_dict() function
    geometry_params1 = GeometryParams(
        mesh_elements_on_border=21, mesh_length_scale=13.32
    )
    geometry_params2 = GeometryParams(**geometry_params1.as_dict())
    assert geometry_params1 == geometry_params2

    geometry_params1.domain_height = 300
    assert geometry_params1 != geometry_params2
