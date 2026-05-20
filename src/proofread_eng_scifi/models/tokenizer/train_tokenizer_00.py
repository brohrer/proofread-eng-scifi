"""
These are the initialization options that are specific to `tokenizer_00`

Run with
    uv run test_tokenizer_00.py
"""

from proofread_eng_scifi.models.tokenizer.tokenizer import train

model_name = "tokenizer_00"

train(
    model_name=model_name,
    model_type="unigram",
    normalization_rule_name="identity",
    remove_extra_whitespaces=False,
    split_by_whitespace=False,
    vocab_size=20000,
)
