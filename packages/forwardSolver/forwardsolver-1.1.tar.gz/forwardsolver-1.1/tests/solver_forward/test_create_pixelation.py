import copy
import os
import shutil
from dataclasses import asdict

import pytest

from forwardSolver.scripts.params.forward_solver_params import ForwardSolverParams
from forwardSolver.scripts.utils.constants import ERROR_STRINGS, FREEFEM_DIR
from forwardSolver.scripts.utils.copy_files_to_subdir import copy_files_to_subdir
from forwardSolver.scripts.utils.create_pixelation import (
    PixelationCircularPhantom,
    PixelationCurvedRectangle,
    PixelationCurvedRectangleNonuniform,
    create_pixelation,
)
from forwardSolver.scripts.utils.freefem import params_to_freefem_command
from forwardSolver.scripts.utils.hash import hash_dictionary
from forwardSolver.scripts.utils.pixels import Pixels

params_forward_9 = ForwardSolverParams.factory("P1000-009")


# Function required for testing
def run_freefem_geometry(params_forward: ForwardSolverParams) -> bool:
    """

    Function to run the freefem geometry file and check for error in mesh creation

    Args:
        params_forward: forward solver parameters

    Returns:
        If the freefem geometry file runs without error, success is set to True

    Raises:
        ArithmeticError: Raised if an error string is found in the freefem log
    """
    success = False
    solver_dir = "/model_solver/"
    solver_dir = FREEFEM_DIR + solver_dir
    solver_subdir = "test_run_" + hash_dictionary(asdict(params_forward)) + "/"
    log_path = solver_dir + solver_subdir + "freefem.log"

    os.makedirs(
        solver_dir + solver_subdir + "solver_artefacts" + "/pixels", exist_ok=True
    )
    copy_files_to_subdir(solver_dir, solver_dir + solver_subdir, "edp")

    create_pixelation(
        params_pixels=params_forward.pixels, subdir=solver_dir + solver_subdir
    )

    os_command = params_to_freefem_command(
        params_forward,
        solver_dir + solver_subdir,
        log_path,
    )

    cwd = os.getcwd()  # current working directory
    try:
        os.chdir(solver_dir + solver_subdir)  # enter subdir to use relevant files
        os.system(os_command)
    except Exception as err:
        print(f"Unable to change directory!\n{err}")
    finally:
        os.chdir(cwd)  # exit subdir to allow deletion of subdir

    with open(log_path, "r") as f:
        contents = f.read()
    if any(error_string in contents.lower() for error_string in ERROR_STRINGS):
        raise ArithmeticError(
            "Error found in FreeFem log file when attempting to"
            f" generate meshes and matrices: \n{contents})"
        )
    else:
        success = True
    if os.path.exists(solver_dir + solver_subdir):
        shutil.rmtree(solver_dir + solver_subdir)

    return success


# Fixtures related to non-uniform curved rectangle pixelation


@pytest.fixture(scope="module")
def params_pixels_curved_rectangle_nonuniform():
    return Pixels(
        create_standalone=False,
        region_width="xMaterialW",
        region_height="xMaterialH",
        region_label=300,
        num_pixel_rows=2,
        num_pixel_columns=2,
        pixel_columns_per_row=[1, 2],
        permittivity_matrix=[2, 3, 4],
        pixel_type="curved_rectangle_nonuniform",
    )


@pytest.fixture(scope="module")
def params_pixels_curved_rectangle_nonuniform_standalone():
    return Pixels(
        create_standalone=True,
        region_width="xMaterialW",
        region_height="xMaterialH",
        region_label=300,
        num_pixel_rows=2,
        num_pixel_columns=2,
        pixel_columns_per_row=[1, 2],
        permittivity_matrix=[2, 3, 4],
        pixel_type="curved_rectangle_nonuniform",
    )


@pytest.fixture
def curved_rectangle_nonuniform_object(params_pixels_curved_rectangle_nonuniform):
    return PixelationCurvedRectangleNonuniform(
        params_pixels=params_pixels_curved_rectangle_nonuniform
    )


@pytest.fixture
def curved_rectangle_nonuniform_object_standalone(
    params_pixels_curved_rectangle_nonuniform_standalone,
):
    return PixelationCurvedRectangleNonuniform(
        params_pixels=params_pixels_curved_rectangle_nonuniform_standalone
    )


