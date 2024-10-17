from enum import Enum


class TextClassifyModel(Enum):
    """Defines AI Models that can be used"""

    bart_large_mnli = "https://text-classification-bart-large.icysmoke-f4846de1.switzerlandnorth.azurecontainerapps.io"
    bart = "https://text-classification-bart.agreeabledune-08a9cefb.switzerlandnorth.azurecontainerapps.io"
    disbart_mnli_12_1 = "https://text-classification-disbart-mnli.calmground-e921d537.switzerlandnorth.azurecontainerapps.io"
