from enum import Enum


class ImageClassificationModel(str, Enum):
    """Defines AI Models that can be used"""

    clip_vit_base_patch32 = "https://image-class-openai-clip-vit.agreeabledune-08a9cefb.switzerlandnorth.azurecontainerapps.io"
    document_finetuned_rvlcdip = "https://image-c-document-finetuned.agreeabledune-08a9cefb.switzerlandnorth.azurecontainerapps.io"
    efficientnet_b1 = "https://image-class-efficientnet.blackdune-63837cff.switzerlandnorth.azurecontainerapps.io"


class AgeClassificationModel(str, Enum):
    google_vit_base = "https://image-vit-age-classifier.icysmoke-f4846de1.switzerlandnorth.azurecontainerapps.io"