@pytest.fixture
def expected_curved_rectangle_nonuniform_fflines_header(
    params_pixels_curved_rectangle_nonuniform,
):
    return (
        ""
        + "real regionW = xMaterialW;\n"
        + "real regionH = xMaterialH;\n"
        + "int labelRegion = 300;\n"
        + "\n"
        + "\n"
    )


@pytest.fixture
def expected_curved_rectangle_nonuniform_fflines_pixel_segments(
    params_pixels_curved_rectangle_nonuniform,
):
    return (
        "border RegionMiddleV0s0(t=1*regionH/2, 0*regionH/2){x = (rCurvature + t - xMaterialGap - regionH - xElecH)*sin((-regionW/2 + 0*regionW/1 + regionOffsetX)/rCurvature); y = yCurvatureCentre - (rCurvature + t - xMaterialGap - regionH - xElecH)*cos((-regionW/2 + 0*regionW/1 + regionOffsetX)/rCurvature) + regionOffsetY; label = labelRegion;};\n"
        + "border RegionMiddleV1s0(t=1*regionH/2, 0*regionH/2){x = (rCurvature + t - xMaterialGap - regionH - xElecH)*sin((-regionW/2 + 1*regionW/1 + regionOffsetX)/rCurvature); y = yCurvatureCentre - (rCurvature + t - xMaterialGap - regionH - xElecH)*cos((-regionW/2 + 1*regionW/1 + regionOffsetX)/rCurvature) + regionOffsetY; label = labelRegion;};\n"
        + "border RegionMiddleV0s1(t=2*regionH/2, 1*regionH/2){x = (rCurvature + t - xMaterialGap - regionH - xElecH)*sin((-regionW/2 + 0*regionW/2 + regionOffsetX)/rCurvature); y = yCurvatureCentre - (rCurvature + t - xMaterialGap - regionH - xElecH)*cos((-regionW/2 + 0*regionW/2 + regionOffsetX)/rCurvature) + regionOffsetY; label = labelRegion;};\n"
        + "border RegionMiddleV1s1(t=2*regionH/2, 1*regionH/2){x = (rCurvature + t - xMaterialGap - regionH - xElecH)*sin((-regionW/2 + 1*regionW/2 + regionOffsetX)/rCurvature); y = yCurvatureCentre - (rCurvature + t - xMaterialGap - regionH - xElecH)*cos((-regionW/2 + 1*regionW/2 + regionOffsetX)/rCurvature) + regionOffsetY; label = labelRegion;};\n"
        + "border RegionMiddleV2s1(t=2*regionH/2, 1*regionH/2){x = (rCurvature + t - xMaterialGap - regionH - xElecH)*sin((-regionW/2 + 2*regionW/2 + regionOffsetX)/rCurvature); y = yCurvatureCentre - (rCurvature + t - xMaterialGap - regionH - xElecH)*cos((-regionW/2 + 2*regionW/2 + regionOffsetX)/rCurvature) + regionOffsetY; label = labelRegion;};\n"
        + "border RegionMiddleH0s0(t=-regionW/2 + 1*regionW/1,-regionW/2 + 0*regionW/1){x = (rCurvature + 0*regionH/2 - xMaterialGap - regionH - xElecH)*sin((t + regionOffsetX)/rCurvature); y = yCurvatureCentre - (rCurvature + 0*regionH/2 - xMaterialGap - regionH - xElecH)*cos((t + regionOffsetX)/rCurvature) + regionOffsetY; label = labelRegion;};\n"
        + "border RegionMiddleH1s0(t=-regionW/2 + 1*regionW/2,-regionW/2 + 0*regionW/2){x = (rCurvature + 1*regionH/2 - xMaterialGap - regionH - xElecH)*sin((t + regionOffsetX)/rCurvature); y = yCurvatureCentre - (rCurvature + 1*regionH/2 - xMaterialGap - regionH - xElecH)*cos((t + regionOffsetX)/rCurvature) + regionOffsetY; label = labelRegion;};\n"
        + "border RegionMiddleH1s1(t=-regionW/2 + 2*regionW/2,-regionW/2 + 1*regionW/2){x = (rCurvature + 1*regionH/2 - xMaterialGap - regionH - xElecH)*sin((t + regionOffsetX)/rCurvature); y = yCurvatureCentre - (rCurvature + 1*regionH/2 - xMaterialGap - regionH - xElecH)*cos((t + regionOffsetX)/rCurvature) + regionOffsetY; label = labelRegion;};\n"
        + "border RegionMiddleH2s0(t=-regionW/2 + 1*regionW/2,-regionW/2 + 0*regionW/2){x = (rCurvature + 2*regionH/2 - xMaterialGap - regionH - xElecH)*sin((t + regionOffsetX)/rCurvature); y = yCurvatureCentre - (rCurvature + 2*regionH/2 - xMaterialGap - regionH - xElecH)*cos((t + regionOffsetX)/rCurvature) + regionOffsetY; label = labelRegion;};\n"
        + "border RegionMiddleH2s1(t=-regionW/2 + 2*regionW/2,-regionW/2 + 1*regionW/2){x = (rCurvature + 2*regionH/2 - xMaterialGap - regionH - xElecH)*sin((t + regionOffsetX)/rCurvature); y = yCurvatureCentre - (rCurvature + 2*regionH/2 - xMaterialGap - regionH - xElecH)*cos((t + regionOffsetX)/rCurvature) + regionOffsetY; label = labelRegion;};\n"
        + "\n"
        + "\n"
    )


