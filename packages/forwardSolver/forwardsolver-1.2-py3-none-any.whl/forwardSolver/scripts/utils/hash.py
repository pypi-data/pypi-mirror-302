import hashlib
import json

import git
from git import InvalidGitRepositoryError

from forwardSolver.scripts.utils.json_coder import CustomJsonEncoder


def clean_dictionary(dictionary):
    """
    Clean a dictionary before hashing. Remove None values and ensure
    numbers are treated as floats so 1 == 1.0 == 1.000.
    Args:
        dictionary (dict): The dictionary to be cleaned.
    Returns:
        dict: A new dictionary with integers converted to floats and None values removed.
    """

    output_dict = {}

    for k, v in dictionary.items():

        if v is None:
            continue

        if isinstance(v, int):
            output_dict[k] = float(v)
        elif isinstance(v, dict):
            output_dict[k] = clean_dictionary(v)
        else:
            output_dict[k] = v

    return output_dict


def hash_repo():
    """
    Hash of the last git commit
    Returns:
        str: The hexadecimal SHA-1 hash of the current commit, or "no_repo" if the
             repository is not found.
    Raises:
        InvalidGitRepositoryError: If the directory is not a valid git repository.
    """
    try:
        repo = git.Repo(search_parent_directories=True)
        return repo.head.object.hexsha
    except InvalidGitRepositoryError:
        return "no_repo"


def hash_dictionary(dictionary, version=hash_repo()):
    """
    MD5 hash of a dictionary.
    Returns MD5 hash + version string separated by a full stop.
    Args:
        dictionary (dict): The dictionary to be hashed.
        version (str, optional): A version string to append to the hash. Defaults to the result of `hash_repo()`.
    Returns:
        str: The MD5 hash of the dictionary concatenated with the version string.
    """

    hash_algo = hashlib.md5()
    # We remove keys that have None as their value
    new_dictionary = clean_dictionary(dictionary)

    # We sort keys so permutations still give the same hash. Use NumpyEncoder to serialise ndarrays
    encoded = json.dumps(new_dictionary, sort_keys=True, cls=CustomJsonEncoder).encode()
    hash_algo.update(encoded)

    return hash_algo.hexdigest() + "." + version


def hash_obj(obj, version=hash_repo()):
    """
    MD5 hash of an object. Object must be convertible to str type.
    Returns MD5 hash + version string separated by a full stop.
    Args:
        obj (Any): The object to be hashed. It will be converted to a string before hashing.
        version (str, optional): A version string to append to the hash. Defaults to the result of hash_repo().
    Returns:
        str: The MD5 hash of the object as a hexadecimal string, followed by a period and the version string.
    """

    hash_algo = hashlib.md5()

    hash_algo.update(str(obj).encode())

    return hash_algo.hexdigest() + "." + version
