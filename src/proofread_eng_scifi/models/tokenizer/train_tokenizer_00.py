"""
These are the initialization options that are specific to `tokenizer_00`
"""

import os
from proofread_eng_scifi.models.tokenizer.tokenizer_tools import (
    train as train_tokenizer,
)

model_prefix = os.path.join(
    os.path.dirname(__file__), "model_versions", "tokenizer_00"
)

train_tokenizer(
    model_prefix=model_prefix,
    model_type="unigram",
    normalization_rule_name="identity",
    remove_extra_whitespaces=False,
    split_by_whitespace=False,
    vocab_size=20000,
)