@pytest.fixture
def expected_curved_rectangle_nonuniform_fflines_pixel_function():
    return (
        "func pixelRegion = \n"
        + "RegionMiddleV0s0(ceil(regionH*rMaterialStandard/(2*h)))\n"
        + "+RegionMiddleV1s0(ceil(regionH*rMaterialStandard/(2*h)))\n"
        + "+RegionMiddleV0s1(ceil(regionH*rMaterialStandard/(2*h)))\n"
        + "+RegionMiddleV1s1(ceil(regionH*rMaterialStandard/(2*h)))\n"
        + "+RegionMiddleV2s1(ceil(regionH*rMaterialStandard/(2*h)))\n"
        + "+RegionMiddleH0s0(ceil(regionW*rMaterialStandard/(2*h)))\n"
        + "+RegionMiddleH1s0(ceil(regionW*rMaterialStandard/(2*h)))\n"
        + "+RegionMiddleH1s1(ceil(regionW*rMaterialStandard/(2*h)))\n"
        + "+RegionMiddleH2s0(ceil(regionW*rMaterialBottom/(2*h)))\n"
        + "+RegionMiddleH2s1(ceil(regionW*rMaterialBottom/(2*h)))\n"
        + ";\n"
        + "\n"
        + "\n"
        + 'if(BPlot){plot(pixelRegion, wait=false, cmm="Pixel Geometry");}\n'
        + "\n"
        + "\n"
    )


@pytest.fixture
def expected_curved_rectangle_nonuniform_fflines_standalone_mesh():
    return (
        "// Macro to generate the mesh. (Can't have comments within macro environment)\n"
        + "macro createMesh(h)\n"
        + "mesh Th = buildmesh(\n"
        + "    pixelRegion\n"
        + ");\n"
        + "// End of macro\n"
        + "\n"
        + "\n"
        + "createMesh(h);\n"
        + "plot(Th);\n"
        + "\n"
        + "\n"
    )


@pytest.fixture
def expected_curved_rectangle_nonuniform_fflines_pixel_centres():
    return (
        "// store the centers of each pixel\n"
        + "real[int] pixelCenterX(3);\n"
        + "real[int] pixelCenterY(3);\n"
        + "int numPixelRows = 2;\n"
        + "int[int] numPixelColumnsPerRow = [1, 2];\n"
        + "int loopCount = 0;\n"
        + "for (int i = 0; i < numPixelRows; i++){\n"
        + "\tfor (int j = 0; j < numPixelColumnsPerRow[i]; j++)  {\n"
        + "\t\tpixelCenterX[loopCount] = (rCurvature + (i+0.5)*regionH/numPixelRows - xMaterialGap - regionH - xElecH)*sin((-regionW/2 + (j+0.5)*regionW/numPixelColumnsPerRow[i] + regionOffsetX)/rCurvature);\n"
        + "\t\tpixelCenterY[loopCount] = yCurvatureCentre - (rCurvature + (i+0.5)*regionH/numPixelRows - xMaterialGap - regionH - xElecH)*cos((-regionW/2 + (j+0.5)*regionW/numPixelColumnsPerRow[i] + regionOffsetX)/rCurvature) + regionOffsetY;\n"
        + "\t\tloopCount++;\n"
        + "\t}\n"
        + "}\n"
    )


# Fixtures related to curved rectangle pixelation


