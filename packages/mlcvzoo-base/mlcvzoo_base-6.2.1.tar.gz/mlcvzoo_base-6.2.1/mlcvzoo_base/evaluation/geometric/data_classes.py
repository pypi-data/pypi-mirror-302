# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Module for storing data classes and complex type definitions that are used in the context of the
mlcvzoo_base.evaluation.geometric package
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Final, List, NamedTuple, Optional

import numpy as np

from mlcvzoo_base.api.data.annotation import BaseAnnotation
from mlcvzoo_base.api.data.geometric_classifiction import GeometricClassification

# 3D List containing of the following:
#   1) One entry per data items / image
#   2) One entry per call of classes
#   3) One entry per annotation Annotations the matches the image (1) and the class (2)
# This is a list of BaseAnnotations in order to carry information about the image
# instead of just bounding boxes
EVALUATION_LIST_TYPE = List[List[List[BaseAnnotation]]]  # pylint: disable=invalid-name

CONFUSION_MATRIX_TYPE = List[List[int]]
CONFUSION_MATRIX_DICT_TYPE = Dict[str, Dict[str, int]]  # pylint: disable=invalid-name

DEFAULT_INT_VALUE: Final[int] = 0
DEFAULT_FLOAT_VALUE: Final[float] = 0.0


class EvaluationEntry(NamedTuple):
    image_path: str
    evaluation_objects: List[GeometricClassification]


# NOTE: Since this are the main Object Detection metrics, it's okay to have more instance
#       attributes
@dataclass
class GeometricMetrics:  # pylint: disable=too-many-instance-attributes
    """
    Dataclass for storing the main metrics that are computed for object detection algorithms
    """

    # TODO: rename to lower case, disable pylint only temporary!
    TP: int = DEFAULT_INT_VALUE  # pylint: disable=invalid-name
    FP: int = DEFAULT_INT_VALUE  # pylint: disable=invalid-name
    FN: int = DEFAULT_INT_VALUE  # pylint: disable=invalid-name
    PR: float = DEFAULT_FLOAT_VALUE  # pylint: disable=invalid-name
    RC: float = DEFAULT_FLOAT_VALUE  # pylint: disable=invalid-name
    F1: float = DEFAULT_FLOAT_VALUE  # pylint: disable=invalid-name
    AP: float = DEFAULT_FLOAT_VALUE  # pylint: disable=invalid-name
    COUNT: int = DEFAULT_INT_VALUE  # pylint: disable=invalid-name
    AVG_TP_IOU: float = DEFAULT_FLOAT_VALUE  # pylint: disable=invalid-name

    @staticmethod
    def from_dict(input_dict: Dict[str, Any]) -> GeometricMetrics:
        return GeometricMetrics(**input_dict)

    def __repr__(self):  # type: ignore
        return (
            f"TP: {self.TP}, "
            f"FP: {self.FP}, "
            f"FN: {self.FN}, "
            f"PR: {self.PR}, "
            f"RC: {self.RC}, "
            f"F1: {self.F1}, "
            f"AP: {self.AP}, "
            f"COUNT: {self.COUNT}"
            f"AVG_TP_IOU: {self.COUNT}"
        )

    def __str__(self):  # type: ignore
        return self.__repr__()


@dataclass
class MetricImageInfo:
    """
    Dataclass to store information about false positives and false negatives in the
    form of EvaluationEntry objects. It is used to have an exact relation between an image
    and the according false positive / false negative bounding boxes. The ground
    truth data is added to be able to visualize the expected bounding boxes.
    """

    gt_evaluation_entry: Optional[EvaluationEntry] = None
    tp_evaluation_entry: Optional[EvaluationEntry] = None
    fn_evaluation_entry: Optional[EvaluationEntry] = None
    fp_evaluation_entry: Optional[EvaluationEntry] = None
    fn_matched_fp_evaluation_entry: Optional[EvaluationEntry] = None


