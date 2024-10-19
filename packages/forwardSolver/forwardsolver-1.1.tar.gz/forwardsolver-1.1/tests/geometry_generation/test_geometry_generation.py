import os
from dataclasses import asdict, dataclass
from typing import Union

import numpy as np
import pytest

from forwardSolver.scripts.geometry_generation.geometry_generation import (
    GeometricModel2D,
    GeometricModel3D,
    ShapeInfo,
)
from forwardSolver.scripts.geometry_generation.geometry_interface import (
    add_surface,
    clear_models,
    get_entities_in_bounding_box,
    is_initialised,
    synchronise,
)


def _new_geometric_model(dim: int = 2):
    if is_initialised():
        clear_models()
    if dim == 2:
        return GeometricModel2D()
    else:
        return GeometricModel3D()


@pytest.fixture
def basic_model_2D():
    return _new_geometric_model()


@pytest.fixture
def basic_model_3D():
    return _new_geometric_model(dim=3)


def test_add_domain():
    g = _new_geometric_model()
    assert g._domain_added is False
    assert g.domain_attributes is None
    g.add_domain(shape="rectangle", width=5, height=5, permittivity=50)
    assert g.domain_attributes == ShapeInfo(
        permittivity=50, geo_tag=1, description="domain"
    )
    assert g._domain_added is True
    # assert attempting to change the background properties does not update it
    g.add_domain(shape="ellipse", width=60, height=10, permittivity=5)
    assert g.domain_attributes == ShapeInfo(
        permittivity=50, geo_tag=1, description="domain"
    )


def test_add_inner_shape():
    g = _new_geometric_model()
    # check you can't add inner shape before background assignment
    assert g.add_inner_shape() is None
    g.add_domain(width=5, height=5)
    # check you can't add inner shape if not nested
    assert g.add_inner_shape(centre=(10, 0, 0), width=5, height=5) is None
    assert g.add_inner_shape() == ShapeInfo(
        permittivity=20, geo_tag=2, description="fixedRegion"
    )
    assert g.inner_regions == [
        ShapeInfo(permittivity=20, geo_tag=2, description="fixedRegion")
    ]
    g.run_intersections()
    # check you can't add inner shape once intersections are run
    assert g.add_inner_shape() is None


def test_add_boundary():
    g = _new_geometric_model()
    # check you can't add boundary before background assignment
    assert g.add_boundary() is None
    g.add_domain(width=5, height=5)
    # check you can't add inner shape if not nested
    assert g.add_boundary(centre=(10, 0, 0), width=5, height=5) is None
    assert g.add_boundary(description="test_boundary") == ShapeInfo(
        tag=801, description="test_boundary", geo_tag=2
    )
    assert g.boundaries == [ShapeInfo(tag=801, description="test_boundary", geo_tag=2)]
    g.run_intersections()
    # check you can't add inner shape once intersections are run
    assert g.add_boundary() is None


def _generate_test_mesh(tmp_path, g: Union[GeometricModel2D, GeometricModel3D]):
    g.set_mesh_size_params(
        internal_boundary=1,
        internal_region=1,
        domain_boundary=1,
        max_size=2,
    )
    g.generate_mesh(directory=tmp_path)
    assert os.path.exists(os.path.join(tmp_path, "output_mesh.mesh"))
    assert g.get_permittivity_tag_dict() == {
        "domain": [ShapeInfo(permittivity=8, tag=100, geo_tag=1, description="domain")],
        "pixels": [],
    }
    assert g.get_boundary_tag_dict() == {
        "domainBoundary": ["800"],
        "test_boundary": ["801"],
    }


def test_generate_mesh_2D(tmp_path):
    g = _new_geometric_model()
    g.add_domain(width=5, height=5, permittivity=8)
    g.add_boundary(description="test_boundary")
    _generate_test_mesh(tmp_path, g)


