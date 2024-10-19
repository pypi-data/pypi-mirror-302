import datetime
import json
import os
import re
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Union, get_type_hints

import numpy as np

from forwardSolver.scripts.utils.json_coder import (
    CustomJsonDecoder,
    CustomJsonEncoder,
)


@dataclass
class DeviceDataParams:
    """
    Dataclass to hold device data metadata

    Assumption: the oscilloscope has 4 channels
    """

    # Unit under test number (e.g. UUT3, UUT3MOD2)
    uut: str = field(default="")
    # Board (e.g. P1000-001-1A1)
    board_name: str = field(default="")
    # PIC firmware version
    pic_firmware: str = field(default="")
    # Number of repetitions per span (e.g. 1, 5, 100)
    nreps: int = field(default=1)
    # Tester name
    tester: str = field(default="")
    # Test date
    test_date: datetime.date = field(default=datetime.date.today())
    # Test timestamp
    test_timestamp: datetime.datetime = field(default=datetime.datetime.now())
    # Test equipment details
    scope_name: str = field(default="")
    scope_serial: str = field(default="")
    arb_name: str = field(default="")
    arb_serial: str = field(default="")
    thp: str = field(default="")
    thp_serial: str = field(default="")
    # Test protocol
    test_protocol: str = field(default="")
    # Python git repository info
    git_hash: str = field(default="")
    git_branch: str = field(default="")
    git_is_dirty: bool = field(default=False)
    # Coaxial cable set (e.g. red)
    cable_set: str = field(default="")
    # Receive probe type ('TPP1000' or 'TAP2500')
    probe: str = field(default="")
    # Receive probe set (e.g. 'red' or 'blue')
    probe_set: str = field(default="")
    # Receive probe tip (spring, claw, pincer, none or other)
    tip: str = field(default="")
    # Transmit probe type ('TPP1000' or 'TAP2500')
    probe_t: str = field(default="")
    # Transmit probe set (e.g. 'red' or 'blue')
    probe_set_t: str = field(default="")
    # Transmit probe tip (spring, claw, pincer, none or other)
    tip_t: str = field(default="")
    # Phantom (e.g. 'Air','PC3A_and_QC3A' (Bottom or LHS material named first))
    phantom: str = field(default="")
    material: str = field(default="")
    # Phantom 1 orientation (e.g. 0, 90, 45 or other)(Bottom or LHS material)
    phantom_orientation: str = field(default="")
    # Phantom 1 placement ('T1', 'T2', 'T3', 'flat', 'upright', etc.)
    # (Bottom or LHS material)
    phantom_placement: str = field(default="")
    # Relative humidity
    rel_humidity: float = field(default=None)
    # Room temperature
    temperature: float = field(default=None)
    # Barometric pressure
    pressure: float = field(default=None)
    # Signal input parameters
    # [Rise time (ns), Fall time (ns), Hold time (us), Period (us)]
    input_params: np.ndarray = field(default_factory=lambda: np.empty(1))
    # Transmit Electrode
    transmit: int = field(default=1)
    # Receive Electrode
    receive: int = field(default=1)

    # Oscilloscope signal parameters
    osc_model: str = field(default="")
    osc_serial: str = field(default="")
    osc_mode: str = field(default="")
    osc_record: int = field(default=None)
    osc_horizontal_scale: float = field(default=None)
    osc_sample_rate: float = field(default=None)

    osc_ch_bandwidth: List[float] = field(
        default_factory=lambda: list(np.zeros(4))
    )
    osc_ch_mode: List[float] = field(default_factory=lambda: list(np.zeros(4)))
    osc_ch_offset: List[float] = field(
        default_factory=lambda: list(np.zeros(4))
    )
    osc_ch_pos: List[float] = field(default_factory=lambda: list(np.zeros(4)))
    osc_ch_term: List[float] = field(default_factory=lambda: list(np.zeros(4)))
    osc_ch_vscale: List[float] = field(
        default_factory=lambda: list(np.zeros(4))
    )
    osc_ch_probe_config: List[str] = field(
        default_factory=lambda: list(np.zeros(4))
    )
    osc_ch_probe_id: List[str] = field(
        default_factory=lambda: list(np.zeros(4))
    )
    osc_ch_probe_sn: List[str] = field(
        default_factory=lambda: list(np.zeros(4))
    )

    def __post_init__(self):
        # Type hints for attributes
        self.types = get_type_hints(self)

        # Map of output names to attribute name
        self.params_map: Dict[str, str] = {
            "UUT_ID": "uut",
            "BOARD_ID": "board_name",
            "PIC_FIRMWARE": "pic_firmware",
            "REP_NUM": "nreps",
            "TESTER": "tester",
            "DATE": "test_date",
            "TIMESTAMP": "test_timestamp",
            "SG_MODEL": "arb_name",
            "SG_SN": "arb_serial",
            "THP_MODEL": "thp",
            "THP_SN": "thp_serial",
            "TEST_PROTOCOL": "test_protocol",
            "PYTHON_GIT_SHA": "git_hash",
            "PYTHON_GIT_BRANCH": "git_branch",
            "PYTHON_GIT_IS_DIRTY": "git_is_dirty",
            "INPUT_PARAM": "input_params",
            "CABLE_SET": "cable_set",
            "PROBE": "probe",
            "PROBE_SET": "probe_set",
            "PROBE_TIP": "tip",
            "T_PROBE": "probe_t",
            "T_PROBE_SET": "probe_set_t",
            "T_PROBE_TIP": "tip_t",
            "PHANTOM": "phantom",
            "MATERIAL": "material",
            "PHANTOM_OR": "phantom_orientation",
            "PHANTOM_OR2": "phantom_placement",
            "RHUMIDITY": "rel_humidity",
            "TEMPERATURE": "temperature",
            "BARO_PRESSURE": "pressure",
            "TRANSMIT_POINT": "transmit",
            "RECEIVE_POINT": "receive",
            "OSC_MODEL": "osc_model",
            "OSC_SN": "osc_serial",
            "OSC_MODE": "osc_mode",
            "OSC_RECORD": "osc_record",
            "OSC_HSCALE": "osc_horizontal_scale",
            "OSC_SAMPLE_RATE": "osc_sample_rate",
        }

    @classmethod
    def read_hdf_metadata(cls, data: Dict) -> "DeviceDataParams":
        """
        Read HDF attributes dictionary, while converting the attribute names
        to class attributes
        """
        params = DeviceDataParams()
        for k, v in data.items():
            found = re.search(r"OSC_(.+)_CH(\d)", k)
            if found:
                pat, i = found.groups((1, 2))
                _key = f"osc_ch_{pat.lower()}"
                try:
                    # Try to convert the value to a float.
                    getattr(params, _key)[int(i) - 1] = float(v.strip())
                except Exception:
                    # If not possible, then set as str
                    getattr(params, _key)[int(i) - 1] = v.strip()
            else:
                if k in params.params_map.keys():
                    attr = params.params_map[k]
                    if params.types[attr] == np.ndarray:
                        attr_val = np.array(v)
                    else:
                        if params.types[attr] == str:
                            attr_val = v.strip()
                        elif params.types[attr] in [int, float, bool]:
                            attr_val = (
                                params.types[attr](v) if v != "" else None
                            )
                        elif params.types[attr] in [
                            datetime.date,
                            datetime.datetime,
                        ]:
                            attr_val = params.types[attr].fromisoformat(v)

                    setattr(params, attr, attr_val)

        return params

    def __eq__(self, other: "DeviceDataParams") -> bool:
        try:
            np.testing.assert_equal(self.to_dict(), other.to_dict())
        except AssertionError:
            return False
        return True

    def to_json(self, fpath: Union[str, os.PathLike]):
        """Create json file with serialised self and return the json string"""
        with open(fpath, "w") as file:
            json.dump(
                self.to_dict(),
                file,
                cls=CustomJsonEncoder,
                sort_keys=True,
                indent=4,
            )

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_json(
        cls, jsonfile: Union[str, os.PathLike]
    ) -> "DeviceDataParams":
        """Read existing json file and deserialise into object"""
        if os.path.isfile(jsonfile):
            with open(jsonfile, "r") as file:
                jsondata = json.load(file, cls=CustomJsonDecoder)
                return DeviceDataParams.from_dict(jsondata)
        else:
            raise FileNotFoundError(f"File {jsonfile} could not be found")

    @classmethod
    def from_dict(cls, dict: Dict) -> "DeviceDataParams":
        return DeviceDataParams(**dict)
