from dataclasses import asdict, dataclass
from functools import cached_property
from typing import Optional

import numpy as np


@dataclass(kw_only=True)
class Pixels:
    """
    A class to represent and manage pixel regions for simulations.
    Attributes:
        create_standalone (Optional[bool]): Whether the file with FreeFEM code can be run independently.
        region_width (Optional[float]): Width of the pixel region.
        region_height (Optional[float]): Height of the pixel region.
        region_length (Optional[float]): Length of the pixel region.
        region_label (Optional[int]): Label representing the pixel region.
        num_pixel_rows (Optional[int]): Number of pixel rows.
        num_pixel_columns (Optional[int]): Number of pixel columns.
        num_pixel_layers (Optional[int]): Number of pixel depth layers if 3D.
        pixel_columns_per_row (Optional[np.ndarray]): Number of pixel columns for each row.
        permittivity_matrix (Optional[np.ndarray]): Array of permittivity values for each pixel.
        conductivity_matrix (Optional[np.ndarray]): Array of conductivity values for each pixel.
        pixel_type (Optional[str]): Type of the pixelation.
        circular_phantom_radius (Optional[float]): Radius of circular phantom region.
        circular_phantom_bore_radii (Optional[np.ndarray]): Radii of the bores of circular phantom.
        circular_phantom_bore_centre_distance (Optional[float]): Distance between the centres of the phantom and the bores.
        circular_phantom_angle (Optional[float]): Angle at which the circular phantom is placed.
        circular_phantom_thickness (Optional[float]): Array of thicknesses of the circular phantom.
    Methods:
        __eq__(self, other): Checks if two Pixels objects are equal by comparing their dictionaries.
        as_dict(self): Returns the object as a dictionary.
        num_total_pixels(self): Returns the total number of pixels based on the pixel type and dimensions.
    """

    # Whether the file with freefem code can be run independently
    create_standalone: Optional[bool] = None
    # width of the pixel region
    region_width: Optional[float] = None
    # height of the pixel region
    region_height: Optional[float] = None
    # length of the pixel region
    region_length: Optional[float] = None
    # label representing the pixel region
    region_label: Optional[int] = None
    # number of pixel rows
    num_pixel_rows: Optional[int] = None
    # number of pixel columns
    num_pixel_columns: Optional[int] = None
    # number of pixel depth layers if 3D
    num_pixel_layers: Optional[int] = None
    # number of pixel columns for each row
    pixel_columns_per_row: Optional[np.ndarray] = None
    # array of permittivity values for each pixel
    permittivity_matrix: Optional[np.ndarray] = None
    # array of conductivity values for each pixel
    conductivity_matrix: Optional[np.ndarray] = None
    # type of the pixelation
    pixel_type: Optional[str] = None
    # radius of circular phantom region
    circular_phantom_radius: Optional[float] = None
    # radii of the bores of circular phantom
    circular_phantom_bore_radii: Optional[np.ndarray] = None
    # distance between the centres of the phantom and the bores
    circular_phantom_bore_centre_distance: Optional[float] = None
    # angle at which the circular phantom is placed
    circular_phantom_angle: Optional[float] = None
    # array of thicknesses of the circular phantom
    circular_phantom_thickness: Optional[float] = None

    def __eq__(self, other):
        try:
            np.testing.assert_equal(self.as_dict(), other.as_dict())
        except AssertionError:
            return False
        return True

    def as_dict(self):
        """
        Return the object as a dictionary
        """
        return asdict(self)

    @cached_property
    def num_total_pixels(self):
        if (
            self.pixel_type == "curved_rectangle"
            or self.pixel_type == "circular_phantom"
        ):
            if self.num_pixel_layers:
                return (
                    self.num_pixel_rows * self.num_pixel_columns * self.num_pixel_layers
                )
            else:
                return self.num_pixel_rows * self.num_pixel_columns
        elif self.pixel_type == "curved_rectangle_nonuniform":
            return np.sum(self.pixel_columns_per_row)
        else:
            raise NotImplementedError(
                f"The pixel type {self.pixel_type} is not a valid pixel types"
            )