def test_generate_mesh_3D(tmp_path):
    g = _new_geometric_model(dim=3)
    g.add_domain(shape="box", width=5, height=5, depth=5, permittivity=8)
    g.add_boundary(
        shape="ellipsoid",
        width=1,
        height=1,
        depth=1,
        description="test_boundary",
    )
    _generate_test_mesh(tmp_path, g)


# --------------------- INTERSECTION TESTING ---------------------
# tests below cover testing of run_intersections, _process_raw_shapes,
# _refine_segments_list, _intersect_two_sets_curves workflow and running
# mesh generation to ensure correct mesh can be produced


@dataclass
class ShapeMaker:
    shape: str = "rectangle"
    centre: tuple = (0, 0, 0)
    width: float = 5
    height: float = 5


def _run_geometry_generation(
    list_of_shapes: list = [], extra_shape_type: str = "ellipse"
):
    for i in range(len(list_of_shapes)):
        _execute_geometry_generation(list_of_shapes, i)
        # run again, for rectangles
        new_shapes = []
        if extra_shape_type:
            for shape in list_of_shapes:
                shape.shape = extra_shape_type
                new_shapes.append(shape)
            _execute_geometry_generation(new_shapes, i)


def _execute_geometry_generation(list_of_shapes: list = [], num_boundaries: int = 0):
    g = _new_geometric_model()
    g.set_mesh_size_params(
        internal_boundary=0.1,
        internal_region=0.3,
        domain_boundary=0.5,
    )
    g.add_domain(width=5, height=5)
    for shape in list_of_shapes[: len(list_of_shapes) - num_boundaries]:
        g.add_inner_shape(**asdict(shape))
    for shape in list_of_shapes[
        len(list_of_shapes) - num_boundaries : len(list_of_shapes)  # noqa: E203
    ]:
        g.add_boundary(**asdict(shape))
    g.run_intersections()
    g.generate_mesh()


def test_background_only():
    # background only
    _execute_geometry_generation()


def test_single_internal():
    # one internal square
    shape_1 = ShapeMaker(width=1, height=1)
    _run_geometry_generation([shape_1])


def test_two_intersect():
    # two squares intersecting
    shape_1 = ShapeMaker(centre=(0, -0.5, 0), width=2, height=2)
    shape_2 = ShapeMaker(centre=(0, 0.5, 0), width=2, height=2)
    _run_geometry_generation([shape_1, shape_2])


def test_two_disjoint():
    # two circles disjoint
    shape_1 = ShapeMaker(centre=(0, -1, 0), width=0.5, height=0.5)
    shape_2 = ShapeMaker(centre=(0, 1, 0), width=0.5, height=0.5)
    _run_geometry_generation([shape_1, shape_2])


def test_three_intersect():
    # three intersecting squares
    shape_1 = ShapeMaker(centre=(0.5, -0.5, 0), width=2, height=2)
    shape_2 = ShapeMaker(centre=(0.5, 0.5, 0), width=2, height=2)
    shape_3 = ShapeMaker(centre=(-0.5, 0, 0), width=2, height=2)
    _run_geometry_generation([shape_1, shape_2, shape_3])


def test_two_intersect_one_disjoint():
    # two squeres intersect, third separate
    shape_1 = ShapeMaker(centre=(0.5, -0.5, 0), width=2, height=1)
    shape_2 = ShapeMaker(centre=(-0.5, -0.5, 0), width=2, height=1)
    shape_3 = ShapeMaker(centre=(1, 0, 0), width=0.5, height=0.5)
    _run_geometry_generation([shape_1, shape_2, shape_3])

    # modified intersection order
    _run_geometry_generation([shape_1, shape_3, shape_2])
    _run_geometry_generation([shape_3, shape_1, shape_2])


def test_cutter_sliced():
    # shape_1 cut in two by shape_2
    shape_1 = ShapeMaker(centre=(0, 0, 0), width=3, height=1)
    shape_2 = ShapeMaker(centre=(0, 0, 0), width=1, height=3)
    _run_geometry_generation([shape_1, shape_2], extra_shape_type=None)
    # TODO make sure this fails if overlapping meshes created - read mesh file


