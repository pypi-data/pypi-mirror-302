from enum import Enum


class TextTranslateModel(str, Enum):
    """Defines AI Models that can be used"""

    # only works english -> another language
    Transformers = "https://text-translation-transformers.blackdune-63837cff.switzerlandnorth.azurecontainerapps.io"


class Language(Enum):
    English = "English"
    French = "French"
    Romanian = "Romanian"
    German = "German"
