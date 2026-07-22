import os
import pytest
import time
import numpy as np
from proofread_eng_scifi.data_registry import registry as data_registry
from proofread_eng_scifi.models.fomm.fomm import (
    registry,
    SparseFirstOrderMarkovModel,
)
from proofread_eng_scifi.models.tokenizer.tokenizer import (
    registry as tokenizer_registry,
)

test_version = f"temp_model_{int(time.time())}"
corpus_version = "100"
tokenizer_version = "00"
fomm_id_for_retrieval = "11"


@pytest.fixture
def test_text():
    corpus = data_registry[corpus_version]
    body = list(corpus.get_text_files())[0]
    return body[:20000]


@pytest.fixture
def sparse_model():
    fomm = SparseFirstOrderMarkovModel(
        version=test_version,
        corpus_versions=[corpus_version],
        tokenizer_version=tokenizer_version,
    )

    yield fomm

    try:
        os.remove(fomm.model_path)
    except FileNotFoundError:
        pass


def test_sparse_fomm_creation(sparse_model, test_text):
    sparse_model.train()

    assert 0.0 <= sparse_model.transition_probability_floor <= 1.0
    assert isinstance(sparse_model.bigram_counts, dict)
    assert isinstance(sparse_model.unigram_counts, dict)

    likelihoods = sparse_model.calculate_likelihoods(test_text)
    assert len(likelihoods) > 100


def test_sparse_fomm_training_from_tokens(sparse_model, test_text):
    tokenizer = tokenizer_registry[tokenizer_version]
    ids = tokenizer.encode_as_ids(test_text)
    sparse_model._initialize()
    sparse_model.ready = True
    sparse_model._train_from_tokens(ids)

    bigram_key = list(sparse_model.bigram_counts.keys())[0]
    bigram_value = list(sparse_model.bigram_counts.values())[0]
    unigram_key = list(sparse_model.unigram_counts.keys())[0]
    unigram_value = list(sparse_model.unigram_counts.values())[0]
    assert isinstance(bigram_key, tuple)
    assert isinstance(bigram_key[0], int)
    assert isinstance(bigram_value, int)
    assert isinstance(unigram_key, tuple)
    assert isinstance(unigram_key[0], int)
    assert isinstance(unigram_value, int)

    assert len(sparse_model.bigram_counts) >= int(len(ids) / 10)
    assert len(sparse_model.unigram_counts) <= len(sparse_model.bigram_counts)

    test_seq = ids[5:7]
    unigram_key = tuple(test_seq[:1])
    bigram_key = tuple(test_seq)
    unigram_count = sparse_model.unigram_counts.get(
        unigram_key, sparse_model.epsilon
    )
    bigram_count = sparse_model.bigram_counts.get(bigram_key, 0)
    likelihood = (
        bigram_count / unigram_count + sparse_model.transition_probability_floor
    )
    assert sparse_model.calculate_likelihoods_from_ids(ids[5:7])[
        1
    ] == pytest.approx(likelihood)
    assert (
        np.min(sparse_model.calculate_likelihoods_from_ids(ids[22:122]))
        >= sparse_model.transition_probability_floor
    )


def test_registry_retrieval(test_text):
    model = registry[fomm_id_for_retrieval]

    assert model.version == "11"
    assert model.tokenizer_version == "09"
    assert model.corpus_versions[0] == "04"

    tokenizer = tokenizer_registry[tokenizer_version]
    ids = tokenizer.encode_as_ids(test_text)
    likelihoods = model.calculate_likelihoods_from_ids(ids)
    assert len(likelihoods) > 200
    assert max(likelihoods) < 1.01
    assert min(likelihoods) > 0.0


def test_trained_status_of_all_models(test_text):
    print()
    for version, model in registry.items():
        print(f"    verifying model {version}")
        likelihoods = model.calculate_likelihoods(test_text)
        assert len(likelihoods) > 100
        model.delete()
