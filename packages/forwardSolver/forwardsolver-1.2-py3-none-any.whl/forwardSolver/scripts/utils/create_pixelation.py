import abc
from typing import Optional

import numpy as np

from forwardSolver.scripts.utils.pixels import Pixels


def make_material_parameter_file(
    material_parameter_matrix: np.ndarray,
    file_name: str,
    num_pixel_columns: int = 10,
    num_pixel_rows: int = 10,
    default_parameter_value: float = 1.0006,
) -> None:
    """
    Define the parameter (permittivity or conductivity) value for each pixel. The results are saved to a text file.

    Args:
        permittivity_matrix: permittivity_matrix as numpy array
        file_name: output filename
        num_pixel_columns: number of pixel columns
        num_pixel_rows: number of pixel rows
        default_parameter_value: a default uniform parameter value if
                          the material_parameter_matrix is not specified
    Returns:
        None
    """

    # permittivities
    if material_parameter_matrix is None:
        material_parameter_matrix = (
            np.ones((num_pixel_rows, num_pixel_columns))
            * default_parameter_value
        )

    with open(file_name, "w") as file:
        np.savetxt(file, material_parameter_matrix)


class Pixelation(abc.ABC):
    """
    The pixelation class with the methods to define the lines of freefem code
    to be written a file for creating the pixel region.
    Attributes:
        num_pixel_rows (int): Number of pixel rows.
        num_pixel_columns (int): Number of pixel columns.
        num_total_pixels (int): Total number of pixels.
        permittivity_matrix (list): Matrix of permittivity values for each pixel.
        conductivity_matrix (list): Matrix of conductivity values for each pixel.
        region_offset_x (float): Offset of the region in the x-direction.
        region_offset_y (float): Offset of the region in the y-direction.
        fflines (list): List of FreeFem code lines.
        fflines_header (list): List of FreeFem header code lines.
        fflines_pixel_segments (list): List of FreeFem code lines for pixel segments.
        fflines_pixel_function (list): List of FreeFem code lines for pixel function.
        fflines_standalone_mesh (list): List of FreeFem code lines for standalone mesh.
        fflines_pixel_centres (list): List of FreeFem code lines for pixel centres.
        subdir (str): Subdirectory for output files.
        filename_permittivity (str): Filename for permittivity values.
        filename_conductivity (str): Filename for conductivity values.
        filename_region (str): Filename for the pixelated region script.
    Methods:
        make_pixel_header(): Add FreeFem header code for "includes" and initialisations.
        make_pixel_segments(): Add FreeFem code to define the segments and borders defining pixelated region.
        make_pixel_function(): Add FreeFem code to define the pixelated region as a function to be used in the mesh generation.
        make_standalone_mesh(): Create the mesh. This function should be used when running the resulting script directly.
        make_pixel_centres(): Define the center of each pixel, this will be used to assign properties to individual regions of the geometry.
        create_pixelation(): Writes the FreeFem code lines to the output edp file.
    """

    def __init__(
        self,
        *,
        params_pixels: Pixels,
        region_offset_x: float = 0.0,
        region_offset_y: float = 0.0,
        subdir: str,
    ) -> None:
        self.num_pixel_rows = params_pixels.num_pixel_rows
        self.num_pixel_columns = params_pixels.num_pixel_columns
        self.num_total_pixels = params_pixels.num_total_pixels
        self.permittivity_matrix = params_pixels.permittivity_matrix
        self.conductivity_matrix = params_pixels.conductivity_matrix
        self.region_offset_x = region_offset_x
        self.region_offset_y = region_offset_y
        self.fflines = []
        self.fflines_header = []
        self.fflines_pixel_segments = []
        self.fflines_pixel_function = []
        self.fflines_standalone_mesh = []
        self.fflines_pixel_centres = []
        self.subdir = subdir
        self.filename_permittivity = "pixelEpsilons.txt"
        self.filename_conductivity = "pixelSigmas.txt"
        self.filename_region = "pixel_region.edp"

    @abc.abstractmethod
    def make_pixel_header(self) -> None:
        """
        Add FreeFem header code for "includes" and initialisations.
        """
        pass

    @abc.abstractmethod
    def make_pixel_segments(self) -> None:
        """
        Add FreeFem code to define the segments and borders defining pixelated region.
        """
        pass

    @abc.abstractmethod
    def make_pixel_function(self) -> None:
        """
        Add FreeFem code to define the pixelated region as a function
        to be used in the mesh generation.
        """
        pass

    def make_standalone_mesh(self) -> None:
        """
        Create the mesh.
        This function should be used when running the resulting script directly.
        """
        self.fflines_standalone_mesh.append(
            "// Macro to generate the mesh. "
            + "(Can't have comments within macro environment)\n"
        )
        self.fflines_standalone_mesh.append("macro createMesh(h)\n")
        self.fflines_standalone_mesh.append("mesh Th = buildmesh(\n")
        self.fflines_standalone_mesh.append("    pixelRegion\n")
        self.fflines_standalone_mesh.append(");\n")
        self.fflines_standalone_mesh.append("// End of macro\n")
        self.fflines_standalone_mesh.append("\n" * 2)

        self.fflines_standalone_mesh.append("createMesh(h);\n")
        self.fflines_standalone_mesh.append("plot(Th);\n")
        self.fflines_standalone_mesh.append("\n" * 2)

    @abc.abstractmethod
    def make_pixel_centres(self) -> None:
        """
        Define the center of each pixel, this will be used to assign properties to
        individual regions of the geometry.
        """
        pass

    def create_pixelation(self) -> None:
        """Writes the freefem code lines to the output edp file"""
        self.make_pixel_header()
        self.make_pixel_segments()
        self.make_pixel_function()
        if self.create_standalone:
            self.make_standalone_mesh()
        make_material_parameter_file(
            self.permittivity_matrix,
            self.subdir + self.filename_permittivity,
            self.num_pixel_columns,
            self.num_pixel_rows,
        )
        make_material_parameter_file(
            self.conductivity_matrix,
            self.subdir + self.filename_conductivity,
            self.num_pixel_columns,
            self.num_pixel_rows,
            default_parameter_value=0.0,
        )
        self.make_pixel_centres()
        self.fflines = (
            self.fflines_header
            + self.fflines_pixel_segments
            + self.fflines_pixel_function
            + self.fflines_standalone_mesh
            + self.fflines_pixel_centres
        )
        with open(self.subdir + self.filename_region, "w") as file:
            file.writelines(self.fflines)


