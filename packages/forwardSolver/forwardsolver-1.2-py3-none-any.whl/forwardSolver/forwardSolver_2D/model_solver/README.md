## Refactored FreeFEM code

The refactoring allows the same model_solver file to be called for different geometries, which are passed as command line arguments

To run P1000-009 board, call
>>> FreeFem++ model_solver.edp boardGeometry P1000-009
followed by any other parameters

To run P3000-005 board, call
>>> FreeFem++ model_solver.edp boardGeometry P3000-005
followed by any other parameters

You can also do a dry-run with no calculations to check the input is correctly formed by passing a flag `dryRun 1`. The argument `dryRun` is by default set to 0 (indicating that by default we run the model calculation).

To check the inputs by plotting, you need to pass a flag `BCheckInputs 1`.
To check each individual pixel by plotting, pass `BPlotCheckEachPixel 1`.


Default values:
- `boardGeometry: P1000-009`
- `dryRun: 0`
- `BCheckInputs: 0`
- `BPlotCheckEachPixel: 0`

# Adding a geometry

To add a new geometry to the solver, you need to

1. Create a geometry_****.edp file. This must include (*in this order*)
    - Define all the borders that define the domain
    - Define `regionW, regionH, labelRegion, regionOffsetX, regionOffsetY`
    - `include "pixel_region.edp"`
    - `include "utils.edp"`
    - `macro createMesh(h)`, which generates a `mesh Th` object
    - `DefineFESpaces(Th)`
    - Find region labels as appropriate
    - Material parameters for geometry
        - Define a `Vh0[int] permittivities` array with as many components as necessary
          to define the permittivity for all regions of interest *+1*, leaving space for
          the pixelated region permittivity distribution to be added later.
    - Boundary conditions for geometry
        - Define the `macro InitialiseGroundBoundaryConditions(ABC, rhsBC)`
        - Define the array `int[int] groundLabels` with all labels corresponding to
          grounded surfaces

    NOTE: The geometry definition must include regions labelled as if they were electrodes
    The macro `DefineBoundaryConditions` in the model solver is going to iterate over
    boundaries labelled from 1 to NE

2. Create a args_****.edp file with any geometry-specific arguments. Have a look at
   other args files for example.
   *must include*
    - h: mesh size
    - NE: number of electrodes


3. Edit `model_solver.edp` to add another case to the `if` statement to catch your new
   geometry.