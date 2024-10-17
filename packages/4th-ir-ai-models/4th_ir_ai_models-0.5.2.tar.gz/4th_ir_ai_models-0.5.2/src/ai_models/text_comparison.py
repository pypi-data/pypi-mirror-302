from enum import Enum


class TextComparisonModel(str, Enum):
    """Defines AI Models that can be used"""

    all_minilm = "https://text-comparison-minilm.calmflower-186525cd.switzerlandnorth.azurecontainerapps.io"
    all_mpnet_base = "https://text-comparison-mpnet.calmflower-186525cd.switzerlandnorth.azurecontainerapps.io"
