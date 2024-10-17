# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""Module for different utility operations regarding annotations in lists"""
import logging
import random
from typing import List, Optional, Tuple

from mlcvzoo_base.api.data.annotation import BaseAnnotation
from mlcvzoo_base.api.data.bounding_box import BoundingBox
from mlcvzoo_base.api.data.box import Box
from mlcvzoo_base.api.data.class_identifier import ClassIdentifier
from mlcvzoo_base.api.data.classification import Classification
from mlcvzoo_base.api.data.dataset_info import BaseDatasetInfo
from mlcvzoo_base.utils.file_utils import ensure_dir

logger = logging.getLogger(__name__)


def create_list_split(
    input_file_list: List[BaseAnnotation],
    split_size: float,
    random_state: Optional[int] = None,
) -> Tuple[List[BaseAnnotation], List[BaseAnnotation]]:
    """
    Splits the given input_file_list into training and evaluation lists.

    Args:
        input_file_list: List of BaseAnnotation objects
        split_size: float, size of split between 0 and 1
        random_state: Optional int, defining the random state for reproducible splits

    Returns: two lists of BaseAnnotation objects for training and evaluation

    """
    # create the split
    if len(input_file_list) < 2:
        raise ValueError("Can't split a list with less than 2 elements")

    file_list = input_file_list.copy()
    rng = random.Random()
    if random_state is not None:
        rng.seed(random_state)

    rng.shuffle(file_list)

    # lists for storing the path of the images
    max_index_eval = max(1, int(len(file_list) * split_size))
    eval_list = file_list[:max_index_eval]
    train_list = file_list[max_index_eval:]

    logger.info(
        "Split: train_size={} ({} images), eval_size={} ({} images)".format(
            str(1.0 - split_size),
            str(len(train_list)),
            str(split_size),
            str(len(eval_list)),
        )
    )

    return train_list, eval_list


def create_cross_val_list_splits(
    input_file_list: List[BaseAnnotation], number_splits: int
) -> List[List[BaseAnnotation]]:
    # TODO: implement or remove

    raise ValueError("create_cross_val_list_splits is not implemented for now!")


def create_annotation_file_from_list(
    csv_entry_list: List[str], dataset_info: BaseDatasetInfo, output_file_path: str
) -> BaseDatasetInfo:
    """
    Creates an annotation file from csv annotations

    Args:
        csv_entry_list: List of strings (csv entries)
        dataset_info: BaseDatasetInfo, basic information about a dataset
        output_file_path: string, defines the path where the file should be stored

    Returns: BaseDatasetInfo, the updated information

    """

    dataset_info.base_file = output_file_path

    ensure_dir(file_path=output_file_path, verbose=True)

    logger.info("Write annotations to file: %s", output_file_path)
    with open(output_file_path, "w", encoding="'utf-8") as file:
        file.writelines(csv_entry_list)

    return dataset_info


def generate_tags_based_on_bounding_boxes(
    annotations: List[BaseAnnotation],
) -> List[BaseAnnotation]:
    """

    Args:
        annotations: List of BaseAnnotations from which tags are derived

    Returns:
        List of BaseAnnotations enriched with Classifications

    """
    class_identifier = ClassIdentifier(class_id=-1, class_name="")
    default_bounding_box = BoundingBox(
        box=Box(0, 0, 0, 0),
        class_identifier=class_identifier,
        model_class_identifier=class_identifier,
        score=0.0,
        difficult=False,
        occluded=False,
        background=False,
        content="",
    )

    for annotation in annotations:
        # TODO:
        #  get biggest bounding box out of
        #  annotation.get_bounding_boxes(include_segmentations=True)

        max_bounding_box: BoundingBox = default_bounding_box
        max_area = 0
        for bounding_box in annotation.get_bounding_boxes(include_segmentations=True):
            width = bounding_box.box().xmax - bounding_box.box().xmin
            height = bounding_box.box().ymax - bounding_box.box().ymin
            area = width * height
            if area > max_area:
                max_bounding_box = bounding_box

        assert not max_bounding_box.__eq__(default_bounding_box)
        classification: Classification = Classification(
            class_identifier=max_bounding_box.class_identifier,
            model_class_identifier=max_bounding_box.model_class_identifier,
            score=1.0,
        )

        annotation.classifications.append(classification)

    return annotations
