from dataclasses import asdict, dataclass
from typing import Optional

import numpy as np


@dataclass(kw_only=True)
class GeometryParams:
    """
    Geometric parameters of the simulation that feed into the FreeFEM calculations.
    Attributes:
        mesh_elements_on_border (Optional[int]): Number of elements along standard borders.
        mesh_length_scale (Optional[float]): Mesh size.
        domain_width (Optional[float]): Full domain width.
        domain_height (Optional[float]): Full domain height.
        domain_length (Optional[float]): Full domain length.
        electrode_width (Optional[float]): Electrode width.
        electrode_length (Optional[float]): Electrode length.
        electrode_height (Optional[float]): Electrode height.
        number_electrodes (Optional[int]): Number of electrodes.
        electrode_separation (Optional[float]): Separation of electrode centres.
        pcb_substrate_width (Optional[float]): Width of the PCB substrate.
        pcb_substrate_height (Optional[float]): Height of the PCB substrate.
        soldercoat_height (Optional[float]): Thickness of the solder coat.
        ground_wing_width (Optional[float]): Grounded wing length.
        ground_wing_gap (Optional[float]): Grounded wing to electrode edge gap.
        permittivity_pcb_substrate (Optional[float]): Permittivity of the PCB substrate.
        conductivity_pcb_substrate (Optional[float]): Conductivity of the PCB substrate.
        permittivity_background (Optional[float]): Permittivity of the background.
        conductivity_background (Optional[float]): Conductivity of the background.
        permittivity_soldercoat (Optional[float]): Permittivity of the solder coat.
        conductivity_soldercoat (Optional[float]): Conductivity of the solder coat.
        board_centre_width (Optional[float]): Width of the board centre.
        board_left_width (Optional[float]): Width of the left part of the board.
        board_right_width (Optional[float]): Width of the right part of the board.
        board_height (Optional[float]): Height of the board/membrane.
        board_strip_width (Optional[float]): Width of the board strips underneath the electrodes.
        frame_height (Optional[float]): Height of the supporting frame.
        bottom_ground_plate_height (Optional[float]): Height of the ground plate below the frame.
        left_ground_plate_width (Optional[float]): Width of the ground plate on the left of the board.
        right_ground_plate_width (Optional[float]): Width of the ground plate on the right of the board.
        ground_wing_offset (Optional[float]): Offset of the ground wing from the left margin of the board.
        chord_length (Optional[float]): Width of the curved opening of the curved sensor.
        chord_angle (Optional[float]): Angle of the curved opening of the curved sensor.
        total_frame_height (Optional[float]): Maximum height of the frame below the board surface.
        electrode_span_width (Optional[float]): Compute width of the board based on electrodes.
        board_left_extra_width (Optional[float]): Extra space on the left of the board.
        board_right_extra_width (Optional[float]): Extra space on the right of the board.
        curvature_centre (Optional[tuple]): Centre of curvature.
        system_offset_y (Optional[float]): Offset of the board in the y direction.
        material_offset_x (Optional[float]): Material pixelation offset from the leftmost point of the board.
        permittivity_board (Optional[float]): Permittivity of the board.
        conductivity_board (Optional[float]): Conductivity of the board.
        permittivity_frame (Optional[float]): Permittivity of the frame.
        conductivity_frame (Optional[float]): Conductivity of the frame.
        material_width (Optional[float]): Width of the material under test.
        material_height (Optional[float]): Height of the material under test.
        material_length (Optional[float]): Length of the material under test.
        material_gap (Optional[float]): Gap between the substrate and the material under test.
        curvature_radius (Optional[float]): Radius of curvature from the surface of the board.
        ground_plate_thickness (Optional[float]): Thickness of the ground plate.
        ground_plate_depth (Optional[float]): Depth of the ground plate below the electrodes.
        top_ground_layer_thickness (Optional[float]): Thickness of the top ground layer.
        mylar_thickness (Optional[float]): Thickness of the mylar.
        mylar_gap (Optional[float]): Gap of the mylar.
        oil_thickness (Optional[float]): Thickness of the oil.
        plastic_thickness (Optional[float]): Thickness of the plastic.
        gel_thickness (Optional[float]): Thickness of the gel.
        permittivity_mylar (Optional[float]): Permittivity of the mylar.
        conductivity_mylar (Optional[float]): Conductivity of the mylar.
        permittivity_gel (Optional[float]): Permittivity of the gel.
        conductivity_gel (Optional[float]): Conductivity of the gel.
        permittivity_plastic (Optional[float]): Permittivity of the plastic.
        conductivity_plastic (Optional[float]): Conductivity of the plastic.
        permittivity_oil (Optional[float]): Permittivity of the oil.
        conductivity_oil (Optional[float]): Conductivity of the oil.
        base_radius (Optional[float]): Base radius.
    Methods:
        __eq__(self, other): Checks equality of two GeometryParams objects.
        as_dict(self): Converts the GeometryParams object to a dictionary.
        to_freefem(self): Converts the GeometryParams object to a FreeFEM instruction string.
    """

    # Number of elements along standard borders (-)
    mesh_elements_on_border: Optional[int] = None
    # Mesh size
    mesh_length_scale: Optional[float] = None
    # Full domain geometry
    domain_width: Optional[float] = None
    domain_height: Optional[float] = None
    domain_length: Optional[float] = None
    # Electrode geometry
    electrode_width: Optional[float] = None
    electrode_length: Optional[float] = None
    electrode_height: Optional[float] = None
    number_electrodes: Optional[int] = None
    # Separation of electrode centres
    electrode_separation: Optional[float] = None

    # P1000-006 Parameters
    # Geometry of PCB
    pcb_substrate_width: Optional[float] = None
    pcb_substrate_height: Optional[float] = None
    #  Thickness (mm) of the solder coat
    soldercoat_height: Optional[float] = None
    # Grounded wing length (mm)
    ground_wing_width: Optional[float] = None
    # Grounded wing to electrode edge (mm)
    ground_wing_gap: Optional[float] = None

    permittivity_pcb_substrate: Optional[float] = None
    conductivity_pcb_substrate: Optional[float] = None
    permittivity_background: Optional[float] = None
    conductivity_background: Optional[float] = None
    permittivity_soldercoat: Optional[float] = None
    conductivity_soldercoat: Optional[float] = None

    # P1000-009 Parameters
    # Width of the part of the board that holds the electrodes and can be curved (mm)
    board_centre_width: Optional[float] = None
    # Width of the left part of the board
    board_left_width: Optional[float] = None
    # Width of the right part of the board
    board_right_width: Optional[float] = None
    # Board/Membrane height (mm)
    board_height: Optional[float] = None
    # Width of the board strips underneath the electrodes
    board_strip_width: Optional[float] = None
    # Height of the supporting frame
    frame_height: Optional[float] = None
    # Height of the ground plate below the frame
    bottom_ground_plate_height: Optional[float] = None
    # Width of the ground plate on the left of the board
    left_ground_plate_width: Optional[float] = None
    # Width of the ground plate on the right of the board
    right_ground_plate_width: Optional[float] = None
    # Offset of the ground wing from the left margin of the board
    ground_wing_offset: Optional[float] = None
    # Width of curved opening of the curved sensor
    chord_length: Optional[float] = None
    # Angle of curved opening of the curved sensor
    chord_angle: Optional[float] = None
    # Maximum height of the frame below the board surface
    total_frame_height: Optional[float] = None
    # Compute width of board based on electrodes
    electrode_span_width: Optional[float] = None
    # Extra space on left/right of board
    board_left_extra_width: Optional[float] = None
    board_right_extra_width: Optional[float] = None
    # Centre of curvature
    curvature_centre: Optional[tuple] = None
    # offset of board in y direction
    system_offset_y: Optional[float] = None
    # Material pixelation offset from leftmost point of board
    material_offset_x: Optional[float] = None

    # Permittivities of board and frame
    permittivity_board: Optional[float] = None
    conductivity_board: Optional[float] = None
    permittivity_frame: Optional[float] = None
    conductivity_frame: Optional[float] = None

    # Dimensions of the material under test (mm)
    material_width: Optional[float] = None
    material_height: Optional[float] = None
    material_length: Optional[float] = None
    # Gap between substrate and material under test (mm)
    material_gap: Optional[float] = None
    # Radius of curvature from surface of board (mm)
    curvature_radius: Optional[float] = None

    # P3000-005 board params
    ground_plate_thickness: Optional[float] = None
    ground_plate_depth: Optional[float] = None
    top_ground_layer_thickness: Optional[float] = None
    mylar_thickness: Optional[float] = None
    mylar_gap: Optional[float] = None
    oil_thickness: Optional[float] = None
    plastic_thickness: Optional[float] = None
    gel_thickness: Optional[float] = None
    permittivity_mylar: Optional[float] = None
    conductivity_mylar: Optional[float] = None
    permittivity_gel: Optional[float] = None
    conductivity_gel: Optional[float] = None
    permittivity_plastic: Optional[float] = None
    conductivity_plastic: Optional[float] = None
    permittivity_oil: Optional[float] = None
    base_radius: Optional[float] = None
    conductivity_oil: Optional[float] = None

    # Params map to FreeFEM variable name
    params_map = {
        "mesh_length_scale": "h",
        "domain_width": "xDomainW",
        "domain_height": "xDomainH",
        "electrode_width": "xElecW",
        "electrode_height": "xElecH",
        "electrode_separation": "xElecSep",
        "material_width": "xMaterialW",
        "material_height": "xMaterialH",
        "material_gap": "xMaterialGap",
        "curvature_radius": "rCurvature",
        # P1000-006
        "pcb_substrate_width": "xSubstrateW",
        "pcb_substrate_height": "xSubstrateH",
        "ground_wing_width": "xWingW",
        "ground_wing_gap": "xWingGap",
        "soldercoat_height": "xSolderH",  # also used for P1000-014
        "permittivity_pcb_substrate": "eSubstrate",
        "conductivity_pcb_substrate": "sSubstrate",
        "permittivity_background": "eBackground",  # also used for P1000-014
        "conductivity_background": "sBackground",  # also used for P1000-014
        "permittivity_soldercoat": "eSolderCoat",  # also used for P1000-014
        "conductivity_soldercoat": "sSolderCoat",  # also used for P1000-014
        # P1000-009
        "board_centre_width": "xBoardCentreW",
        "board_left_width": "xBoardLeftW",  # also used for P1000-014
        "board_right_width": "xBoardRightW",  # also used for P1000-014
        "board_height": "xBoardH",  # also used for P1000-014
        "board_strip_width": "xBoardStripW",
        "frame_height": "xFrameH",
        "bottom_ground_plate_height": "xBottomGndPlateH",
        "left_ground_plate_width": "xLeftGndPlateW",  # also used for P1000-014
        "ground_wing_offset": "xMarginW",
        "ground_plate_thickness": "GroundPlateThickness",
        "permittivity_board": "eBoard",  # also used for P1000-014
        "conductivity_board": "sBoard",  # also used for P1000-014
        "permittivity_frame": "eFrame",
        "conductivity_frame": "sFrame",
        # P3000-005
        "ground_plate_depth": "GroundPlateDepthBelowElec",
        "mylar_thickness": "xMylarH",
        "mylar_gap": "xMylarGap",
        "plastic_thickness": "xPlasticH",
        "permittivity_mylar": "eMylar",
        "conductivity_mylar": "sMylar",
        "permittivity_plastic": "ePlastic",
        "conductivity_plastic": "sPlastic",
        "oil_thickness": "xOilH",
        "gel_thickness": "xGelH",
        "permittivity_oil": "eOil",
        "conductivity_oil": "sOil",
        "permittivity_gel": "eGel",
        "conductivity_gel": "sGel",
        # P1000-014
        "right_ground_plate_width": "xRightGndPlateW",
        "system_offset_y": "xOffsetY",
        "material_offset_x": "xMaterialOffsetX",
    }

    def __eq__(self, other):
        try:
            np.testing.assert_equal(self.as_dict(), other.as_dict())
        except AssertionError:
            return False
        return True

    def as_dict(self):
        return asdict(self)

    def to_freefem(self):
        """
        Convert ParamsModule to FreeFEM instruction
        Only include defined (i.e. not None) parameters
        """
        return (
            " ".join(
                [
                    f"{v} {getattr(self, k)}"
                    for k, v in self.params_map.items()
                    if getattr(self, k) is not None
                ]
            )
            + " "
        )
