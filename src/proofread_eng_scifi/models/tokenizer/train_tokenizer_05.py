"""
These are the initialization options that are specific to `tokenizer_00`

Run with
    uv run test_tokenizer_00.py
"""

import os
from proofread_eng_scifi.models.tokenizer.tokenizer import train

model_name = "tokenizer_05"
data_rel_path = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "..", "data", "training_02"
)

train(
    data_rel_path=data_rel_path,
    model_name=model_name,
    model_type="unigram",
    normalization_rule_name="identity",
    remove_extra_whitespaces=False,
    split_by_whitespace=False,
    vocab_size=20000,
)
