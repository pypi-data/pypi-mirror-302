# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""Module for building BaseAnnotation objects"""

from abc import ABC, abstractmethod
from typing import List

from mlcvzoo_base.api.data.annotation import BaseAnnotation
from mlcvzoo_base.api.data.box import Box


class AnnotationBuilder(ABC):
    """
    Super class for defining the methods that are needed to build a single
    instance of an BaseAnnotation.
    """

    @staticmethod
    def _check_and_fix_annotation(annotation: BaseAnnotation) -> None:
        wrong_bounding_boxes: List[Box] = []
        for bounding_box in annotation.bounding_boxes:
            # Update bounding boxes with information from the annotation
            bounding_box.ortho_box().clamp(shape=(annotation.get_height(), annotation.get_width()))

            if not annotation.is_valid_bounding_box(box=bounding_box.ortho_box()):
                wrong_bounding_boxes.append(bounding_box.ortho_box())

        if wrong_bounding_boxes:
            raise ValueError(
                f"Annotation invalid \n"
                f"Wrong boxes: {wrong_bounding_boxes}\n"
                f"Annotation:\n{annotation}"
            )

        wrong_bounding_boxes = []
        for segmentation in annotation.segmentations:
            # Update bounding boxes with information from the annotation
            segmentation.ortho_box().clamp(shape=(annotation.get_height(), annotation.get_width()))

            if not annotation.is_valid_bounding_box(box=segmentation.ortho_box()):
                wrong_bounding_boxes.append(segmentation.ortho_box())

        if wrong_bounding_boxes:
            raise ValueError(
                f"Annotation invalid \n"
                f"Wrong boxes: {wrong_bounding_boxes}\n"
                f"Annotation:\n{annotation}"
            )

    @abstractmethod
    def build(
        self,
        image_path: str,
        annotation_path: str,
        image_dir: str,
        annotation_dir: str,
        replacement_string: str,
    ) -> BaseAnnotation:
        """
        Builds a BaseAnnotation object utilizing the given parameters

        Args:
            image_path: String, points to an annotated image
            annotation_path: String, points to the respective annotation
            image_dir: String, points to the dir where the annotated image is stored
            annotation_dir: String, points to the dir where the respective annotation is stored
            replacement_string: String, part of the paths that is a placeholder

        Returns:
            A BaseAnnotation object
        """

        raise NotImplementedError()
