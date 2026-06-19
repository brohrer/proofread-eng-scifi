import os
import numpy as np
import pytest
from proofread_eng_scifi.models.fomm.fomm_sparse import (
    SparseFirstOrderMarkovModel,
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
    fomm_instance = SparseFirstOrderMarkovModel(
        n_unique_tokens=n_unique_tokens,
        model_name=test_model_name,
        tokenizer_name=tokenizer_name,
    )
    return fomm_instance


def test_fomm_creation(model):
    assert isinstance(model.n_unique_tokens, int)
    assert model.n_unique_tokens > 0
    assert model.model_name == test_model_name
    assert model.tokenizer_name == tokenizer_name

    assert 0.0 <= model.transition_probability_floor <= 1.0

    assert isinstance(model.unigram_counts, dict)
    assert isinstance(model.bigram_counts, dict)


def test_somm_training_from_tokens(model, test_text, tokenizer):
    ids = tokenizer.encode_as_ids(test_text)
    model.train_from_tokens(ids)

    unigram_key = list(model.unigram_counts.keys())[0]
    unigram_value = list(model.unigram_counts.values())[0]
    bigram_key = list(model.bigram_counts.keys())[0]
    bigram_value = list(model.bigram_counts.values())[0]
    assert isinstance(unigram_key, tuple)
    assert isinstance(unigram_key[0], int)
    assert isinstance(unigram_value, int)
    assert isinstance(bigram_key, tuple)
    assert isinstance(bigram_key[0], int)
    assert isinstance(bigram_value, int)

    assert len(model.unigram_counts) >= int(len(ids) / 10)
    assert len(model.bigram_counts) >= len(model.unigram_counts)

    test_seq = ids[7:9]
    unigram_key = tuple(test_seq[:1])
    bigram_key = tuple(test_seq)
    unigram_count = model.unigram_counts.get(unigram_key, model.epsilon)
    bigram_count = model.bigram_counts.get(bigram_key, 0)
    likelihood = (
        bigram_count / unigram_count + model.transition_probability_floor
    )
    assert model.calculate_likelihoods(ids[7:9])[0] == pytest.approx(likelihood)

    assert (
        np.min(model.calculate_likelihoods(ids[22:122]))
        >= model.transition_probability_floor
    )
