pixelation = {
    "create_standalone": False,  # Will the resulting script be run standalone?
    "region_width": "xMaterialW",  # width can be number or recognised FreeFem variable
    "region_height": "xMaterialH",  # height can be number or recognised FreeFem variable
    "region_label": 300,
    "num_pixel_rows": 1,  # number of rows in pixelated region
    "num_pixel_columns": 1,  # number of columns in pixelated region
    "num_pixel_layers": 1,  # number of depth layers in pixelated region 3D
    "pixel_columns_per_row": None,  # array with the number of pixels in each row
    "permittivity_matrix": None,
    "conductivity_matrix": None,
    "pixel_type": "curved_rectangle",
    "circular_phantom_radius": None,
    "circular_phantom_bore_radii": None,
    "circular_phantom_bore_centre_distance": None,
    "circular_phantom_angle": None,
    "circular_phantom_thickness": None,
}
