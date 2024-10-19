from typing import Union

import gmsh

# gmsh kernel


def initialise_geometry_kernel():
    if not gmsh.isInitialized():
        gmsh.initialize()


def synchronise():
    gmsh.model.occ.synchronize()


def is_initialised():
    return gmsh.isInitialized()


def clear_models():
    gmsh.clear()


def set_terminal_output(output_to_terminal: bool = True):
    gmsh.option.setNumber("General.Terminal", int(output_to_terminal))


def set_verbosity(verbosity: int = 3):
    # verbosity levels
    # 0: silent except for fatal errors, 1: +errors, 2: +warnings,
    # 3: +direct, 4: +information, 5: +status, 99: +debug
    gmsh.option.setNumber("General.Verbosity", verbosity)


def set_custom_setting(name: str, value: Union[int, str], type: str = "number"):
    # set option depending on setting type
    if type == "number":
        gmsh.option.setNumber(name, value)
    elif type == "string":
        gmsh.option.setString(name, value)


# generative operations on entities


def cut_objects(
    objects_to_be_cut: list,
    cutters: list,
    remove_object: bool = False,
    remove_tool: bool = False,
    dim: int = 2,
) -> list:
    return gmsh.model.occ.cut(
        [(dim, tag) for tag in objects_to_be_cut],
        [(dim, tag) for tag in cutters],
        removeObject=remove_object,
        removeTool=remove_tool,
    )


def intersect_objects(
    objects_to_intersect: list,
    objects_to_intersect_with: list,
    remove_object: bool = False,
    remove_tool: bool = False,
    dim: int = 2,
) -> list:
    return gmsh.model.occ.intersect(
        [(dim, tag) for tag in objects_to_intersect],
        [(dim, tag) for tag in objects_to_intersect_with],
        removeObject=remove_object,
        removeTool=remove_tool,
    )


def general_fuse_objects(
    object_to_fuse_to: list,
    objects_to_fuse_with: list,
    remove_object: bool = True,
    remove_tool: bool = True,
    dim: int = 2,
) -> list:
    return gmsh.model.occ.fragment(
        [(dim, tag) for tag in object_to_fuse_to],
        [(dim, tag) for tag in objects_to_fuse_with],
        removeObject=remove_object,
        removeTool=remove_tool,
    )


def fuse_objects(
    object_to_fuse_to: list,
    objects_to_fuse_with: list,
    remove_object: bool = True,
    remove_tool: bool = True,
) -> list:
    return gmsh.model.occ.fuse(
        object_to_fuse_to,
        objects_to_fuse_with,
        removeObject=remove_object,
        removeTool=remove_tool,
    )


def extrude_2D_objects(
    tags: list, dim: int = 2, dx: float = 0, dy: float = 0, dz: float = 0
):
    return gmsh.model.occ.extrude(
        dimTags=[(dim, tag) for tag in tags], dx=dx, dy=dy, dz=dz
    )


# mesh properties and generation


def run_mesh_generation(dim: int = 2, tag_type_list: list = [1, 2]):
    for tag_type in tag_type_list:
        gmsh.option.setNumber("Mesh.SaveElementTagType", tag_type)
    gmsh.model.mesh.generate(dim)


def set_mesh_size_at_entities(entity_list: list, mesh_size: float):
    gmsh.model.mesh.setSize(entity_list, mesh_size)


def save_mesh_to_path(path: str):
    gmsh.write(path)


def set_mesh_size_at_objects(
    *,
    points: list = [],
    curves: list = [],
    surfaces: list = [],
    size_min: float = 1,
    size_max: float = 10,
    threshold_lower: float = 3,
    threshold_upper: float = 15,
    sampling: int = 500,
) -> int:
    # threshold setup allows for varying mesh size along distance away from object
    # sampled (Point):
    #
    # SizeMax -                     /------------------
    #                              /
    #                             /
    #                            /
    # SizeMin -o----------------/
    #          |                |    |
    #        Point         DistMin  DistMax

    distance_tag = gmsh.model.mesh.field.add("Distance", -1)
    if points:
        gmsh.model.mesh.field.setNumbers(distance_tag, "PointsList", points)
    if curves:
        gmsh.model.mesh.field.setNumbers(distance_tag, "CurvesList", curves)
    if surfaces:
        gmsh.model.mesh.field.setNumbers(distance_tag, "SurfacesList", surfaces)
    gmsh.model.mesh.field.setNumber(distance_tag, "Sampling", sampling)

    threshold_tag = gmsh.model.mesh.field.add("Threshold", -1)
    gmsh.model.mesh.field.setNumber(threshold_tag, "InField", distance_tag)
    gmsh.model.mesh.field.setNumber(threshold_tag, "SizeMin", size_min)
    gmsh.model.mesh.field.setNumber(threshold_tag, "SizeMax", size_max)
    gmsh.model.mesh.field.setNumber(threshold_tag, "DistMin", threshold_lower)
    gmsh.model.mesh.field.setNumber(threshold_tag, "DistMax", threshold_upper)
    return threshold_tag


