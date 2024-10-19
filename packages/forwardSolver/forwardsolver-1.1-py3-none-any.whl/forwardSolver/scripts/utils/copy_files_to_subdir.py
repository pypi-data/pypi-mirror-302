import glob
import os
import shutil


def copy_files_to_subdir(src, dest, ext):
    """
    Copy all files that end in .`ext` from `src` to `dest`.
    Args:
        src (str): The source directory path.
        dest (str): The destination directory path.
        ext (str): The file extension to filter by (e.g., 'txt' for text files).
    Returns:
        None
    """

    files = glob.iglob(os.path.join(src, f"*.{ext}"))
    for file in files:
        if os.path.isfile(file):
            shutil.copy2(file, dest)
