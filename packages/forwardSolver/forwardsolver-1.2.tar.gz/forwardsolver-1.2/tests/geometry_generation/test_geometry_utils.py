from math import pi

import numpy as np
import pytest

from forwardSolver.scripts.geometry_generation.geometry_utils import (
    cartesian_to_polar2D,
    compute_cord_angle,
    compute_vector,
    point_along_arc,
    polar2D_to_cartesian,
)


@pytest.mark.parametrize(
    ("arc_angle, radius, centre, output"),
    [
        (0, 1, (0, 0), (0, -1)),  # 0,0 edge case
        (pi / 2, 1, (0, 0), (1, 0)),  # pi/2
        (pi / 2, 0, (0, 0), (0, 0)),  # radius = 0 edge case
        (pi / 2, -1, (0, 0), None),  # radius = -1 warning
    ],
)
def test_point_along_arc(arc_angle, radius, centre, output):
    if output:
        np.testing.assert_array_almost_equal(
            point_along_arc(arc_angle=arc_angle, radius=radius, centre=centre),
            np.array(output),
        )
    else:
        assert (
            point_along_arc(arc_angle=arc_angle, radius=radius, centre=centre) is None
        )


@pytest.mark.parametrize(
    ("point, origin, degrees, output"),
    [
        ([0, 0], [0, 0], False, (0, 0)),  # 0,0 edge case
        ([1, pi / 2], [0, 0], False, (0, 1)),  # 0 origin, 1, pi/2 point
        ([1, 90], [0, 0], True, (0, 1)),  # 0 origin, 1, pi/2 point
        ([1, 0], [0, 0], False, (1, 0)),  # 0 origin, 1, 0 point
        ([-1, pi / 2], [0, 0], False, (0, -1)),  # 0 origin, -1, pi/2 point
        ([0, 0], [1, pi / 2], False, (1, pi / 2)),  # 0 point, 1, pi/2 origin
    ],
)
def test_polar2D_to_cartesian(point, origin, degrees, output):
    np.testing.assert_array_almost_equal(
        polar2D_to_cartesian(
            point=np.array(point), origin=np.array(origin), degrees=degrees
        ),
        np.array(output),
    )


@pytest.mark.parametrize(
    ("point, origin, degrees, output"),
    [
        ([0, 0], [0, 0], False, (0, 0)),  # 0,0 edge case
        # 0 origin, c(0,1) p(1, pi/2) point
        ([0, 1], [0, 0], False, (1, pi / 2)),
        ([0, 1], [0, 0], True, (1, 90)),
        # 0 origin,  c(1, 0) p(1, 0) point
        ([1, 0], [0, 0], False, (1, 0)),
        # 0 origin, c(1, 0)  p(-1, pi/2) p(1, -pi/2) point
        ([0, -1], [0, 0], False, (1, -pi / 2)),
        # c(1, 0) origin, c(0,0) p(1,pi) point
        ([0, 0], [1, 0], False, (1, pi)),
    ],
)
def test_cartesian_to_polar2D(point, origin, degrees, output):
    np.testing.assert_array_almost_equal(
        cartesian_to_polar2D(
            point=np.array(point), origin=np.array(origin), degrees=degrees
        ),
        np.array(output),
    )


@pytest.mark.parametrize(
    ("radius, chord_length, degrees, cord_angle"),
    [
        (0, 0, False, None),
        (1, 1, False, pi / 3),
        (1, 1, True, 60),
    ],
)
def test_compute_cord_angle(radius, chord_length, degrees, cord_angle):
    if cord_angle:
        np.testing.assert_almost_equal(
            compute_cord_angle(
                radius=radius, chord_length=chord_length, degrees=degrees
            ),
            cord_angle,
        )
    else:
        assert (
            compute_cord_angle(
                radius=radius, chord_length=chord_length, degrees=degrees
            )
            is None
        )


def test_compute_vector():
    np.testing.assert_array_almost_equal(
        compute_vector(np.array([2, 0, 0, 0]), np.array([0, 1, 0, 1]), False),
        np.array([-2, 1, 0, 1]),
    )
