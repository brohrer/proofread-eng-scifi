import os
import pytest
import time
from proofread_eng_scifi.models.tokenizer.tokenizer import (
    load as load_tokenizer,
    train as train_tokenizer,
)

model_name = f"test_tokenizer_{int(time.time())}"
model_type = "unigram"  # "unigram" (default), "bpe"
normalization_rule_name = "identity"  # one of:
remove_extra_whitespaces = False
split_by_whitespace = False
vocab_size = 20000


@pytest.fixture
def tokenizer_fixture():
    train_tokenizer(
        model_name=model_name,
        model_type=model_type,
        normalization_rule_name=normalization_rule_name,
        remove_extra_whitespaces=remove_extra_whitespaces,
        split_by_whitespace=split_by_whitespace,
        vocab_size=vocab_size,
    )

    tokenizer_model = load_tokenizer(model_name)
    yield tokenizer_model

    model_rel_path = os.path.dirname(__file__)
    model_path_prefix = os.path.join(model_rel_path, model_name)
    os.remove(model_path_prefix + ".model")
    os.remove(model_path_prefix + ".vocab")


def test_tokenizer_training(tokenizer_fixture):
    tok = tokenizer_fixture

    # encode: text => id
    test_sentence = "This is a test of the sentencepiece tokenizer."
    test_pieces = tok.encode_as_pieces(test_sentence)
    assert test_pieces[3] == "▁of"
    assert test_pieces[8] == "ize"

    test_ids = tok.encode_as_ids(test_sentence)
    assert test_ids[1] == 16
    assert test_ids[5] == 13026
    assert test_ids[10] == 6

    # decode: id => text
    assert tok.decode_pieces(test_pieces) == test_sentence
    assert tok.decode_ids(test_ids) == test_sentence