@pytest.fixture(scope="module")
def params_pixels_curved_rectangle():
    return Pixels(
        create_standalone=False,
        region_width="xMaterialW",
        region_height="xMaterialH",
        region_label=300,
        num_pixel_rows=1,
        num_pixel_columns=2,
        permittivity_matrix=None,
        pixel_type="curved_rectangle",
    )


@pytest.fixture(scope="module")
def params_pixels_curved_rectangle_standalone():
    return Pixels(
        create_standalone=True,
        region_width="xMaterialW",
        region_height="xMaterialH",
        region_label=300,
        num_pixel_rows=1,
        num_pixel_columns=2,
        permittivity_matrix=None,
        pixel_type="curved_rectangle",
    )


@pytest.fixture
def curved_rectangle_object(params_pixels_curved_rectangle):
    return PixelationCurvedRectangle(params_pixels=params_pixels_curved_rectangle)


@pytest.fixture
def curved_rectangle_object_standalone(params_pixels_curved_rectangle_standalone):
    return PixelationCurvedRectangle(
        params_pixels=params_pixels_curved_rectangle_standalone
    )


@pytest.fixture
def expected_curved_rectangle_fflines_header(params_pixels_curved_rectangle):
    return (
        ""
        + "real regionW = xMaterialW;\n"
        + "real regionH = xMaterialH;\n"
        + "int labelRegion = 300;\n"
        + "\n"
        + "\n"
    )


@pytest.fixture
def expected_curved_rectangle_fflines_pixel_segments(params_pixels_curved_rectangle):
    return (
        "border RegionMiddleV0s0(t=1*regionH/1, 0*regionH/1){x = (rCurvature + t - xMaterialGap - regionH - xElecH)*sin((-regionW/2 + 0*regionW/2 + regionOffsetX)/rCurvature); y = yCurvatureCentre - (rCurvature + t - xMaterialGap - regionH - xElecH)*cos((-regionW/2 + 0*regionW/2 + regionOffsetX)/rCurvature) + regionOffsetY; label = labelRegion;};\n"
        + "border RegionMiddleV1s0(t=1*regionH/1, 0*regionH/1){x = (rCurvature + t - xMaterialGap - regionH - xElecH)*sin((-regionW/2 + 1*regionW/2 + regionOffsetX)/rCurvature); y = yCurvatureCentre - (rCurvature + t - xMaterialGap - regionH - xElecH)*cos((-regionW/2 + 1*regionW/2 + regionOffsetX)/rCurvature) + regionOffsetY; label = labelRegion;};\n"
        + "border RegionMiddleV2s0(t=1*regionH/1, 0*regionH/1){x = (rCurvature + t - xMaterialGap - regionH - xElecH)*sin((-regionW/2 + 2*regionW/2 + regionOffsetX)/rCurvature); y = yCurvatureCentre - (rCurvature + t - xMaterialGap - regionH - xElecH)*cos((-regionW/2 + 2*regionW/2 + regionOffsetX)/rCurvature) + regionOffsetY; label = labelRegion;};\n"
        + "border RegionMiddleH0s0(t=-regionW/2 + 1*regionW/2, -regionW/2 + 0*regionW/2){x = (rCurvature + 0*regionH/1 - xMaterialGap - regionH - xElecH)*sin((t + regionOffsetX)/rCurvature); y = yCurvatureCentre - (rCurvature + 0*regionH/1 - xMaterialGap - regionH - xElecH)*cos((t + regionOffsetX)/rCurvature) + regionOffsetY; label = labelRegion;};\n"
        + "border RegionMiddleH0s1(t=-regionW/2 + 2*regionW/2, -regionW/2 + 1*regionW/2){x = (rCurvature + 0*regionH/1 - xMaterialGap - regionH - xElecH)*sin((t + regionOffsetX)/rCurvature); y = yCurvatureCentre - (rCurvature + 0*regionH/1 - xMaterialGap - regionH - xElecH)*cos((t + regionOffsetX)/rCurvature) + regionOffsetY; label = labelRegion;};\n"
        + "border RegionMiddleH1s0(t=-regionW/2 + 1*regionW/2, -regionW/2 + 0*regionW/2){x = (rCurvature + 1*regionH/1 - xMaterialGap - regionH - xElecH)*sin((t + regionOffsetX)/rCurvature); y = yCurvatureCentre - (rCurvature + 1*regionH/1 - xMaterialGap - regionH - xElecH)*cos((t + regionOffsetX)/rCurvature) + regionOffsetY; label = labelRegion;};\n"
        + "border RegionMiddleH1s1(t=-regionW/2 + 2*regionW/2, -regionW/2 + 1*regionW/2){x = (rCurvature + 1*regionH/1 - xMaterialGap - regionH - xElecH)*sin((t + regionOffsetX)/rCurvature); y = yCurvatureCentre - (rCurvature + 1*regionH/1 - xMaterialGap - regionH - xElecH)*cos((t + regionOffsetX)/rCurvature) + regionOffsetY; label = labelRegion;};\n"
        + "\n"
        + "\n"
    )


