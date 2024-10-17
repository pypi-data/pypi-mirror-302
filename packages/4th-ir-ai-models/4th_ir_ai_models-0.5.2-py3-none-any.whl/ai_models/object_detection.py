from enum import Enum


class ObjectDetectionModel(str, Enum):
    circularnet = "https://image-obje-detec-circularnet.icysmoke-f4846de1.switzerlandnorth.azurecontainerapps.io"

    efficientdet_d7 = "https://image-object-dec-effi-det.icysmoke-f4846de1.switzerlandnorth.azurecontainerapps.io"

    inception_resnet_v2 = "https://image-object-detect-inception-v2.icysmoke-f4846de1.switzerlandnorth.azurecontainerapps.io"

    resnet152_v1_fpn_640x640 = "https://image-obj-detec-incep-resnet.icysmoke-f4846de1.switzerlandnorth.azurecontainerapps.io"