class PixelationCurvedRectangleNonuniform(Pixelation):
    """ "
    A class to create a non-uniform pixelation of a curved rectangular region.
    This class extends the Pixelation class and provides methods to generate
    FreeFem code for defining pixelated regions with non-uniform pixel sizes
    in a curved rectangular geometry.
    Attributes:
        create_standalone (bool): Flag indicating if the pixelation is standalone.
        region_label (int): Label for the region.
        region_width (float): Width of the region.
        region_height (float): Height of the region.
        pixel_columns_per_row (np.ndarray): Number of pixel columns per row.
        num_pixel_geometry_rows (int): Number of rows in the pixel geometry.
        num_pixel_geometry_columns (int): Number of columns in the pixel geometry.
        extra_layers (Optional[list]): Additional layers to be considered.
        pixel_columns_horizontal_segments (np.ndarray): Number of horizontal segments in each row.
    Methods:
        _split_horizontal_segments() -> np.ndarray:
            Returns a list with the number of horizontal segments in each row.
        _draw_vertical_edge(vertical_line_index: int, segment_index: int, extra_layers_string: str) -> None:
            Draws the segments of the vertical lines of the pixels.
        _draw_horizontal_edge(horizontal_line_index: int, segment_index: int, extra_layers_string: str) -> None:
            Draws the segments of the horizontal lines of the pixels.
        make_pixel_header() -> None:
            Adds FreeFem header code for "includes" and initializations.
        make_pixel_segments() -> None:
            Adds FreeFem code to define the segments and borders defining the pixelated region.
        make_pixel_function() -> None:
            Adds FreeFem code to define the pixelated region as a function to be used in the mesh generation.
        make_pixel_centres() -> None:
            Defines the center of each pixel, which will be used to assign properties to individual regions of the geometry.
    """

    def __init__(
        self,
        *,
        params_pixels: Pixels,
        extra_layers: Optional[list] = None,
        subdir: str = "./",
    ) -> None:
        self.create_standalone = params_pixels.create_standalone
        self.region_label = params_pixels.region_label
        self.region_width = params_pixels.region_width
        self.region_height = params_pixels.region_height

        if params_pixels.pixel_columns_per_row is not None:
            self.pixel_columns_per_row = params_pixels.pixel_columns_per_row
        else:
            self.pixel_columns_per_row = (
                params_pixels.num_pixel_columns
                * np.ones((params_pixels.num_pixel_rows, 1))
            )
        self.num_pixel_geometry_rows = len(self.pixel_columns_per_row)
        self.num_pixel_geometry_columns = self.pixel_columns_per_row[-1]
        self.extra_layers = extra_layers
        super().__init__(
            params_pixels=params_pixels,
            subdir=subdir,
        )

        self.pixel_columns_horizontal_segments = (
            self._split_horizontal_segments()
        )

    def _split_horizontal_segments(self) -> np.ndarray:
        """Returns a list with number of horizontal segments in each row"""
        pixel_columns_horizontal_segments = np.append(
            self.pixel_columns_per_row, self.pixel_columns_per_row[-1]
        )
        for iloop in range(len(self.pixel_columns_per_row) - 1):
            pixel_columns_horizontal_segments[iloop + 1] = np.lcm(
                self.pixel_columns_per_row[iloop + 1],
                self.pixel_columns_per_row[iloop],
            )
        return pixel_columns_horizontal_segments

    def _draw_vertical_edge(
        self,
        vertical_line_index: int,
        segment_index: int,
        extra_layers_string: str,
    ) -> None:
        """Draws the segments of the vertical lines of the pixels"""
        self.fflines_pixel_segments.append(
            f"border RegionMiddleV{vertical_line_index}s{segment_index}"
            + f"(t={segment_index+1}*regionH/{self.num_pixel_geometry_rows}, "
            + f"{segment_index}*regionH/{self.num_pixel_geometry_rows})"
            + "{x = (rCurvature + t - xMaterialGap - regionH - xElecH"
            + extra_layers_string
            + ")*sin((-regionW/2 + "
            + f"{vertical_line_index}"
            + f"*regionW/{self.pixel_columns_per_row[segment_index]} "
            + "+ regionOffsetX)/rCurvature); "
            + "y = yCurvatureCentre - (rCurvature + t - xMaterialGap - regionH - xElecH"
            + extra_layers_string
            + ")*cos((-regionW/2 + "
            + f"{vertical_line_index}"
            + f"*regionW/{self.pixel_columns_per_row[segment_index]}"
            + " + regionOffsetX)/rCurvature) + regionOffsetY; label = labelRegion;};\n"
        )

    def _draw_horizontal_edge(
        self,
        horizontal_line_index: int,
        segment_index: int,
        extra_layers_string: str,
    ) -> None:
        """Draws the segments of the horizontal lines of the pixels"""
        self.fflines_pixel_segments.append(
            f"border RegionMiddleH{horizontal_line_index}s{segment_index}"
            + f"(t=-regionW/2 + {segment_index+1}*"
            + f"regionW/{self.pixel_columns_horizontal_segments[horizontal_line_index]},"
            + f"-regionW/2 + {segment_index}*"
            + f"regionW/{self.pixel_columns_horizontal_segments[horizontal_line_index]})"
            + "{x = (rCurvature + "
            + f"{horizontal_line_index}*regionH/{self.num_pixel_geometry_rows}"
            + " - xMaterialGap - regionH - xElecH"
            + extra_layers_string
            + ")*sin((t + regionOffsetX)/rCurvature); "
            + "y = yCurvatureCentre - (rCurvature + "
            + f"{horizontal_line_index}*regionH/{self.num_pixel_geometry_rows}"
            + " - xMaterialGap - regionH - xElecH"
            + extra_layers_string
            + ")*cos((t + regionOffsetX)/rCurvature) "
            + "+ regionOffsetY; label = labelRegion;};\n"
        )

    def make_pixel_header(self) -> None:
        """
        Add FreeFem header code for "includes" and initialisations.
        """
        self.fflines_header.append(f"real regionW = {self.region_width};\n")
        self.fflines_header.append(f"real regionH = {self.region_height};\n")
        self.fflines_header.append(f"int labelRegion = {self.region_label};\n")
        self.fflines_header.append("\n" * 2)

    def make_pixel_segments(self) -> None:
        """
        Add FreeFem code to define the segments and borders defining pixelated region.
        When radius of curvature is high, the region just a rectangular block.
        """
        if self.num_pixel_geometry_columns != self.pixel_columns_per_row[-1]:
            raise ValueError(
                "The parameters num_pixel_geometry_columns and pixel_columns_per_row "
                + "are not consistent."
                + "The value of num_pixel_geometry_columns "
                + f"{self.num_pixel_geometry_columns} "
                + "should match with "
                + "the value of the number of columns in the lowest row "
                + f"{self.pixel_columns_per_row[-1]}."
            )
        if len(self.pixel_columns_per_row) != self.num_pixel_geometry_rows:
            raise ValueError(
                f"The length of pixel_columns_per_row {len(self.pixel_columns_per_row)} "
                + "should be equal to num_pixel_geometry_rows "
                + f"{self.num_pixel_geometry_rows}"
            )

        if self.extra_layers:
            extra_layers_string = str(-sum(self.extra_layers))
        else:
            extra_layers_string = ""

        for segment_index in range(self.num_pixel_geometry_rows):
            for vertical_line_index in range(
                self.pixel_columns_per_row[segment_index] + 1
            ):
                self._draw_vertical_edge(
                    vertical_line_index,
                    segment_index,
                    extra_layers_string,
                )

        for horizontal_line_index in range(self.num_pixel_geometry_rows + 1):
            for segment_index in range(
                self.pixel_columns_horizontal_segments[horizontal_line_index]
            ):
                self._draw_horizontal_edge(
                    horizontal_line_index,
                    segment_index,
                    extra_layers_string,
                )

        self.fflines_pixel_segments.append("\n" * 2)

    def make_pixel_function(self) -> None:
        """
        Add FreeFem code to define the pixelated region as a function
        to be used in the mesh generation.
        """

        self.fflines_pixel_function.append("func pixelRegion = \n")
        for segment_index in range(self.num_pixel_geometry_rows):
            for vertical_line_index in range(
                self.pixel_columns_per_row[segment_index] + 1
            ):
                add = "" if vertical_line_index == segment_index == 0 else "+"
                self.fflines_pixel_function.append(
                    f"{add}RegionMiddleV{vertical_line_index}s{segment_index}"
                    + f"(ceil(regionH*rMaterialStandard/({self.num_pixel_geometry_rows}*h)))\n"
                )

        for horizontal_line_index in range(self.num_pixel_geometry_rows + 1):
            for segment_index in range(
                self.pixel_columns_horizontal_segments[horizontal_line_index]
            ):
                if horizontal_line_index == self.num_pixel_geometry_rows:
                    self.fflines_pixel_function.append(
                        f"+RegionMiddleH{horizontal_line_index}s{segment_index}("
                        + f"ceil(regionW*rMaterialBottom/({self.num_pixel_geometry_columns}*h))"
                        + ")\n"
                    )
                else:
                    self.fflines_pixel_function.append(
                        f"+RegionMiddleH{horizontal_line_index}s{segment_index}("
                        + f"ceil(regionW*rMaterialStandard/({self.num_pixel_geometry_columns}*h))"
                        + ")\n"
                    )

        self.fflines_pixel_function.append(";\n")
        self.fflines_pixel_function.append("\n" * 2)

        # Plot region
        self.fflines_pixel_function.append(
            'if(BPlot){plot(pixelRegion, wait=false, cmm="Pixel Geometry");}\n'
        )
        self.fflines_pixel_function.append("\n" * 2)

    def make_pixel_centres(self) -> None:
        """
        Define the center of each pixel, this will be used to assign properties to
        individual regions of the geometry.
        """
        if self.extra_layers:
            extra_layers_string = str(-sum(self.extra_layers))
        else:
            extra_layers_string = ""

        self.fflines_pixel_centres.append(
            "// store the centers of each pixel\n"
        )
        self.fflines_pixel_centres.append(
            f"real[int] pixelCenterX({self.num_total_pixels});\n"
        )
        self.fflines_pixel_centres.append(
            f"real[int] pixelCenterY({self.num_total_pixels});\n"
        )

        self.fflines_pixel_centres.append(
            f"int numPixelRows = {self.num_pixel_geometry_rows};\n"
        )
        self.fflines_pixel_centres.append(
            "int[int] numPixelColumnsPerRow = ["
            + ", ".join(
                [
                    f"{self.pixel_columns_per_row[iloop]}"
                    for iloop in range(self.num_pixel_geometry_rows)
                ]
            )
            + "];\n"
        )

        self.fflines_pixel_centres.append("int loopCount = 0;\n")
        self.fflines_pixel_centres.append(
            "for (int i = 0; i < numPixelRows; i++)"
        )
        self.fflines_pixel_centres.append("{\n")
        self.fflines_pixel_centres.append(
            "\tfor (int j = 0; j < numPixelColumnsPerRow[i]; j++)"
        )
        self.fflines_pixel_centres.append("  {\n")
        self.fflines_pixel_centres.append(
            "\t\tpixelCenterX[loopCount] = (rCurvature "
            + "+ (i+0.5)*regionH/numPixelRows - xMaterialGap - regionH - xElecH"
            + extra_layers_string
            + ")*sin((-regionW/2 + (j+0.5)*regionW/numPixelColumnsPerRow[i] + "
            + "regionOffsetX)/rCurvature);\n"
        )
        self.fflines_pixel_centres.append(
            "\t\tpixelCenterY[loopCount] = yCurvatureCentre - (rCurvature + "
            + "(i+0.5)*regionH/numPixelRows - xMaterialGap - regionH - xElecH"
            + extra_layers_string
            + ")*cos((-regionW/2 + (j+0.5)*regionW/numPixelColumnsPerRow[i] + "
            + "regionOffsetX)/rCurvature) + regionOffsetY;\n"
        )
        self.fflines_pixel_centres.append("\t\tloopCount++;\n")

        self.fflines_pixel_centres.append("\t}\n")
        self.fflines_pixel_centres.append("}\n")


