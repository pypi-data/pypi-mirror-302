from enum import Enum


class NamedEntityRecognitionModel(str, Enum):
    """Defines AI Models that can be used"""

    spacy = "https://text-named-er-spacy.icysmoke-f4846de1.switzerlandnorth.azurecontainerapps.io"
    # flair = ""
    # flair_2 = ""
    # bert_1 = ""
    # en_bert_nvidia = ""
    # bert_finedtuned = ""
    # biomedical_ner_all = ""
    # bent_pub = ""
    # flair_ner_multi = ""
    # ner_english_ontonotes_large = ""
    # spacy_ner = ""