def test_cutter_contained():
    # shape_1 contained by shape_2
    shape_1 = ShapeMaker(centre=(0, 0, 0), width=1, height=1)
    shape_2 = ShapeMaker(centre=(0, 0, 0), width=3, height=3)
    _run_geometry_generation([shape_1, shape_2])


def test_cutter_with_one_nested():
    # shape_2 contained by shape_1
    shape_1 = ShapeMaker(centre=(0, 0, 0), width=3, height=3)
    shape_2 = ShapeMaker(centre=(0, 0, 0), width=1, height=1)
    _run_geometry_generation([shape_1, shape_2])


def test_cutter_with_nested_intersection():
    # shape_2 and shape_3 contained withing shape_1
    shape_1 = ShapeMaker(centre=(0, 0, 0), width=4, height=4)
    shape_2 = ShapeMaker(centre=(0, -0.5, 0), width=1.5, height=1.5)
    shape_3 = ShapeMaker(centre=(0, 0.5, 0), width=1.5, height=1.5)
    _run_geometry_generation([shape_1, shape_2, shape_3])


def test_cutter_with_nested_intersection_and_single():
    # shape_2 and shape_3 intersect and contained within shape_1
    # shape_4 not intersecting contained within shape_1
    shape_1 = ShapeMaker(centre=(0, 0, 0), width=4, height=4)

    shape_2 = ShapeMaker(centre=(1, -0.5, 0), width=1.5, height=1.5)
    shape_3 = ShapeMaker(centre=(1, 0.5, 0), width=1.5, height=1.5)
    shape_4 = ShapeMaker(centre=(-1, 0, 0), width=0.5, height=0.5)

    _run_geometry_generation([shape_1, shape_2, shape_3, shape_4])

    # modified generation order
    _run_geometry_generation([shape_1, shape_2, shape_4, shape_3])
    _run_geometry_generation([shape_1, shape_4, shape_2, shape_3])
    _run_geometry_generation([shape_4, shape_1, shape_2, shape_3])
    _run_geometry_generation([shape_2, shape_1, shape_3, shape_4])


# ------------------ END OF INTERSECTION TESTING ------------------


@pytest.mark.parametrize(
    ("centre, width, height, result"),
    [
        ((0, 0, 0), 1, 1, True),  # nested
        ((0, 10, 0), 1, 1, False),  # outside background
        ((0, 0, 0), 10, 10, False),  # overlaps background
        ((2, 0, 0), 5, 5, False),  # intersects with background
    ],
)
def test_check_if_nested_2D(
    centre: tuple,
    width: float,
    height: float,
    result: bool,
    basic_model_2D: GeometricModel2D,
):
    # add background to model
    if basic_model_2D._domain_added is False:
        basic_model_2D.add_domain(width=5, height=5)
    surface_tag = basic_model_2D._create_shape(
        shape="ellipse", centre=centre, width=width, height=height
    )

    assert basic_model_2D._check_if_nested(object_tag=surface_tag) == result


@pytest.mark.parametrize(
    ("centre, width, height, depth, result"),
    [
        ((0, 0, 0), 1, 1, 1, True),  # nested
        ((0, 10, 0), 1, 1, 1, False),  # outside background
        ((0, 0, 0), 10, 10, 10, False),  # overlaps background
        ((2, 0, 0), 5, 5, 5, False),  # intersects with background
    ],
)
def test_check_if_nested_3D(
    centre: tuple,
    width: float,
    height: float,
    depth: float,
    result: bool,
    basic_model_3D: GeometricModel3D,
):
    # add background to model
    if basic_model_3D._domain_added is False:
        basic_model_3D.add_domain(shape="box", width=5, height=5, depth=5)
    volume_tag = basic_model_3D._create_shape(
        shape="ellipsoid",
        centre=centre,
        width=width,
        height=height,
        depth=depth,
    )

    assert basic_model_3D._check_if_nested(object_tag=volume_tag) == result


