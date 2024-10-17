# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""Module for different utility operations regarding files and file access"""
import logging
import os
import shutil
import zipfile
from pathlib import Path
from typing import Dict, List

import cv2
import numpy as np

logger = logging.getLogger(__name__)


def get_file_list(
    input_dir: str,
    search_subfolders: bool = False,
    file_extension: str = "",
    include_pattern: str = "",
    exclude_pattern: str = "",
) -> List[str]:
    """
    Create a list of all files found in input_dir. When search_subfolders = True, the list
    contains all files from the input_dir and all its subfolders. The file_extension argument
    can be set to filter for file-types like ".jpg" or ".xml".

    Args:
        input_dir: String, the directory to get the files from
        search_subfolders: Bool, whether to search in subfolders
        file_extension: String, extension of file-paths as string. e.g. ".jpg", ".xml", ".png"
        include_pattern: String, which has to be contained in a file-path
        exclude_pattern: String, which are not allowed to be contained in a file-path

    Returns: List of strings, the list of the files as strings with the complete path

    """

    file_list: List[str] = []

    if not os.path.isdir(input_dir):
        logger.warning("'{}' is not a directory".format(input_dir))
        return file_list

    if search_subfolders:
        path_generator = Path(input_dir).glob(f"**/*{file_extension}")
    else:
        path_generator = Path(input_dir).glob(f"*{file_extension}")

    file_list = [str(p) for p in path_generator]

    if include_pattern != "":
        file_list = [f for f in file_list if include_pattern in f]

    if exclude_pattern:
        file_list = [f for f in file_list if exclude_pattern not in f]

    logger.info(
        "Found '%s' files in path '%s' for files of type '%s'",
        len(file_list),
        input_dir,
        file_extension,
    )

    return file_list


def get_image_file_dict(input_dir: str, image_format: str) -> Dict[str, str]:
    """
    Create a dictionary that contains all file paths of the given image format
    that are present in the input directory, including its subfolders. By separating
    the image format with "|" one can specify multiple image formats, for example
    ".png|.jpg|.jpeg".

    Args:
        input_dir: The directory to get the files from
        image_format: The format of the image files

    Returns:

    """
    input_image_types = image_format.split("|")

    input_image_paths: List[str] = []
    for input_image_type in input_image_types:
        input_image_paths.extend(
            get_file_list(
                input_dir=input_dir,
                search_subfolders=True,
                file_extension=input_image_type,
            )
        )

    return {os.path.basename(p): p for p in input_image_paths}


def ensure_dir(file_path: str, verbose: bool = False) -> None:
    """
    Creates directories for this file-path if they do not exist.
    Does nothing for existing parts of path.

    Args:
        file_path: String, the complete path that is to be checked
        verbose: Bool, whether or not to print infos

    Returns: None

    """

    directory = os.path.dirname(file_path)

    if verbose:
        if not os.path.exists(directory) and len(directory) > 0:
            logger.warning("Create new directory: '%s' for '%s'", directory, file_path)

    os.makedirs(directory, exist_ok=True)


def encoding_safe_imwrite(filename: str, image: np.ndarray) -> None:  # type: ignore[type-arg]
    """
    Saves (Writes) an encoded version of the given image at the given path.
    Args:
        filename: String, name of file
        image: Numpy array, image to be saved

    Returns: None

    """
    # TODO: Consider giving the (mandatory!) filetype separately to avoid having to split here
    file_type = os.path.splitext(filename)[1]
    assert file_type[0] == "."
    _, im_buf_arr = cv2.imencode(file_type, image)
    im_buf_arr.tofile(filename)


def encoding_safe_imread(filename: str) -> np.ndarray:  # type: ignore[type-arg]
    """
    Reads a image file from the given path by decoding buffered image information
    Args:
        filename: String, name of file

    Returns: Numpy array, the image at given path

    """
    image: np.ndarray = cv2.imdecode(  # type: ignore[type-arg]
        np.fromfile(filename, dtype=np.uint8), cv2.IMREAD_UNCHANGED
    )
    return image


def extract_zip_data(zip_path: str, zip_extract_dir: str, remove_existing: bool = True) -> None:
    """
    Extract the content of a zip file to a directory

    Args:
        zip_path: The path to the zip file that should be extracted
        zip_extract_dir: The path to the directory where the content should be extracted to
        remove_existing: Whether to overwrite existing data

    Returns:
        None
    """

    if os.path.isdir(zip_extract_dir):
        if remove_existing:
            logger.debug("Remove existing zip data at '%s'" % zip_extract_dir)
            shutil.rmtree(zip_extract_dir)
        else:
            logger.info("Data is already extracted, skip ...")
            return

    logger.info(f"Extract data from {zip_path} to {zip_extract_dir}")

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(zip_extract_dir)


def get_basename(file_path: str) -> str:
    """
    Get the raw basename of the given file path

    Args:
        file_path: The file from which to determine the raw basename

    Returns:
        The raw basename of the given input file_path
    """

    return os.path.splitext(os.path.basename(file_path))[0]