@pytest.fixture
def expected_curved_rectangle_fflines_pixel_function():
    return (
        "func pixelRegion = \n"
        + "RegionMiddleV0s0(ceil(regionH*rMaterialStandard/(1*h)))\n"
        + "+RegionMiddleV1s0(ceil(regionH*rMaterialStandard/(1*h)))\n"
        + "+RegionMiddleV2s0(ceil(regionH*rMaterialStandard/(1*h)))\n"
        + "+RegionMiddleH0s0(ceil(regionW*rMaterialStandard/(2*h)))\n"
        + "+RegionMiddleH0s1(ceil(regionW*rMaterialStandard/(2*h)))\n"
        + "+RegionMiddleH1s0(ceil(regionW*rMaterialBottom/(2*h)))\n"
        + "+RegionMiddleH1s1(ceil(regionW*rMaterialBottom/(2*h)))\n"
        + ";\n"
        + "\n"
        + "\n"
        + 'if(BPlot){plot(pixelRegion, wait=false, cmm="Pixel Geometry");}\n'
        + "\n"
        + "\n"
    )


@pytest.fixture
def expected_curved_rectangle_fflines_standalone_mesh():
    return (
        "// Macro to generate the mesh. (Can't have comments within macro environment)\n"
        + "macro createMesh(h)\n"
        + "mesh Th = buildmesh(\n"
        + "    pixelRegion\n"
        + ");\n"
        + "// End of macro\n"
        + "\n"
        + "\n"
        + "createMesh(h);\n"
        + "plot(Th);\n"
        + "\n"
        + "\n"
    )


@pytest.fixture
def expected_curved_rectangle_fflines_pixel_centres():
    return (
        "// store the centers of each pixel\n"
        + "real[int] pixelCenterX(2);\n"
        + "real[int] pixelCenterY(2);\n"
        + "for (int i = 0; i < 2; i++){\n"
        + "\tfor (int j = 0; j < 1; j++){\n"
        + "\t\tpixelCenterX[i+2*j] = (rCurvature + (j+0.5)*regionH/1 - xMaterialGap - regionH - xElecH)*sin((-regionW/2 + (i+0.5)*regionW/2 + regionOffsetX)/rCurvature);\n"
        + "\t\tpixelCenterY[i+2*j] = yCurvatureCentre - (rCurvature + (j+0.5)*regionH/1 - xMaterialGap - regionH - xElecH)*cos((-regionW/2 + (i+0.5)*regionW/2 + regionOffsetX)/rCurvature) + regionOffsetY;\n"
        + "\t}\n"
        + "}\n"
    )


# Fixtures related to circular phantom pixels


@pytest.fixture(scope="module")
def params_pixels_circular_phantom():
    return Pixels(
        create_standalone=False,
        region_label=300,
        num_pixel_rows=1,
        num_pixel_columns=2,
        permittivity_matrix=None,
        pixel_type="circular_phantom",
        circular_phantom_radius=71.0,
        circular_phantom_bore_radii=[20.0],
        circular_phantom_bore_centre_distance=41.0,
        circular_phantom_angle=0.0,
    )


@pytest.fixture(scope="module")
def params_pixels_circular_phantom_standalone():
    return Pixels(
        create_standalone=True,
        region_label=300,
        num_pixel_rows=1,
        num_pixel_columns=2,
        permittivity_matrix=None,
        pixel_type="circular_phantom",
        circular_phantom_radius=71.0,
        circular_phantom_bore_radii=[20.0],
        circular_phantom_bore_centre_distance=41.0,
        circular_phantom_angle=0.0,
    )


@pytest.fixture
def circular_phantom_object(params_pixels_circular_phantom):
    return PixelationCircularPhantom(params_pixels=params_pixels_circular_phantom)