class PixelationCurvedRectangle(Pixelation):
    """
    A class to create a pixelated region with a curved rectangular shape for FreeFem simulations.
    Attributes:
        create_standalone (bool): Indicates if the pixelation is standalone.
        region_label (int): Label for the region.
        region_width (float): Width of the region.
        region_height (float): Height of the region.
        extra_layers (Optional[list]): Additional layers to be considered in the pixelation.
        fflines_header (list): List to store FreeFem header lines.
        fflines_pixel_segments (list): List to store FreeFem pixel segment lines.
        fflines_pixel_function (list): List to store FreeFem pixel function lines.
        fflines_pixel_centres (list): List to store FreeFem pixel center lines.
        num_pixel_columns (int): Number of pixel columns.
        num_pixel_rows (int): Number of pixel rows.
        num_total_pixels (int): Total number of pixels.
    Methods:
        __init__(params_pixels: Pixels, extra_layers: Optional[list] = None, subdir: str = "./"):
            Initializes the PixelationCurvedRectangle with given parameters.
        make_pixel_header() -> None:
            Adds FreeFem header code for "includes" and initializations.
        make_pixel_segments() -> None:
            Adds FreeFem code to define the segments and borders defining the pixelated region.
        make_pixel_function() -> None:
            Adds FreeFem code to define the pixelated region as a function for mesh generation.
        make_pixel_centres() -> None:
            Defines the center of each pixel for assigning properties to individual regions of the geometry.
    """

    def __init__(
        self,
        *,
        params_pixels: Pixels,
        extra_layers: Optional[list] = None,
        subdir: str = "./",
    ) -> None:
        self.create_standalone = params_pixels.create_standalone
        self.region_label = params_pixels.region_label
        self.region_width = params_pixels.region_width
        self.region_height = params_pixels.region_height
        self.extra_layers = extra_layers
        super().__init__(
            params_pixels=params_pixels,
            subdir=subdir,
        )

    def make_pixel_header(self) -> None:
        """
        Add FreeFem header code for "includes" and initialisations.
        """
        self.fflines_header.append(f"real regionW = {self.region_width};\n")
        self.fflines_header.append(f"real regionH = {self.region_height};\n")
        self.fflines_header.append(f"int labelRegion = {self.region_label};\n")
        self.fflines_header.append("\n" * 2)

    def make_pixel_segments(self) -> None:
        """
        Add FreeFem code to define the segments and borders defining pixelated region.
        When radius of curvature is high, the region just a rectangular block.
        """
        if self.extra_layers:
            extra_layers_string = str(-sum(self.extra_layers))
        else:
            extra_layers_string = ""
        # Define the vertical and horizontal splits of the pixelated region
        # Each column edge is split up into segments to
        # avoid crossing the row edges and vice versa
        for edge_col in range(self.num_pixel_columns + 1):
            for edge_row in range(self.num_pixel_rows):
                self.fflines_pixel_segments.append(
                    f"border RegionMiddleV{edge_col}s{edge_row}"
                    + f"(t={edge_row+1}*regionH/{self.num_pixel_rows}, "
                    + f"{edge_row}*regionH/{self.num_pixel_rows})"
                    + "{x = (rCurvature + t - xMaterialGap - regionH - xElecH"
                    + extra_layers_string
                    + ")*sin((-regionW/2 + "
                    + f"{edge_col}*regionW/{self.num_pixel_columns}"
                    + " + regionOffsetX)/rCurvature); y = yCurvatureCentre - "
                    + "(rCurvature + t - xMaterialGap - regionH - xElecH"
                    + extra_layers_string
                    + ")*cos((-regionW/2 + "
                    + f"{edge_col}*regionW/{self.num_pixel_columns}"
                    + " + regionOffsetX)/rCurvature) + regionOffsetY; "
                    + "label = labelRegion;};\n"
                )

        for edge_row in range(self.num_pixel_rows + 1):
            for edge_col in range(self.num_pixel_columns):
                self.fflines_pixel_segments.append(
                    f"border RegionMiddleH{edge_row}s{edge_col}"
                    + f"(t=-regionW/2 + {edge_col+1}*regionW/{self.num_pixel_columns}, "
                    + f"-regionW/2 + {edge_col}*regionW/{self.num_pixel_columns})"
                    + "{x = (rCurvature + "
                    + f"{edge_row}*regionH/{self.num_pixel_rows}"
                    + " - xMaterialGap - regionH - xElecH"
                    + extra_layers_string
                    + ")*sin((t + regionOffsetX)/rCurvature); "
                    + "y = yCurvatureCentre - (rCurvature + "
                    + f"{edge_row}*regionH/{self.num_pixel_rows}"
                    + " - xMaterialGap - regionH - xElecH"
                    + extra_layers_string
                    + ")*cos((t + regionOffsetX)/rCurvature) + "
                    + "regionOffsetY; label = labelRegion;};\n"
                )

        self.fflines_pixel_segments.append("\n" * 2)

    def make_pixel_function(self) -> None:
        """
        Add FreeFem code to define the pixelated region as a function
        to be used in the mesh generation.
        """

        self.fflines_pixel_function.append("func pixelRegion = \n")

        for edge_row in range(self.num_pixel_columns + 1):
            for edge_col in range(self.num_pixel_rows):
                add = "" if edge_row == edge_col == 0 else "+"
                self.fflines_pixel_function.append(
                    f"{add}RegionMiddleV{edge_row}s{edge_col}"
                    + f"(ceil(regionH*rMaterialStandard/({self.num_pixel_rows}*h)))\n"
                )

        for edge_row in range(self.num_pixel_rows + 1):
            for edge_col in range(self.num_pixel_columns):
                if edge_row == self.num_pixel_rows:
                    self.fflines_pixel_function.append(
                        f"+RegionMiddleH{edge_row}s{edge_col}("
                        + f"ceil(regionW*rMaterialBottom/({self.num_pixel_columns}*h))"
                        + ")\n"
                    )
                else:
                    self.fflines_pixel_function.append(
                        f"+RegionMiddleH{edge_row}s{edge_col}("
                        + f"ceil(regionW*rMaterialStandard/({self.num_pixel_columns}*h))"
                        + ")\n"
                    )  # xMaterialW*rMaterialBottom

        self.fflines_pixel_function.append(";\n")
        self.fflines_pixel_function.append("\n" * 2)

        # Plot region
        self.fflines_pixel_function.append(
            'if(BPlot){plot(pixelRegion, wait=false, cmm="Pixel Geometry");}\n'
        )
        self.fflines_pixel_function.append("\n" * 2)

    def make_pixel_centres(self) -> None:
        """
        Define the center of each pixel, this will be used to assign properties to
        individual regions of the geometry.
        """

        if self.extra_layers:
            extra_layers_string = str(-sum(self.extra_layers))
        else:
            extra_layers_string = ""

        self.fflines_pixel_centres.append(
            "// store the centers of each pixel\n"
        )
        self.fflines_pixel_centres.append(
            f"real[int] pixelCenterX({self.num_total_pixels});\n"
        )
        self.fflines_pixel_centres.append(
            f"real[int] pixelCenterY({self.num_total_pixels});\n"
        )

        self.fflines_pixel_centres.append(
            f"for (int i = 0; i < {self.num_pixel_columns}; i++)" "{\n"
        )
        self.fflines_pixel_centres.append(
            f"\tfor (int j = 0; j < {self.num_pixel_rows}; j++)" "{\n"
        )
        self.fflines_pixel_centres.append(
            f"\t\tpixelCenterX[i+{self.num_pixel_columns}*j] = (rCurvature + "
            + f"(j+0.5)*regionH/{self.num_pixel_rows} - xMaterialGap - regionH - xElecH"
            + extra_layers_string
            + ")*sin((-regionW/2 + "
            + f"(i+0.5)*regionW/{self.num_pixel_columns} + regionOffsetX)/rCurvature);\n"
        )
        self.fflines_pixel_centres.append(
            f"\t\tpixelCenterY[i+{self.num_pixel_columns}*j] = yCurvatureCentre - (rCurvature "
            + f"+ (j+0.5)*regionH/{self.num_pixel_rows} - xMaterialGap - regionH - xElecH"
            + extra_layers_string
            + f")*cos((-regionW/2 + (i+0.5)*regionW/{self.num_pixel_columns} "
            + "+ regionOffsetX)/rCurvature) + regionOffsetY;\n"
        )

        self.fflines_pixel_centres.append("\t}\n")
        self.fflines_pixel_centres.append("}\n")