def set_mesh_size_within_box(
    size_inside: float,
    size_outside: float,
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    z_min: float = 0,
    z_max: float = 0,
    thickness: float = 5,
):
    box_tag = gmsh.model.mesh.field.add("Box", -1)
    gmsh.model.mesh.field.setNumber(box_tag, "VIn", size_inside)
    gmsh.model.mesh.field.setNumber(box_tag, "VOut", size_outside)
    gmsh.model.mesh.field.setNumber(box_tag, "XMin", x_min)
    gmsh.model.mesh.field.setNumber(box_tag, "XMax", x_max)
    gmsh.model.mesh.field.setNumber(box_tag, "YMin", y_min)
    gmsh.model.mesh.field.setNumber(box_tag, "YMax", y_max)
    gmsh.model.mesh.field.setNumber(box_tag, "ZMin", z_min)
    gmsh.model.mesh.field.setNumber(box_tag, "ZMax", z_max)
    gmsh.model.mesh.field.setNumber(box_tag, "Thickness", thickness)

    return box_tag


def mesh_fields_set(fields_list: list = []):
    gmsh.option.setNumber("Mesh.MeshSizeExtendFromBoundary", 0)
    gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 0)
    gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 0)
    if fields_list:
        min_tag = gmsh.model.mesh.field.add("Min", -1)
        gmsh.model.mesh.field.setNumbers(min_tag, "FieldsList", fields_list)
        gmsh.model.mesh.field.setAsBackgroundMesh(min_tag)


def set_meshing_algorithm(algorithm: str = "Frontal-Delaunay"):
    if algorithm == "Frontal-Delaunay":
        gmsh.option.setNumber("Mesh.Algorithm", 6)
    elif algorithm == "Delaunay":
        gmsh.option.setNumber("Mesh.Algorithm", 5)
    elif algorithm == "MeshAdapt":
        gmsh.option.setNumber("Mesh.Algorithm", 1)


def add_point(x: float, y: float, z: float = 0, mesh_size: float = 0) -> int:
    return gmsh.model.occ.addPoint(x=x, y=y, z=z, meshSize=mesh_size)


def add_line(point_1: int, point_2: int) -> int:
    return gmsh.model.occ.addLine(point_1, point_2)


def add_loop(objects_to_loop: list, dim: int = 2) -> int:
    if dim == 2:
        return gmsh.model.occ.addCurveLoop(objects_to_loop)


def add_circular_arc(start: tuple, centre: tuple, end: tuple) -> int:
    return gmsh.model.occ.addCircleArc(start, centre, end)


def add_ellipse(
    centre: tuple = (0, 0, 0),
    radius_x: float = 0.5,
    radius_y: float = 0.5,
    angle_1: float = 0,
) -> int:
    # angles in radians
    return gmsh.model.occ.addEllipse(
        centre[0],
        centre[1],
        centre[2],
        r1=radius_x,
        r2=radius_y,
        angle1=angle_1,
    )


def add_rectangle(
    centre: tuple = (0, 0, 0),
    width: float = 1,
    height: float = 1,
    radius: float = 0,
) -> int:
    return gmsh.model.occ.addRectangle(
        x=centre[0] - width / 2,
        y=centre[1] - height / 2,
        z=centre[2],
        dx=width,
        dy=height,
        roundedRadius=radius,
    )


def add_surface(curve_loops_tags: list) -> int:
    # addPlaneSurface takes list of curve loop tags
    # e.g. [501, 502]
    return gmsh.model.occ.addPlaneSurface(curve_loops_tags)


# 3D
def scale_object(
    tags: list,
    dim: int = 3,
    centre: tuple = (0, 0, 0),
    scale_x: float = 1,
    scale_y: float = 1,
    scale_z: float = 1,
):
    gmsh.model.occ.dilate(
        [(dim, tag) for tag in tags],
        x=centre[0],
        y=centre[1],
        z=centre[2],
        a=scale_x,
        b=scale_y,
        c=scale_z,
    )
    return tags


def rotate_objects(
    tags: list,
    dim: int = 3,
    centre: tuple = (0, 0, 0),
    theta_x: float = 0,
    theta_y: float = 0,
    theta_z: float = 0,
    angle: float = 0,
):
    gmsh.model.occ.rotate(
        [(dim, tag) for tag in tags],
        x=centre[0],
        y=centre[1],
        z=centre[2],
        ax=theta_x,
        ay=theta_y,
        az=theta_z,
        angle=angle,
    )
    return tags