@pytest.fixture
def expected_circular_phantom_fflines_header(params_pixels_circular_phantom):
    return (
        "" + "int labelRegion = 300;\n" + "\n" + "\n"
        "// Phantom parameters\n"
        + f"int numBores = {len(params_pixels_circular_phantom.circular_phantom_bore_radii)};\n"
        + f"real radiusOuterPhantom = {params_pixels_circular_phantom.circular_phantom_radius};\n"
        + f"real distanceBoreCentres = {params_pixels_circular_phantom.circular_phantom_bore_centre_distance};\n"
        + f"real anglePhantom = -pi/2 + {params_pixels_circular_phantom.circular_phantom_angle};\n"
        + f"real radiusBore1 = {params_pixels_circular_phantom.circular_phantom_bore_radii[0]};\n"
        + "real xCentrePhantom = regionOffsetX;\n"
        + "real yCentrePhantom = regionOffsetY + yCurvatureCentre - rCurvature + xMaterialGap + radiusOuterPhantom;\n"
        + "\n"
        + "\n"
    )


@pytest.fixture
def expected_circular_phantom_fflines_pixel_segments():
    return (
        "//The  centre of bores\n"
        + "real[int] xCentreBores(numBores);\n"
        + "real[int] yCentreBores(numBores);\n"
        + "for (int iloopBores=0; iloopBores<numBores; iloopBores++)\n"
        + "{\n"
        + "    xCentreBores[iloopBores] = xCentrePhantom + distanceBoreCentres*cos(iloopBores*2*pi/numBores + anglePhantom);\n"
        + "    yCentreBores[iloopBores] = yCentrePhantom + distanceBoreCentres*sin(iloopBores*2*pi/numBores + anglePhantom);\n"
        + "}\n"
        + "\n"
        + "\n"
        + "border phantomBackgroundBottom(t=-5*pi/6, -pi/6){x = xCentrePhantom + radiusOuterPhantom*cos(t);y = yCentrePhantom + radiusOuterPhantom*sin(t);label = labelRegion;};\n"
        + "border phantomBackgroundTop(t=-pi/6, 7*pi/6){x = xCentrePhantom + radiusOuterPhantom*cos(t);y = yCentrePhantom + radiusOuterPhantom*sin(t);label = labelRegion;};\n"
        + "border phantomBore1(t=0, 2*pi){x = xCentreBores[0]+radiusBore1*cos(t);y = yCentreBores[0]+radiusBore1*sin(t);label = labelRegion;};\n"
        + "\n"
        + "\n"
    )


@pytest.fixture
def expected_circular_phantom_fflines_pixel_function():
    return (
        "func pixelRegion = \n"
        + "phantomBackgroundBottom(ceil(rMaterialBottom*2*pi*radiusOuterPhantom/h))\n"
        + "+phantomBackgroundTop(ceil(rMaterialStandard*2*pi*radiusOuterPhantom/h))\n"
        + "+phantomBore1(ceil(rMaterialStandard*2*pi*radiusBore1/h))\n"
        + ";\n"
        + "\n"
        + "\n"
        + 'if(BPlot){plot(pixelRegion, wait=false, cmm="Pixel Geometry");}\n'
        + "\n"
        + "\n"
    )


@pytest.fixture
def expected_circular_phantom_fflines_standalone_mesh():
    return (
        "// Macro to generate the mesh. (Can't have comments within macro environment)\n"
        + "macro createMesh(h)\n"
        + "mesh Th = buildmesh(\n"
        + "    pixelRegion\n"
        + ");\n"
        + "// End of macro\n"
        + "\n"
        + "\n"
        + "createMesh(h);\n"
        + "plot(Th);\n"
        + "\n"
        + "\n"
    )


@pytest.fixture
def expected_circular_phantom_fflines_pixel_centres():
    return (
        "// store the centers of each pixel\n"
        + "real[int] pixelCenterX(numBores+1);\n"
        + "real[int] pixelCenterY(numBores+1);\n"
        + "pixelCenterX[0] = xCentrePhantom;\n"
        + "pixelCenterY[0] = yCentrePhantom;\n"
        + "for (int iloopPixel=1; iloopPixel<pixelCenterX.n; iloopPixel++){\n"
        + "\tpixelCenterX[iloopPixel] = xCentreBores[iloopPixel-1];\n"
        + "\tpixelCenterY[iloopPixel] = yCentreBores[iloopPixel-1];\n"
        + "}\n"
    )


