import datetime
import os

import h5py
import numpy as np
import pytest

from forwardSolver.scripts.utils.device_data.device_data import DeviceDataParams
from forwardSolver.tests.device_data.test_device_data import print_datasets


@pytest.mark.usefixtures("hdf_file")
def test_read_device_data_metadata_from_hdf_file(hdf_file):
    """
    Test that an HDF dataset's metadata is correctly read
    and stored as an DeviceDataParams object
    """
    # 0. Instantiate dataset
    hdf = h5py.File(hdf_file, "r")
    dataset: h5py.Dataset = hdf[
        print_datasets(hdf, filter_strings=["PulseResponse"])[0]
    ]
    # 1. Instantiate DeviceDataParams from dataset
    metadata = DeviceDataParams.read_hdf_metadata(dataset.attrs)

    # 2. Compare the two
    #    We need to do some processing because the data out of the HDF will be strings
    #    whereas the DeviceDataParams has more adequate types
    for k, v in metadata.params_map.items():
        obj_attr = getattr(metadata, v)

        dat_attr = dataset.attrs[k]
        if metadata.types[v] == np.ndarray:
            attr_val = np.array(dat_attr)
        else:
            if metadata.types[v] == str:
                attr_val = dat_attr.strip()
            elif metadata.types[v] in [int, float, bool]:
                attr_val = metadata.types[v](dat_attr) if dat_attr != "" else None
            elif metadata.types[v] in [datetime.date, datetime.datetime]:
                attr_val = metadata.types[v].fromisoformat(dat_attr)
            else:
                raise AttributeError(f"Unknown attribute {v}")

        if type(obj_attr) == np.ndarray:
            np.testing.assert_array_equal(obj_attr, attr_val)
        else:
            np.testing.assert_equal(obj_attr, attr_val)

    hdf.close()


@pytest.mark.usefixtures("hdf_file")
def test_device_data_metadata_json_IO(hdf_file, tmp_path_factory):
    """
    Test the input/output to JSON file by creating a json file in the testing directory,
    loading it and comparing the two
    """
    # Instantiate dataset
    hdf = h5py.File(hdf_file, "r")
    dataset: h5py.Dataset = hdf[
        print_datasets(hdf, filter_strings=["PulseResponse"])[0]
    ]

    # Initialise the signal from HDF
    metadata = DeviceDataParams.read_hdf_metadata(dataset.attrs)

    # Output to JSON
    jsonpath = tmp_path_factory.mktemp("data") / "metadata.json"
    if os.path.isfile(jsonpath):
        os.remove(jsonpath)

    metadata.to_json(jsonpath)

    # Assert that the file was created
    np.testing.assert_(os.path.isfile(jsonpath))

    # Read json file
    metadata_read = DeviceDataParams.from_json(jsonfile=jsonpath)

    for k, v in metadata.types.items():
        if v == np.ndarray:
            np.testing.assert_array_equal(
                getattr(metadata, k), getattr(metadata_read, k)
            )
        else:
            np.testing.assert_equal(getattr(metadata, k), getattr(metadata_read, k))

    hdf.close()
