import numpy as np
import pytest

from forwardSolver.scripts.geometry_generation.board_models.P3000_005_geometry import (
    GeometryP30002D,
    GeometryP30003D,
)
from forwardSolver.scripts.geometry_generation.geometry_interface import (
    clear_models,
    is_initialised,
)


def _new_geometric_model(dim: int = 2):
    if is_initialised():
        clear_models()
    if dim == 2:
        return GeometryP30002D()
    else:
        return GeometryP30003D()


# tests below ensure there are no errors in geometry generation, but do not test
# integrity/ corectness of the geometry generated


def test_add_rectangular_pixelation():
    basic_model = _new_geometric_model()
    with pytest.raises(TypeError):
        basic_model.add_rectangular_pixelation()

    # add pixels with perm jj
    basic_model.add_domain(
        shape="rectangle",
        width=280.0,
        height=150.0,
    )
    assert (
        len(
            basic_model.add_rectangular_pixelation(
                pixel_permittivity=np.ones((5, 3)), columns=5, rows=3
            )
        )
        == 15
    )


def test_add_P3000_005_board_2D():
    basic_model = _new_geometric_model()
    basic_model.add_domain(shape="rectangle", width=280.0, height=150.0)
    basic_model.add_P3000_005_board()


def test_add_P3000_005_board_3D():
    basic_model = _new_geometric_model(dim=3)
    basic_model.add_domain(shape="box", width=280.0, height=150.0, depth=400)
    basic_model.add_P3000_005_board()


def test_add_cuboid_pixelation():
    basic_model = _new_geometric_model(dim=3)
    with pytest.raises(TypeError):
        basic_model.add_cuboid_pixelation()

    # add pixels with perm jj
    basic_model.add_domain(
        shape="box",
        width=280.0,
        height=150.0,
        depth=300.0,
    )
    assert (
        len(
            basic_model.add_cuboid_pixelation(
                pixel_permittivity=np.ones((5, 3, 4)),
                columns=5,
                rows=3,
                layers=2,
            )
        )
        == 30
    )