@pytest.mark.parametrize(
    "input_list, refined_list",
    [([[1, 2, 3], [2, 3], [4, 5], [5], [5]], [[1], [2, 3], [4], [], [5]])],
)
def test_resolve_fragments(input_list: list, refined_list: list):
    g = GeometricModel2D()
    assert refined_list == g._resolve_fragments(input_list)


def _tags_in_bounding_box(
    list_of_tags: list,
    bb_cords: tuple = (-0.5, -0.5, -0.5, 0.5, 0.5, 0.5),
    dim: int = 1,
):
    synchronise()
    for tag in list_of_tags:
        assert (dim, tag) in get_entities_in_bounding_box(*bb_cords, dim=dim)


def test_create_shape_2D(basic_model_2D: GeometricModel2D):
    with pytest.raises(TypeError):
        basic_model_2D._create_shape()
    with pytest.raises(ValueError):
        basic_model_2D._create_shape(
            shape="unknown", centre=(0, 0, 0), width=1, height=1
        )
    with pytest.raises(ValueError):
        basic_model_2D._create_shape(
            shape="rectangle", centre=(0, 0, 0), width=-1, height=1
        )
    surface_tag = basic_model_2D._create_shape(
        shape="rectangle", centre=(0, 0, 0), width=1, height=1
    )
    _tags_in_bounding_box([surface_tag], dim=2)


def test_add_rectangle_outline(basic_model_2D: GeometricModel2D):
    outline_loop = basic_model_2D._add_rectangle_outline()
    surface = add_surface([outline_loop])
    _tags_in_bounding_box([surface], dim=2)


def test_add_ellipse_outline(basic_model_2D: GeometricModel2D):
    outline_loop = basic_model_2D._add_ellipse_outline()
    surface = add_surface([outline_loop])
    _tags_in_bounding_box([surface], dim=2)

    with pytest.raises(Exception):
        _, _ = basic_model_2D._add_ellipse_outline(width=-1)


def test_create_shape_3D(basic_model_3D: basic_model_3D):
    with pytest.raises(TypeError):
        basic_model_3D._create_shape()
    with pytest.raises(ValueError):
        basic_model_3D._create_shape(
            shape="unknown", centre=(0, 0, 0), width=1, height=1, depth=1
        )
    volume_tag = basic_model_3D._create_shape(
        shape="box", centre=(0, 0, 0), width=1, height=1, depth=1
    )
    _tags_in_bounding_box([volume_tag], dim=3)


def test_rotate_pixels(basic_model_3D: GeometricModel3D):
    basic_model_3D.add_inner_shape(
        shape="box", width=1, height=1, depth=1, description="pixels"
    )

    basic_model_3D.rotate_pixels(shapes=basic_model_3D.inner_regions, rotation_idx=1)
    with pytest.raises(ValueError):
        basic_model_3D.rotate_pixels(
            shapes=basic_model_3D.inner_regions, use_raw_angle=True
        )
    basic_model_3D.rotate_pixels(
        shapes=basic_model_3D.inner_regions, use_raw_angle=True, angle=0.1
    )


@pytest.mark.parametrize(
    ("nested_list, flattened_list"),
    [
        ([[1, 2, 3], [4, 5]], [1, 2, 3, 4, 5]),
        ([[1, 2, [3]], [4, 5]], [1, 2, [3], 4, 5]),
        ([[]], []),
    ],
)
def test_flatten_list(nested_list: list, flattened_list: list):
    assert GeometricModel2D._flatten_list(nested_list) == flattened_list