# Unit tests for non-uniform curved rectangle pixelation


def test_pixelation_curved_rectangle_nonuniform_make_pixel_header(
    curved_rectangle_nonuniform_object,
    expected_curved_rectangle_nonuniform_fflines_header,
):
    curved_rectangle_nonuniform_object.make_pixel_header()
    curved_rectangle_nonuniform_fflines_header = "".join(
        curved_rectangle_nonuniform_object.fflines_header
    )
    assert (
        curved_rectangle_nonuniform_fflines_header
        == expected_curved_rectangle_nonuniform_fflines_header
    )


def test_pixelation_curved_rectangle_nonuniform_make_pixel_segments(
    curved_rectangle_nonuniform_object,
    expected_curved_rectangle_nonuniform_fflines_pixel_segments,
):
    curved_rectangle_nonuniform_object.make_pixel_segments()
    curved_rectangle_nonuniform_fflines_pixel_segments = "".join(
        curved_rectangle_nonuniform_object.fflines_pixel_segments
    )

    assert (
        curved_rectangle_nonuniform_fflines_pixel_segments
        == expected_curved_rectangle_nonuniform_fflines_pixel_segments
    )


def test_pixelation_curved_rectangle_nonuniform_make_pixel_function(
    curved_rectangle_nonuniform_object,
    expected_curved_rectangle_nonuniform_fflines_pixel_function,
):
    curved_rectangle_nonuniform_object.make_pixel_function()
    curved_rectangle_nonuniform_fflines_pixel_function = "".join(
        curved_rectangle_nonuniform_object.fflines_pixel_function
    )
    assert (
        curved_rectangle_nonuniform_fflines_pixel_function
        == expected_curved_rectangle_nonuniform_fflines_pixel_function
    )


def test_pixelation_curved_rectangle_nonuniform_make_standalone_mesh(
    curved_rectangle_nonuniform_object_standalone,
    expected_curved_rectangle_nonuniform_fflines_standalone_mesh,
):
    curved_rectangle_nonuniform_object_standalone.make_standalone_mesh()
    curved_rectangle_nonuniform_fflines_standalone_mesh = "".join(
        curved_rectangle_nonuniform_object_standalone.fflines_standalone_mesh
    )
    assert (
        curved_rectangle_nonuniform_fflines_standalone_mesh
        == expected_curved_rectangle_nonuniform_fflines_standalone_mesh
    )


def test_pixelation_curved_rectangle_nonuniform_make_pixel_centres(
    curved_rectangle_nonuniform_object,
    expected_curved_rectangle_nonuniform_fflines_pixel_centres,
):
    curved_rectangle_nonuniform_object.make_pixel_centres()
    curved_rectangle_nonuniform_fflines_pixel_centres = "".join(
        curved_rectangle_nonuniform_object.fflines_pixel_centres
    )
    assert (
        curved_rectangle_nonuniform_fflines_pixel_centres
        == expected_curved_rectangle_nonuniform_fflines_pixel_centres
    )


# Integration test to check if freefem geometry compiles for
# curved_rectangle_nonuniform pixels
def tests_pixelation_curved_rectangle_nonuniform_geometry_compilation(
    params_pixels_curved_rectangle_nonuniform,
):
    params_forward = copy.deepcopy(params_forward_9)
    params_forward.pixels = params_pixels_curved_rectangle_nonuniform
    params_forward.pixels.permittivity_matrix = None
    success = run_freefem_geometry(params_forward)
    assert success


# Unit tests for curved rectangle pixelation


def test_pixelation_curved_rectangle_make_pixel_header(
    curved_rectangle_object, expected_curved_rectangle_fflines_header
):
    curved_rectangle_object.make_pixel_header()
    curved_rectangle_fflines_header = "".join(curved_rectangle_object.fflines_header)
    assert curved_rectangle_fflines_header == expected_curved_rectangle_fflines_header


def test_pixelation_curved_rectangle_make_pixel_segments(
    curved_rectangle_object, expected_curved_rectangle_fflines_pixel_segments
):
    curved_rectangle_object.make_pixel_segments()
    curved_rectangle_fflines_pixel_segments = "".join(
        curved_rectangle_object.fflines_pixel_segments
    )

    assert (
        curved_rectangle_fflines_pixel_segments
        == expected_curved_rectangle_fflines_pixel_segments
    )


