import os
import pickle
from pathlib import Path

from forwardSolver.scripts.utils.constants import CACHE_DIR
from forwardSolver.scripts.utils.logging import close_logger, get_logger

logger = get_logger(__name__)


def find_cached(hash_string):
    """
    Looks for cached data with the filename hash_string.pickle
    Args:
        hash_string (str): The hash string used to identify the cached file.
    Returns:
        Any: The cached data if the file exists, otherwise None.
    """

    filename = f"{CACHE_DIR}/{hash_string}.pickle"

    if os.path.isfile(filename):

        logger.info(f"{filename} exists. Using cached data.")

        # open a file, where you stored the pickled data
        file = open(filename, "rb")

        # load information from that file
        cached_data = pickle.load(file)

        # close the file
        file.close()

        return cached_data
    else:
        return None


def create_cache(hash_string, obj):
    """
    Creates cached (obj) data with the filename hash_string.pickle
    Args:
        hash_string (str): The hash string to be used as the filename for the cache file.
        obj (Any): The object to be cached.
    Returns:
        None
    """

    filename = f"{CACHE_DIR}/{hash_string}.pickle"
    logger.info(f"Caching data: {filename}.")

    # open a file, where you ant to store the data
    file = open(filename, "wb")

    # dump information to that file
    pickle.dump(obj, file)

    # close the file
    file.close()


def create_cache_subdir(hash_string):
    """
    Creates a subdirectory in the cache directory.
    Returns the path of the newly-created directory.
    Args:
        hash_string (str): The hash string used to name the subdirectory.
    Returns:
        str: The path to the created or existing subdirectory.
    """

    filedir = str(Path(CACHE_DIR, hash_string))
    if not os.path.exists(filedir):
        logger.info(f"Creating cache dir: {filedir}.")
        os.makedirs(filedir)
    return filedir


close_logger(logger)
