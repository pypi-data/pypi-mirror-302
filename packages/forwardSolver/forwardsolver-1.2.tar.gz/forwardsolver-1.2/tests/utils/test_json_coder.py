import copy
import json
from datetime import date, datetime
from pathlib import Path

import numpy as np

from forwardSolver.scripts.utils.json_coder import (
    CustomJsonDecoder,
    CustomJsonEncoder,
)


def test_json_encoder_and_decoder():
    """
    Tests that an object which has been encoded to, and then decoded from, JSON are the same.
    """

    # create a dictionary with different types
    subdict = {
        "nparr": np.array([[1, 0, 3], [2.3, 4.5, 0], [9, 9, 9]]),
        "float": float(1.2),
        "int": int(2),
        "str": str("high"),
        "date_obj": date(2022, 12, 25),
        "datetime_obj": datetime(2022, 12, 25, 9, 50, 23),
        "path": Path("some", "arbitrary", "path"),
    }
    # check that nesting works
    fulldict = copy.deepcopy(subdict)
    fulldict["dict"] = copy.deepcopy(subdict)

    # encode dictionary to json string
    string_json = json.dumps(fulldict, cls=CustomJsonEncoder, indent=1)

    # decode json string back into dictionary
    decoded_fulldict = json.loads(string_json, cls=CustomJsonDecoder)

    # assert that the two objects are equal
    np.testing.assert_equal(decoded_fulldict, fulldict)