def test_pixelation_curved_rectangle_make_pixel_function(
    curved_rectangle_object, expected_curved_rectangle_fflines_pixel_function
):
    curved_rectangle_object.make_pixel_function()
    curved_rectangle_fflines_pixel_function = "".join(
        curved_rectangle_object.fflines_pixel_function
    )
    assert (
        curved_rectangle_fflines_pixel_function
        == expected_curved_rectangle_fflines_pixel_function
    )


def test_pixelation_curved_rectangle_make_standalone_mesh(
    curved_rectangle_object_standalone,
    expected_curved_rectangle_fflines_standalone_mesh,
):
    curved_rectangle_object_standalone.make_standalone_mesh()
    curved_rectangle_fflines_standalone_mesh = "".join(
        curved_rectangle_object_standalone.fflines_standalone_mesh
    )
    assert (
        curved_rectangle_fflines_standalone_mesh
        == expected_curved_rectangle_fflines_standalone_mesh
    )


def test_pixelation_curved_rectangle_make_pixel_centres(
    curved_rectangle_object, expected_curved_rectangle_fflines_pixel_centres
):
    curved_rectangle_object.make_pixel_centres()
    curved_rectangle_fflines_pixel_centres = "".join(
        curved_rectangle_object.fflines_pixel_centres
    )
    assert (
        curved_rectangle_fflines_pixel_centres
        == expected_curved_rectangle_fflines_pixel_centres
    )


# Integration test to check if freefem geometry compiles for
# curved_rectangle pixels
def tests_pixelation_curved_rectangle_geometry_compilation(
    params_pixels_curved_rectangle,
):
    params_forward = copy.deepcopy(params_forward_9)
    params_forward.pixels = params_pixels_curved_rectangle
    params_forward.pixels.permittivity_matrix = None
    success = run_freefem_geometry(params_forward)
    assert success


# Unit tests for circular phantom pixelation


def test_pixelation_circular_phantom_make_pixel_header(
    circular_phantom_object, expected_circular_phantom_fflines_header
):
    circular_phantom_object.make_pixel_header()
    circular_phantom_fflines_header = "".join(circular_phantom_object.fflines_header)
    assert circular_phantom_fflines_header == expected_circular_phantom_fflines_header


def test_pixelation_circular_phantom_make_pixel_segments(
    circular_phantom_object, expected_circular_phantom_fflines_pixel_segments
):
    circular_phantom_object.make_pixel_segments()
    circular_phantom_fflines_pixel_segments = "".join(
        circular_phantom_object.fflines_pixel_segments
    )

    assert (
        circular_phantom_fflines_pixel_segments
        == expected_circular_phantom_fflines_pixel_segments
    )


def test_pixelation_circular_phantom_make_pixel_function(
    circular_phantom_object, expected_circular_phantom_fflines_pixel_function
):
    circular_phantom_object.make_pixel_function()
    circular_phantom_fflines_pixel_function = "".join(
        circular_phantom_object.fflines_pixel_function
    )
    assert (
        circular_phantom_fflines_pixel_function
        == expected_circular_phantom_fflines_pixel_function
    )


def test_pixelation_circular_phantom_make_standalone_mesh(
    circular_phantom_object, expected_circular_phantom_fflines_standalone_mesh
):
    circular_phantom_object.make_standalone_mesh()
    circular_phantom_fflines_standalone_mesh = "".join(
        circular_phantom_object.fflines_standalone_mesh
    )
    assert (
        circular_phantom_fflines_standalone_mesh
        == expected_circular_phantom_fflines_standalone_mesh
    )


def test_pixelation_circular_phantom_make_pixel_centres(
    circular_phantom_object, expected_circular_phantom_fflines_pixel_centres
):
    circular_phantom_object.make_pixel_centres()
    circular_phantom_fflines_pixel_centres = "".join(
        circular_phantom_object.fflines_pixel_centres
    )
    assert (
        circular_phantom_fflines_pixel_centres
        == expected_circular_phantom_fflines_pixel_centres
    )


# Integration test to check if freefem geometry compiles for
# circular_phantom pixels
def tests_pixelation_circular_phantom_geometry_compilation(
    params_pixels_circular_phantom,
):
    params_forward = copy.deepcopy(params_forward_9)
    params_forward.geometry.domain_height = 300.0
    params_forward.pixels = params_pixels_circular_phantom
    params_forward.pixels.permittivity_matrix = None
    success = run_freefem_geometry(params_forward)
    assert success