def test_update_permittivity(tmp_path_factory, basic_model_2D: GeometricModel2D):
    dir = tmp_path_factory.mktemp("meshes")
    basic_model_2D.add_domain(shape="rectangle", width=5, height=5)
    basic_model_2D.add_inner_shape(shape="ellipse", centre=(-2, 0, 0), permittivity=20)
    basic_model_2D.add_inner_shape(
        shape="ellipse", centre=(2, 0, 0), permittivity=30, sub_info="board"
    )
    basic_model_2D.run_intersections()
    basic_model_2D.generate_mesh(directory=dir)

    with open(dir / "output_parameter_mapping.txt", "r") as file:
        lines = file.readlines()

    expected = (
        "domain 1\n100 1.0006\nfixedRegion 2\n101 30\n"
        "102 20\npixels 0\ndomainBoundary 1\n800\n"
    )
    assert "".join(lines) == expected

    # Check update permittivities with physical group
    basic_model_2D.update_permittivities(
        new_permittivities_dict={101: 15}, use_sub_info=False
    )

    with open(dir / "output_parameter_mapping.txt", "r") as file:
        lines = file.readlines()

    expected = (
        "domain 1\n100 1.0006\nfixedRegion 2\n101 15\n"
        "102 20\npixels 0\ndomainBoundary 1\n800\n"
    )
    assert "".join(lines) == expected

    # Check update permittivities with sub_info
    basic_model_2D.update_permittivities(
        new_permittivities_dict={"board": 10}, use_sub_info=True
    )

    with open(dir / "output_parameter_mapping.txt", "r") as file:
        lines = file.readlines()

    expected = (
        "domain 1\n100 1.0006\nfixedRegion 2\n101 10\n"
        "102 20\npixels 0\ndomainBoundary 1\n800\n"
    )
    assert "".join(lines) == expected

    # Check that update_permittivitites with empty dict and with a key that does not exist
    # also works
    basic_model_2D.update_permittivities(
        new_permittivities_dict=dict(), use_sub_info=True
    )
    basic_model_2D.update_permittivities(
        new_permittivities_dict={145: 10}, use_sub_info=False
    )

    with open(dir / "output_parameter_mapping.txt", "r") as file:
        lines = file.readlines()

    expected = (
        "domain 1\n100 1.0006\nfixedRegion 2\n101 10\n"
        "102 20\npixels 0\ndomainBoundary 1\n800\n"
    )
    assert "".join(lines) == expected


def test_update_pixels(tmp_path_factory, basic_model_2D: GeometricModel2D):
    dir = tmp_path_factory.mktemp("meshes")
    basic_model_2D.add_domain(shape="rectangle", width=5, height=5)
    basic_model_2D.add_inner_shape(shape="ellipse", centre=(-2, 0, 0), permittivity=20)
    basic_model_2D.add_inner_shape(shape="ellipse", centre=(2, 0, 0), permittivity=30)

    permittivity_array = np.random.random(size=(3, 3))
    for i in range(3):
        for j in range(3):
            basic_model_2D.add_inner_shape(
                shape="rectangle",
                centre=((i - 1) * 0.5, (j - 1) * 0.5, 0),
                width=0.5,
                height=0.5,
                description="pixels",
                sub_info=f"p_{i}_{j}",
                permittivity=permittivity_array[i][j],
            )

    basic_model_2D.run_intersections()
    basic_model_2D.generate_mesh(directory=dir)

    expected = "domain 1\n100 1.0006\nfixedRegion 2\n110 30\n111 20\npixels 9\n"
    for i in range(3):
        for j in range(3):
            expected += f"{101+3*i+j} {permittivity_array[2-i][2-j]}\n"

    expected += "domainBoundary 1\n800\n"

    with open(dir / "output_parameter_mapping.txt", "r") as file:
        lines = file.readlines()

    assert "".join(lines) == expected

    # Check update pixels
    new_permittivity_array = np.random.random(size=(3, 3))
    basic_model_2D.update_pixels(new_permittivity_array)

    expected = "domain 1\n100 1.0006\nfixedRegion 2\n110 30\n111 20\npixels 9\n"
    for i in range(3):
        for j in range(3):
            expected += f"{101+3*i+j} {new_permittivity_array[2-i][2-j]}\n"

    expected += "domainBoundary 1\n800\n"

    with open(dir / "output_parameter_mapping.txt", "r") as file:
        lines = file.readlines()

    assert "".join(lines) == expected
