import os
import numpy as np
import pytest
from proofread_eng_scifi.models.somm.somm_sparse import (
    SparseSecondOrderMarkovModel,
)
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
tokenizer_name = "tokenizer_00"


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
    somm_instance = SparseSecondOrderMarkovModel(
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

    assert isinstance(model.bigram_counts, dict)
    assert isinstance(model.trigram_counts, dict)


def test_somm_training_from_tokens(model, test_text, tokenizer):
    ids = tokenizer.encode_as_ids(test_text)
    model.train_from_tokens(ids)

    bigram_key = list(model.bigram_counts.keys())[0]
    bigram_value = list(model.bigram_counts.values())[0]
    trigram_key = list(model.trigram_counts.keys())[0]
    trigram_value = list(model.trigram_counts.values())[0]
    assert isinstance(bigram_key, tuple)
    assert isinstance(bigram_key[0], int)
    assert isinstance(bigram_value, int)
    assert isinstance(trigram_key, tuple)
    assert isinstance(trigram_key[0], int)
    assert isinstance(trigram_value, int)

    assert len(model.bigram_counts) >= int(len(ids) / 10)
    assert len(model.trigram_counts) >= len(model.bigram_counts)

    test_seq = ids[7:10]
    bigram_key = tuple(test_seq[:2])
    trigram_key = tuple(test_seq)
    bigram_count = model.bigram_counts.get(bigram_key, model.epsilon)
    trigram_count = model.trigram_counts.get(trigram_key, 0)
    likelihood = (
        trigram_count / bigram_count + model.transition_probability_floor
    )
    assert model.calculate_likelihoods(ids[7:10])[0] == pytest.approx(likelihood)

    assert (
        np.min(model.calculate_likelihoods(ids[22:122]))
        >= model.transition_probability_floor
    )
