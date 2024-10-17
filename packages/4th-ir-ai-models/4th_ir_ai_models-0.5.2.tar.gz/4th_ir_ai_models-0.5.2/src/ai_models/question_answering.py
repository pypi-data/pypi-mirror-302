from enum import Enum


class QuestionAnswerModel(str, Enum):
    """Defines AI Models that can be used"""

    # RobertaBaseSquad2 = "https://tqa-roberta-base-squad2.icysmoke-f4846de1.switzerlandnorth.azurecontainerapps.io"
    IntelDynamicTinybert = "https://tqa-intel-dynamic-tinybert.agreeabledune-08a9cefb.switzerlandnorth.azurecontainerapps.io"
    DistilbertBaseCasedDistilledSquad = "https://tqa-distilbert-distilled-squad.blackdune-63837cff.switzerlandnorth.azurecontainerapps.io"
