import os
import numpy as np
import pytest
from proofread_eng_scifi.models.fomm.fomm_dev import FirstOrderMarkovModel
from proofread_eng_scifi.models.tokenizer.tokenizer_tools import (
    load as load_tokenizer,
)

tokenizer_name = "tokenizer_00"
test_text_filename = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "..",
    "..",
    "data",
    "evaluation",
    "frankenstein.txt",
)


@pytest.fixture
def test_text():
    with open(test_text_filename, "rt") as f:
        body = f.read()
    return body[:20000]


@pytest.fixture
def tokenizer():
    tokenizer_instance = load_tokenizer(tokenizer_name)
    return tokenizer_instance


@pytest.fixture
def model(tokenizer):
    n_unique_tokens = tokenizer.get_piece_size()
    fomm_instance = FirstOrderMarkovModel(n_unique_tokens=n_unique_tokens)
    return fomm_instance


def test_fomm_creation(model):
    assert isinstance(model.n_unique_tokens, int)
    assert model.n_unique_tokens > 0

    n_rows, n_cols = model.transition_probabilities.shape
    assert n_rows == model.n_unique_tokens
    assert n_cols == model.n_unique_tokens

    assert 0.0 <= model.transition_probability_floor <= 1.0


def test_fomm_training(model, test_text, tokenizer):
    ids = tokenizer.encode_as_ids(test_text)
    model.train(ids)

    assert np.sum(model.transition_counts) >= len(ids) - 1
    assert 0.0 < np.mean(model.transition_probabilities) < 1.0

    assert model.transition_counts[ids[1], ids[2]] >= 1
    assert model.transition_probabilities[ids[3], ids[4]] > 0.0

    assert (
        model.calculate_likelihoods(ids[5:7])[0]
        == model.transition_probabilities[ids[5], ids[6]]
    )
    assert (
        np.min(model.calculate_likelihoods(ids[22:122]))
        >= model.transition_probability_floor
    )
