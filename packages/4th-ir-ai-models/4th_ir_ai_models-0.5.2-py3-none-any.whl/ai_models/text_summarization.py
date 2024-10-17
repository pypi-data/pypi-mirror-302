from enum import Enum


class TextSummarizeModel(str, Enum):
    """Defines AI Models that can be used"""

    bert2bert_small = "https://text-summarization.agreeabledune-08a9cefb.switzerlandnorth.azurecontainerapps.io"
    # google_bigbird_1 = ""
    # fairseq = ""
    # meeting_summary_facebook = ""
    # pegasus = ""
    # t5_headline_generator = ""
    # mt5_multilingual = ""
    # bert_finetuned_cnn = ""
    # bart_large_cnn = ""
    # facebook_bart_large = ""
    # long_t5 = ""
    # base_finetuned_news = ""
