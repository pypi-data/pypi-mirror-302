from pathlib import Path

import pytest  # noqa

from forwardSolver.scripts.geometry_generation.mesh_utils import (
    mesh_conversion_3D_to_2D,
)


def _write_from_lines(lines, path):
    with open(path, "w") as f:
        for line in lines:
            f.write(f"{line}\n")


def test_mesh_conversion_3D_to_2D(tmp_path):
    input_path = Path(tmp_path / "test_mesh_3D.mesh")
    output_path = Path(tmp_path / "test_mesh_2D.mesh")
    input_lines = [
        "Version",
        "Dimension",
        "3",
        "Vertices",
        "3",
        "0 0 0 1",
        "0 3 0 1",
        "5 5 0 1",
        "Triangles",
        "1",
        "0, 1, 2",
    ]
    output_lines_expected = [
        "Version",
        "Dimension",
        "2",
        "Vertices",
        "3",
        "0 0 1",
        "0 3 1",
        "5 5 1",
        "Triangles",
        "1",
        "0, 1, 2",
    ]
    _write_from_lines(input_lines, input_path)
    mesh_conversion_3D_to_2D(input_path, output_path)
    output_file = open(output_path, "r")
    output_lines_actual = output_file.readlines()
    for i, line in enumerate(output_lines_actual):
        assert line.strip() == output_lines_expected[i]