def add_volume_from_outline(surface_loops_tags: list) -> int:
    return gmsh.model.occ.addVolume(shellTags=surface_loops_tags)


def add_ellipsoid(
    *,
    centre: tuple = (0, 0, 0),
    width: float = 1,
    height: float = 1,
    depth: float = 1,
) -> int:
    sphere = gmsh.model.occ.addSphere(
        xc=centre[0], yc=centre[1], zc=centre[2], radius=width / 2
    )
    gmsh.model.occ.dilate(
        dimTags=[(3, sphere)],
        x=centre[0],
        y=centre[1],
        z=centre[2],
        a=1,
        b=height / width,
        c=depth / width,
    )

    return sphere


def add_box(
    centre: tuple = (0, 0, 0),
    width: float = 1,
    height: float = 1,
    depth: float = 1,
) -> int:
    left_bottom_back_x = centre[0] - width / 2
    left_bottom_back_y = centre[1] - height / 2
    left_bottom_back_z = centre[2] - depth / 2
    box = gmsh.model.occ.addBox(
        x=left_bottom_back_x,
        y=left_bottom_back_y,
        z=left_bottom_back_z,
        dx=width,
        dy=height,
        dz=depth,
    )

    return box


def add_cylindroid(
    centre: tuple = (0, 0, 0),
    radius: float = 1,
    height: float = 1,
) -> int:
    cylinder = gmsh.model.occ.addCylinder(
        x=centre[0],
        y=centre[1] - height / 2,
        z=centre[2],
        r=radius,
        dx=0,
        dy=height,
        dz=0,
    )

    return cylinder


# translate/ rotate 3D geometry


def translate_objects(
    *, tags: list, dim: int = 3, dx: float = 0, dy: float = 0, dz: float = 0
):
    gmsh.model.occ.translate(dimTags=[(dim, tag) for tag in tags], dx=dx, dy=dy, dz=dz)
    return tags


# add/ modify mesh objects


def add_nodes(tag: int, dim: int = 1, coord: list = []):
    return gmsh.model.mesh.addNodes(dim=dim, tag=tag, nodeTags=[], coord=coord)


def reverse_object(object: int, dim: int = 1):
    return gmsh.model.mesh.reverse([(dim, object)])


# get objects/ mesh elements


def get_bounding_box(object_tag: int, dim: int = 2):
    return gmsh.model.getBoundingBox(dim, object_tag)


def get_entities_in_bounding_box(
    xmin: float = -0.5,
    ymin: float = -0.5,
    zmin: float = 0,
    xmax: float = 0.5,
    ymax: float = 0.5,
    zmax: float = 0,
    dim: int = -1,
    tol: float = 1e-7,
):
    # note if dim specified, only entities of the given dim are returned
    # tol inherent offset occ applies to bounding boxes
    return gmsh.model.occ.getEntitiesInBoundingBox(
        xmin=xmin - tol,
        ymin=ymin - tol,
        zmin=zmin - tol,
        xmax=xmax + tol,
        ymax=ymax + tol,
        zmax=zmax + tol,
        dim=dim,
    )


def get_loops(object_tag: int, dim: int = 2) -> list:
    if dim == 2:
        return gmsh.model.occ.getCurveLoops(object_tag)
    if dim == 3:
        return gmsh.model.occ.getSurfaceLoops(object_tag)


def get_coordinates(tag: int, dim: int = 1, parametric_coord: list = [0]):
    return gmsh.model.getValue(dim=dim, tag=tag, parametricCoord=parametric_coord)


def get_parametrisation_bounds(tag: int, dim: int = 1):
    return gmsh.model.getParametrizationBounds(dim, tag)


def get_duplicate_nodes(tags: list = [], dim: int = 2) -> list:
    # if tags list is empty, considering the whole mesh
    return gmsh.model.mesh.getDuplicateNodes([(dim, tag) for tag in tags])


def get_nodes(
    tag: int,
    dim: int = 1,
    incl_boundary=False,
    return_parametric: bool = False,
):
    return gmsh.model.mesh.getNodes(
        dim=dim,
        tag=tag,
        includeBoundary=incl_boundary,
        returnParametricCoord=return_parametric,
    )


# remove entities


def remove_entities(tags: list = [], dim: int = 2, recursive=True):
    gmsh.model.occ.remove([(dim, tag) for tag in tags], recursive=recursive)


# operate on physical groups


def add_physical_group(objects, tag: int, dim: int = 2) -> int:
    return gmsh.model.addPhysicalGroup(dim, objects, tag=tag)


def get_entities_in_physical_group(tag: int, dim: int = 1):
    return gmsh.model.getEntitiesForPhysicalGroup(dim, tag)


def remove_physical_groups(tags: list = [], dim: int = 3):
    gmsh.model.removePhysicalGroups(dimTags=[(dim, tag) for tag in tags])
