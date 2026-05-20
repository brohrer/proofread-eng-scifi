import os
import pytest
import time
import numpy as np
from proofread_eng_scifi.models.fomm.fomm import load
from proofread_eng_scifi.models.fomm.train_fomm_00 import train
from proofread_eng_scifi.models.tokenizer.tokenizer import (
    train as train_tokenizer,
)


@pytest.fixture
def tokenizer_name():
    tokenizer_model_name = f"test_tokenizer_{int(time.time())}"
    model_type = "unigram"  # "unigram" (default), "bpe"
    normalization_rule_name = "identity"  # one of:
    remove_extra_whitespaces = False
    split_by_whitespace = False
    vocab_size = 1000

    train_tokenizer(
        model_name=tokenizer_model_name,
        model_type=model_type,
        normalization_rule_name=normalization_rule_name,
        remove_extra_whitespaces=remove_extra_whitespaces,
        split_by_whitespace=split_by_whitespace,
        vocab_size=vocab_size,
    )

    # tokenizer_model = load_tokenizer(tokenizer_model_name)
    yield tokenizer_model_name

    model_rel_path = os.path.join(os.path.dirname(__file__), "..", "tokenizer")
    model_path_prefix = os.path.join(model_rel_path, tokenizer_model_name)
    os.remove(model_path_prefix + ".model")
    os.remove(model_path_prefix + ".vocab")


def test_fomm_00_training(tokenizer_name):
    fomm_model_name = f"test_fomm_{int(time.time())}"
    train(model_name=fomm_model_name, tokenizer_name=tokenizer_name)
    model = load(model_name=fomm_model_name)

    assert np.sum(model.transition_counts) >= 1546466
    assert 0.0 < np.mean(model.transition_probabilities) < 1.0

    assert model.transition_counts[3, 5] >= 1286
    assert model.transition_probabilities[9, 3] > 0.2

    assert (
        model.calculate_likelihoods([69, 42])[0]
        == model.transition_probabilities[69, 42]
    )
    assert (
        np.min(model.calculate_likelihoods(np.arange(22, 127)))
        >= model.transition_probability_floor
    )

    # Delete the fomm that was created for testing
    os.remove(os.path.join(os.path.dirname(__file__), fomm_model_name + ".pkl"))