class PixelationCircularPhantom(Pixelation):
    """
    A class to handle the pixelation of a circular phantom with optional bores.
    This class extends the Pixelation class and provides methods to generate
    FreeFem code for defining the pixelated region of a circular phantom. The
    phantom can have an outer and inner radius, and can contain multiple circular
    bores.
    Attributes:
        create_standalone (bool): Flag indicating if the pixelation is standalone.
        region_label (int): Label for the region.
        circular_phantom_outer_radius (float): Outer radius of the circular phantom.
        circular_phantom_inner_radius (float or None): Inner radius of the circular phantom.
        circular_phantom_bore_radii (list of float or None): Radii of the bores in the phantom.
        num_background_pixels (int): Number of background pixels.
        circular_phantom_bore_centre_distance (float): Distance between the centers of the bores.
        circular_phantom_angle (float): Angle of the phantom.
        circular_phantom_num_bores (int): Number of bores in the phantom.
    Methods:
        make_pixel_header(): Adds FreeFem header code for "includes" and initializations.
        make_pixel_segments(): Adds FreeFem code to define the segments and borders defining the pixelated region.
        make_pixel_function(): Adds FreeFem code to define the pixelated region as a function for mesh generation.
        make_pixel_centres(): Defines the center of each pixel for assigning properties to individual regions.
    """

    def __init__(
        self,
        *,
        params_pixels: Pixels,
        subdir: str = "./",
    ) -> None:
        self.create_standalone = params_pixels.create_standalone
        self.region_label = params_pixels.region_label
        self.circular_phantom_outer_radius = (
            params_pixels.circular_phantom_radius
        )
        self.circular_phantom_inner_radius = (
            (
                params_pixels.circular_phantom_radius
                - params_pixels.circular_phantom_thickness
            )
            if params_pixels.circular_phantom_thickness is not None
            else None
        )
        self.circular_phantom_bore_radii = (
            params_pixels.circular_phantom_bore_radii
        )
        self.num_background_pixels = (
            2 if self.circular_phantom_inner_radius is not None else 1
        )
        self.circular_phantom_bore_centre_distance = (
            params_pixels.circular_phantom_bore_centre_distance
        )
        self.circular_phantom_angle = params_pixels.circular_phantom_angle
        self.circular_phantom_num_bores = (
            len(params_pixels.circular_phantom_bore_radii)
            if params_pixels.circular_phantom_bore_radii is not None
            else 0
        )
        if (
            params_pixels.num_pixel_rows != 1
            or params_pixels.num_pixel_columns
            != self.circular_phantom_num_bores + self.num_background_pixels
        ):
            raise ValueError(
                "num_pixel_rows and num_pixel_columns are "
                + "not consistent for circular phantom"
            )
        super().__init__(
            params_pixels=params_pixels,
            subdir=subdir,
        )

    def make_pixel_header(self) -> None:
        """
        Add FreeFem header code for "includes" and initialisations.
        """
        self.fflines_header.append(f"int labelRegion = {self.region_label};\n")
        self.fflines_header.append("\n" * 2)

        self.fflines_header.append("// Phantom parameters\n")
        self.fflines_header.append(
            f"int numBores = {self.circular_phantom_num_bores};\n"
        )
        self.fflines_header.append(
            f"real radiusOuterPhantom = {self.circular_phantom_outer_radius};\n"
        )
        if self.circular_phantom_inner_radius is not None:
            self.fflines_header.append(
                f"real radiusInnerPhantom = {self.circular_phantom_inner_radius};\n"
            )
        if self.circular_phantom_bore_radii is not None:
            self.fflines_header.append(
                f"real distanceBoreCentres = {self.circular_phantom_bore_centre_distance};\n"
            )
            self.fflines_header.append(
                f"real anglePhantom = -pi/2 + {self.circular_phantom_angle};\n"
            )
            for iloop_bores in range(len(self.circular_phantom_bore_radii)):
                self.fflines_header.append(
                    f"real radiusBore{iloop_bores+1} = "
                    + f"{self.circular_phantom_bore_radii[iloop_bores]};\n"
                )
        self.fflines_header.append("real xCentrePhantom = regionOffsetX;\n")
        self.fflines_header.append(
            "real yCentrePhantom = regionOffsetY + yCurvatureCentre - rCurvature"
            + " + xMaterialGap + radiusOuterPhantom;\n"
        )
        self.fflines_header.append("\n" * 2)

    def make_pixel_segments(self) -> None:
        """
        Add FreeFem code to define the segments and borders defining pixelated region.
        This defines the pixelated region for 2D phantom of circular cross-section.
        The cross section can contain many circular bores.
        """
        if self.circular_phantom_bore_radii is not None:
            self.fflines_pixel_segments.append("//The  centre of bores\n")
            self.fflines_pixel_segments.append(
                "real[int] xCentreBores(numBores);\n"
            )
            self.fflines_pixel_segments.append(
                "real[int] yCentreBores(numBores);\n"
            )

            self.fflines_pixel_segments.append(
                "for (int iloopBores=0; iloopBores<numBores; iloopBores++)\n{\n"
            )
            self.fflines_pixel_segments.append(
                "    xCentreBores[iloopBores] = xCentrePhantom + "
                + "distanceBoreCentres*cos(iloopBores*2*pi/numBores + anglePhantom);\n"
            )
            self.fflines_pixel_segments.append(
                "    yCentreBores[iloopBores] = yCentrePhantom + "
                + "distanceBoreCentres*sin(iloopBores*2*pi/numBores + anglePhantom);\n"
            )
            self.fflines_pixel_segments.append("}\n")

        self.fflines_pixel_segments.append("\n" * 2)
        self.fflines_pixel_segments.append(
            "border phantomBackgroundBottom(t=-5*pi/6, -pi/6){"
            + "x = xCentrePhantom + radiusOuterPhantom*cos(t);"
            + "y = yCentrePhantom + radiusOuterPhantom*sin(t);"
            + "label = labelRegion;"
            + "};\n"
        )

        self.fflines_pixel_segments.append(
            "border phantomBackgroundTop(t=-pi/6, 7*pi/6){"
            + "x = xCentrePhantom + radiusOuterPhantom*cos(t);"
            + "y = yCentrePhantom + radiusOuterPhantom*sin(t);"
            + "label = labelRegion;"
            + "};\n"
        )
        if self.circular_phantom_inner_radius is not None:
            self.fflines_pixel_segments.append(
                "border phantomBackgroundInner(t=0, 2*pi){"
                + "x = xCentrePhantom + radiusInnerPhantom*cos(t);"
                + "y = yCentrePhantom + radiusInnerPhantom*sin(t);"
                + "label = labelRegion;"
                + "};\n"
            )

        if self.circular_phantom_bore_radii is not None:
            for iloop_bores in range(len(self.circular_phantom_bore_radii)):
                self.fflines_pixel_segments.append(
                    f"border phantomBore{iloop_bores+1}(t=0, 2*pi)"
                    + "{"
                    + f"x = xCentreBores[{iloop_bores}]+radiusBore{iloop_bores+1}*cos(t);"
                    + f"y = yCentreBores[{iloop_bores}]+radiusBore{iloop_bores+1}*sin(t);"
                    + "label = labelRegion;};\n"
                )

        self.fflines_pixel_segments.append("\n" * 2)

    def make_pixel_function(self) -> None:
        """
        Add FreeFem code to define the pixelated region as a function
        to be used in the mesh generation.
        """

        self.fflines_pixel_function.append("func pixelRegion = \n")
        self.fflines_pixel_function.append(
            "phantomBackgroundBottom(ceil(rMaterialBottom*2*pi*radiusOuterPhantom/h))\n"
        )
        self.fflines_pixel_function.append(
            "+phantomBackgroundTop(ceil(rMaterialStandard*2*pi*radiusOuterPhantom/h))\n"
        )
        if self.circular_phantom_inner_radius is not None:
            self.fflines_pixel_function.append(
                "+phantomBackgroundInner(ceil(rMaterialStandard*2*pi*radiusInnerPhantom/h))\n"
            )

        if self.circular_phantom_bore_radii is not None:
            for iloop_bores in range(len(self.circular_phantom_bore_radii)):
                self.fflines_pixel_function.append(
                    f"+phantomBore{iloop_bores+1}("
                    + f"ceil(rMaterialStandard*2*pi*radiusBore{iloop_bores+1}/h))\n"
                )
        self.fflines_pixel_function.append(";\n")

        self.fflines_pixel_function.append("\n" * 2)

        # Plot region
        self.fflines_pixel_function.append(
            'if(BPlot){plot(pixelRegion, wait=false, cmm="Pixel Geometry");}\n'
        )

        self.fflines_pixel_function.append("\n" * 2)

    def make_pixel_centres(self) -> None:
        """
        Define the center of each pixel, this will be used to assign properties
        to individual regions of the geometry.
        """
        self.fflines_pixel_centres.append(
            "// store the centers of each pixel\n"
        )
        self.fflines_pixel_centres.append(
            f"real[int] pixelCenterX(numBores+{self.num_background_pixels});\n"
        )
        self.fflines_pixel_centres.append(
            f"real[int] pixelCenterY(numBores+{self.num_background_pixels});\n"
        )
        self.fflines_pixel_centres.append(
            "pixelCenterX[0] = xCentrePhantom;\n"
        )
        self.fflines_pixel_centres.append(
            "pixelCenterY[0] = yCentrePhantom;\n"
        )

        if self.circular_phantom_inner_radius is not None:
            self.fflines_pixel_centres.append(
                "pixelCenterX[1] = xCentrePhantom;\n"
            )
            self.fflines_pixel_centres.append(
                "pixelCenterY[1] = yCentrePhantom - (radiusOuterPhantom+radiusInnerPhantom)/2;\n"
            )

        if self.circular_phantom_bore_radii is not None:
            self.fflines_pixel_centres.append(
                f"for (int iloopPixel={self.num_background_pixels}; iloopPixel<pixelCenterX.n; iloopPixel++)"
                + "{\n"
            )
            self.fflines_pixel_centres.append(
                "\tpixelCenterX[iloopPixel] = "
                + f"xCentreBores[iloopPixel-{self.num_background_pixels}];"
                + "\n"
            )
            self.fflines_pixel_centres.append(
                "\tpixelCenterY[iloopPixel] = "
                + f"yCentreBores[iloopPixel-{self.num_background_pixels}];"
                + "\n"
            )
            self.fflines_pixel_centres.append("}\n")