# 1st key: Class Identifier as string
# 2nd key: Image Path
# 2nd value: The MetricImageInfo for this class name and image path
METRIC_IMAGE_INFO_TYPE = Dict[str, Dict[str, MetricImageInfo]]  # pylint: disable=invalid-name


# 1st key: iou-threshold
# 2nd key: Type of the size of the bounding-box => Any of GeometricSizeTypes.BBOX_SIZE_TYPE
# 3rd key: Class Identifier as string
# value: The computed metrics of type GeometricMetrics
METRIC_DICT_TYPE = Dict[
    float, Dict[str, Dict[str, GeometricMetrics]]
]  # pylint: disable=invalid-name


def build_metric_dict_from_dict(
    input_dict: Dict[str, Dict[str, Dict[str, Dict[str, Any]]]]
) -> METRIC_DICT_TYPE:
    metric_dict: METRIC_DICT_TYPE = {}

    for key_0, value_0 in input_dict.items():
        metric_dict[float(key_0)] = {}
        for key_1, value_1 in value_0.items():
            metric_dict[float(key_0)][key_1] = {}
            for key_2, od_metrics_dict in value_1.items():
                metric_dict[float(key_0)][key_1][key_2] = GeometricMetrics.from_dict(
                    input_dict=od_metrics_dict
                )

    return metric_dict


@dataclass
class GeometricEvaluationMetrics:
    """
    Dataclass for storing the output of an object detection evaluation.
    The metrics_dict stores the actual computed metrics, while the metrics_image_info_dict
    stores debugging information to be able to analyze false positives and false negatives.

    The model_specifier indicates for which model the metrics have been computed.
    """

    model_specifier: str
    metrics_dict: METRIC_DICT_TYPE = field(default_factory=lambda: {})
    metrics_image_info_dict: METRIC_IMAGE_INFO_TYPE = field(default_factory=lambda: {})


@dataclass
class GeometricEvaluationComputingData:
    """
    Dataclass for storing data structures that are needed to computed object detection metrics
    """

    # 1st key: Type of the size of the bounding-box => Any of GeometricSizeTypes.BBOX_SIZE_TYPE
    # 2nd key: Class Identifier as string
    # value: The number of ground truth boxes for the combination of keys
    gt_counter_dict: Dict[str, Dict[str, int]] = field(default_factory=lambda: {})

    # 1st key: iou-threshold
    # 2nd key: Type of the size of the bounding-box => Any of GeometricSizeTypes.BBOX_SIZE_TYPE
    # Cumulative array indicating the false positives of the dataset
    false_positives_dict: Dict[float, Dict[str, np.ndarray]] = field(  # type: ignore[type-arg]
        default_factory=lambda: {}
    )

    # 1st key: iou-threshold
    # 2nd key: Type of the size of the bounding-box => Any of GeometricSizeTypes.BBOX_SIZE_TYPE
    # Cumulative array indicating the true positives of the dataset
    true_positives_dict: Dict[float, Dict[str, np.ndarray]] = field(  # type: ignore[type-arg]
        default_factory=lambda: {}
    )

    # 1st key: iou-threshold
    # 2nd key: Type of the size of the bounding-box => Any of GeometricSizeTypes.BBOX_SIZE_TYPE
    # Cumulative array indicating the iou value of an evaluation. This can be used to determine
    # false positives and false negatives, as well as to see the 'real' geometric overlap of
    # an prediction.
    iou_dict: Dict[str, np.ndarray] = field(default_factory=lambda: {})  # type: ignore[type-arg]

    # 1st key: iou-threshold
    # 2nd key: Type of the size of the bounding-box => Any of GeometricSizeTypes.BBOX_SIZE_TYPE
    # value: Array indicating the score for each data item
    scores: Dict[float, Dict[str, np.ndarray]] = field(  # type: ignore[type-arg]
        default_factory=lambda: {}
    )
