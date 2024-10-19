import numpy as np

from forwardSolver.scripts.utils.logging import get_logger

logger = get_logger(__name__)


def point_along_arc(
    arc_angle: float,
    radius: float,
    centre: tuple,
) -> np.ndarray:
    """
    Computes the cartesian coordinates of point along circular arc centred
    at centre_curvature with radius radius_curvature.
    Angle is measured from negative theta

    Args:
        arc_angle (float): arc angle in radians
        radius (float): arc radius
        centre (tuple): 2D cartesian coordinates of the arc centre

    Returns:
        np.ndarray: 2D cartesian coordinates of the point along arc
    """
    if radius >= 0:
        point_x = radius * np.sin(arc_angle)
        point_y = -radius * np.cos(arc_angle)
        return np.array([point_x + centre[0], point_y + centre[1]])
    else:
        logger.warning("Radius needs to be >=0")


def polar2D_to_cartesian(
    point: np.ndarray,
    origin: np.ndarray,
    degrees: bool = False,
) -> np.ndarray:
    """
    Computes cartesian coordinates given 2D polar coordinates (r, theta)
    and polar coordinate origin

    Args:
        point (np.ndarray): polar coordinates of a point (r, theta)
        origin (np.ndarray): polar coordinates of the origin (r, theta)
        degrees (bool, optional): flag for theta input in degrees (default radians).
                                  Defaults to False.

    Returns:
        np.ndarray: 2D cartesian coordinates of the point
    """

    assert len(point) == 2, (
        "Incorrect shape in polar2D_to_cartesian, " f"expected (2,) got {len(point)}"
    )

    radius = point[0]
    theta = point[1]
    if degrees:
        theta = np.pi * theta / 180

    point_x = radius * np.cos(theta)
    point_y = radius * np.sin(theta)

    return origin + np.array([point_x, point_y])


def cartesian_to_polar2D(
    point: np.ndarray,
    origin: np.ndarray,
    degrees: bool = False,
) -> np.ndarray:
    """Returns 2D polar coordinates (r, theta) centred at given origin of the point (x,y).
    Point is in cartesian coordinates from (0,0) i.e. there is a change of origin

    Args:
        point (np.ndarray): cartesian point coordinates
        origin (np.ndarray): cartesian origin coordinates for output
        degrees (bool, optional): flag for theta output in degrees (default radians).
                                  Defaults to False.

    Returns:
        np.ndarray: 2D polar coordinates (r, theta)
    """

    vector = np.array(point - origin)
    r = np.linalg.norm(vector)

    theta = np.arctan2(vector[1], vector[0])
    if degrees:
        theta = 180 * theta / np.pi

    return np.array([r, theta])


def compute_cord_angle(
    radius: float,
    chord_length: float,
    degrees: bool = False,
) -> float:
    """Computes angle at the centre of the circle formed by the horizontal chord
    intersecting the circle BELOW the origin.

    Args:
        radius (float): radius of the circle
        chord_length (float): cord length
        degrees (bool, optional): flag for theta output in degrees. Defaults to False.

    Returns:
        float: cord angle
    """
    if radius > 0:
        theta = np.arcsin((0.5 * chord_length) / radius) * 2

        if degrees:
            theta = 180 * theta / np.pi
        return theta
    else:
        logger.warning("Radius needs to be > 0")


def compute_chord_length(
    radius: float,
    arc_length: float,
    degrees: bool = False,
) -> float:
    """Computes the horizontal chord length between the ends of the symmetric circular
    arc of given length

    Args:
        radius (float): radius of the circle
        arc_length (float): cord angle
        degrees (bool, optional): flag for theta output in degrees. Defaults to False.

    Returns:
        float: cord length
    """
    if radius > 0:
        chord_angle = arc_length / radius
        chord_length = 2 * radius * np.sin(0.5 * chord_angle)

        if degrees:
            chord_length = 2 * radius * np.sin(0.5 * chord_angle * np.pi / 180)
        return chord_length
    else:
        logger.warning("Radius needs to be > 0")


def compute_vector(
    point1: np.ndarray,
    point2: np.ndarray,
    unit: bool = True,
) -> np.ndarray:
    """
    Function to compute vector pointing from point 1 to point 2.
    Works in n-dimensions.

    Args:
        point1 (np.ndarray): end point of the vector - cartesian coords
        point2 (np.ndarray): start point of the vector - cartesian coords
        unit (bool, optional): flag for unit vector output. Defaults to True.

    Returns:
        np.ndarray: vector coordinates
    """
    assert (
        point1.shape == point2.shape
    ), "Inconsistent shapes between points in compute_vector"

    vector = np.array(point2 - point1)

    if unit:
        vector = vector / np.linalg.norm(vector)

    return vector