def create_pixelation(
    *,
    params_pixels: Pixels = None,
    subdir: str = "./",  # prefix to filenames
    extra_layers: Optional[list] = None,
) -> None:
    """
    Create a freefem file that defines the geometry and the mesh for the
    pixel region.

    Args:
        params_pixels: parameters to define the pixel
        subdir: directory in which the freefem file is created
        extra_layers: A list of additional layers between the electrodes and the
                      pixelated material.

    Returns:
             None

    Raises:
        NotImplementedError: if params_pixels.pixel_type is not valid
    """
    if params_pixels.pixel_type == "curved_rectangle":
        pixel_creator = PixelationCurvedRectangle(
            params_pixels=params_pixels,
            subdir=subdir,
            extra_layers=extra_layers,
        )

    elif params_pixels.pixel_type == "curved_rectangle_nonuniform":
        pixel_creator = PixelationCurvedRectangleNonuniform(
            params_pixels=params_pixels,
            subdir=subdir,
            extra_layers=extra_layers,
        )

    elif params_pixels.pixel_type == "circular_phantom":
        pixel_creator = PixelationCircularPhantom(
            params_pixels=params_pixels,
            subdir=subdir,
        )

    else:
        raise NotImplementedError(
            f"The type of pixelation {params_pixels.pixel_type} is not yet implemented"
        )

    pixel_creator.create_pixelation()


def permittivity_array_to_matrix(array, params):
    return np.reshape(
        array, (params.pixels.num_pixel_rows, params.pixels.num_pixel_columns)
    )
