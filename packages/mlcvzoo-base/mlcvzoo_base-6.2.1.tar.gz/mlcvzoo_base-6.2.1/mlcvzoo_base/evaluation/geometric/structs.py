# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

from mlcvzoo_base.configuration.structs import BaseType


class GeometricSizeTypes(BaseType):
    BBOX_ALL: str = "ALL"
    BBOX_SMALL: str = "S"
    BBOX_MEDIUM: str = "M"
    BBOX_LARGE: str = "L"


class MetricTypes(BaseType):
    GROUND_TRUTH: str = "GT"
    TRUE_POSITIVES: str = "TP"
    FALSE_POSITIVES: str = "FP"
    FALSE_NEGATIVES: str = "FN"
    RECALL: str = "RC"
    PRECISION: str = "PR"
    F1: str = "F1"
    AP: str = "AP"
    AVG_TP_IOU: str = "AVG_TP_IOU"
