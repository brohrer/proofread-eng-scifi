import os
import numpy as np
import pytest
from proofread_eng_scifi.models.somm.somm import SecondOrderMarkovModel
from proofread_eng_scifi.models.tokenizer.tokenizer import (
    load as load_tokenizer,
)

test_model_name = "temp_test_model"
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
tokenizer_name = "tokenizer_04"


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
    somm_instance = SecondOrderMarkovModel(
        n_unique_tokens=n_unique_tokens,
        model_name=test_model_name,
        tokenizer_name=tokenizer_name,
    )
    return somm_instance


def test_somm_creation(model):
    assert isinstance(model.n_unique_tokens, int)
    assert model.n_unique_tokens > 0
    assert model.model_name == test_model_name
    assert model.tokenizer_name == tokenizer_name

    assert 0.0 <= model.transition_probability_floor <= 1.0

    n_d1, n_d2, n_d3 = model.transition_counts.shape
    assert n_d1 == model.n_unique_tokens
    assert n_d2 == model.n_unique_tokens
    assert n_d3 == model.n_unique_tokens

    n_d1, n_d2, n_d3 = model.transition_probabilities.shape
    assert n_d1 == model.n_unique_tokens
    assert n_d2 == model.n_unique_tokens
    assert n_d3 == model.n_unique_tokens

    assert isinstance(model.transition_counts[0][0][0], np.int32)
    assert isinstance(model.transition_probabilities[0][0][0], np.float64)


def test_somm_training_from_tokens(model, test_text, tokenizer):
    ids = tokenizer.encode_as_ids(test_text)
    model.train_from_tokens(ids)

    assert np.sum(model.transition_counts) >= len(ids) - 2
    assert 0.0 < np.mean(model.transition_probabilities) < 1.0

    assert model.transition_counts[ids[1], ids[2], ids[3]] >= 1
    assert model.transition_probabilities[ids[4], ids[5], ids[6]] > 0.0

    assert (
        model.calculate_likelihoods(ids[7:10])[0]
        == model.transition_probabilities[ids[7], ids[8], ids[9]]
    )
    assert (
        np.min(model.calculate_likelihoods(ids[22:122]))
        >= model.transition_probability_floor
    )
