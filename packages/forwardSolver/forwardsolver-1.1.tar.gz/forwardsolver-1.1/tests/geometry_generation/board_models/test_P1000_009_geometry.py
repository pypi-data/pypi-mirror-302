import numpy as np
import pytest

from forwardSolver.scripts.geometry_generation.board_models.P1000_009_geometry import (
    GeometryP10002D,
)
from forwardSolver.scripts.geometry_generation.geometry_interface import (
    clear_models,
    is_initialised,
)


def _new_geometric_model():
    if is_initialised():
        clear_models()
    return GeometryP10002D()


def test_compute_electrode_centres_009_board():

    # Note: tests are in polar coordinates

    basic_model = _new_geometric_model()
    # check the output for default P1000-009 inputs
    assert basic_model._compute_electrode_centres_009_board(
        N_electrodes=15,
        electrode_gap=4,
        electrode_width=6,
        radius_curvature=71.8,
        chord_length=126.15,
    ) == [
        (71.8, -2.545726688911888),
        (71.8, -2.406450922895175),
        (71.8, -2.267175156878462),
        (71.8, -2.127899390861749),
        (71.8, -1.9886236248450357),
        (71.8, -1.8493478588283228),
        (71.8, -1.7100720928116098),
        (71.8, -1.5707963267948966),
        (71.8, -1.4315205607781833),
        (71.8, -1.2922447947614704),
        (71.8, -1.1529690287447574),
        (71.8, -1.0136932627280442),
        (71.8, -0.8744174967113311),
        (71.8, -0.735141730694618),
        (71.8, -0.5958659646779049),
    ]
    # Intermediate curvature
    assert basic_model._compute_electrode_centres_009_board(
        N_electrodes=15,
        electrode_gap=4,
        electrode_width=6,
        radius_curvature=500,
        chord_length=154.70,
    ) == [
        (500, -1.7107963267948967),
        (500, -1.6907963267948967),
        (500, -1.6707963267948966),
        (500, -1.6507963267948966),
        (500, -1.6307963267948966),
        (500, -1.6107963267948966),
        (500, -1.5907963267948966),
        (500, -1.5707963267948966),
        (500, -1.5507963267948965),
        (500, -1.5307963267948965),
        (500, -1.5107963267948965),
        (500, -1.4907963267948965),
        (500, -1.4707963267948965),
        (500, -1.4507963267948965),
        (500, -1.4307963267948964),
    ]
    # Flat board
    assert basic_model._compute_electrode_centres_009_board(
        N_electrodes=15,
        electrode_gap=4,
        electrode_width=6,
        radius_curvature=1e7,
        chord_length=155.32,
    ) == [
        (10000000.0, -1.5708033267948966),
        (10000000.0, -1.5708023267948965),
        (10000000.0, -1.5708013267948966),
        (10000000.0, -1.5708003267948965),
        (10000000.0, -1.5707993267948965),
        (10000000.0, -1.5707983267948966),
        (10000000.0, -1.5707973267948965),
        (10000000.0, -1.5707963267948966),
        (10000000.0, -1.5707953267948966),
        (10000000.0, -1.5707943267948965),
        (10000000.0, -1.5707933267948966),
        (10000000.0, -1.5707923267948967),
        (10000000.0, -1.5707913267948965),
        (10000000.0, -1.5707903267948966),
        (10000000.0, -1.5707893267948965),
    ]


# tests below ensure there are no errors in geometry generation, but do not test
# integrity/ corectness of the geometry generated
def test_add_curved_rectangle_outline():
    basic_model = _new_geometric_model()
    # tag of the outer loop generated is a postive int
    assert basic_model.add_curved_rectangle_outline(radius_curvature=0.1) > 0
    # warning is generated (and None returned) if radius_curvture = 0
    # assert basic_model.add_curved_rectangle_outline() == None


def test_add_curved_rectangular_pixelation():
    basic_model = _new_geometric_model()
    with pytest.raises(TypeError):
        basic_model.add_curved_rectangular_pixelation()
    # add pixels with perm jj
    basic_model.add_domain(
        shape="rectangle",
        width=375.0,
        height=150.0,
    )
    assert (
        len(
            basic_model.add_curved_rectangular_pixelation(
                pixel_permittivity=np.ones((5, 3)), columns=5, rows=3
            )
        )
        == 15
    )


def test_add_P1000_009_board():
    basic_model = _new_geometric_model()
    basic_model.add_domain(shape="rectangle", width=375.0, height=150.0)
    basic_model.add_P1000_009_board()
