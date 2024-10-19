import json
from datetime import date, datetime
from pathlib import Path

import numpy as np

from forwardSolver.scripts.utils.device_data.models.noise_data import (
    MeanData,
    NoiseData,
)


class CustomJsonEncoder(json.JSONEncoder):
    """
    JSON encoder which includes support for numpy types
    Methods:
        default(obj):
            Overrides the default method to provide custom serialization for specific
            data types.
            Args:
                obj: The object to serialize.
            Returns:
                A JSON-serializable representation of the object.
            Supported types:
                - np.integer: Converts to int.
                - np.floating: Converts to float.
                - np.ndarray: Converts to a list with a key "np.ndarray".
                - NoiseData: Converts to a dictionary with a key "type.NoiseData".
                - MeanData: Converts to a dictionary with a key "type.MeanData".
                - datetime: Converts to ISO format string with a key "datetime".
                - date: Converts to ISO format string with a key "date".
                - Path: Converts to string with a key "PosixPath".
    """

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return {"np.ndarray": obj.tolist()}
        elif isinstance(obj, NoiseData):
            return {"type.NoiseData": obj.to_dict()}
        elif isinstance(obj, MeanData):
            return {"type.MeanData": obj.to_dict()}
        # The order of datetime, date is important because an object of type
        # datetime is also of type date.
        # However, for decoding, we need to keep these separate
        elif isinstance(obj, datetime):
            return {"datetime": obj.isoformat()}
        elif isinstance(obj, date):
            return {"date": obj.isoformat()}
        elif isinstance(obj, Path):
            return {"PosixPath": str(obj)}
        return json.JSONEncoder.default(self, obj)


class CustomJsonDecoder(json.JSONDecoder):
    """
    JSON decoder which includes support for numpy types
    This decoder can handle the following custom types:
    - np.ndarray: Converts JSON objects with the key "np.ndarray" to numpy arrays.
    - type.NoiseData: Converts JSON objects with the key "type.NoiseData" to NoiseData instances.
    - type.MeanData: Converts JSON objects with the key "type.MeanData" to MeanData instances.
    - date: Converts JSON objects with the key "date" to date objects.
    - datetime: Converts JSON objects with the key "datetime" to datetime objects.
    - PosixPath: Converts JSON objects with the key "PosixPath" to Path objects.
    Methods:
    - __init__(*args, **kwargs): Initializes the CustomJsonDecoder with the provided arguments.
    - object_hook(obj): Custom object hook method to decode specific object types.
    """

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if isinstance(obj, dict):
            if "np.ndarray" in obj:
                return np.asarray(obj["np.ndarray"])
            elif "type.NoiseData" in obj:
                return NoiseData(**obj["type.NoiseData"])
            elif "type.MeanData" in obj:
                return MeanData(**obj["type.MeanData"])
            elif "date" in obj:
                return date.fromisoformat(obj["date"])
            elif "datetime" in obj:
                return datetime.fromisoformat(obj["datetime"])
            elif "PosixPath" in obj:
                return Path(obj["PosixPath"])
        return obj
