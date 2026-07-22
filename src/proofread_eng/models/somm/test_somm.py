import os
import pytest
import time
import numpy as np
from proofread_eng.data_registry import registry as data_registry
from proofread_eng.models.somm.somm import (
    registry,
    ConstrainedSparseSecondOrderMarkovModel,
)
from proofread_eng.models.tokenizer.tokenizer import (
    registry as tokenizer_registry,
)

test_version = f"temp_model_{int(time.time())}"
corpus_version = "100"
tokenizer_version = "10"
somm_id_for_retrieval = "16"


@pytest.fixture
def test_text():
    corpus = data_registry[corpus_version]
    body = list(corpus.get_text_files())[0]
    return body[:20000]


@pytest.fixture
def sparse_model():
    somm = ConstrainedSparseSecondOrderMarkovModel(
        version=test_version,
        corpus_versions=[corpus_version],
        tokenizer_version=tokenizer_version,
        max_dict_size=int(3e5),
        max_dict_size_after_shrink=int(2e5),
    )

    yield somm

    try:
        os.remove(somm.model_path)
    except FileNotFoundError:
        pass


def test_sparse_somm_creation(sparse_model, test_text):
    assert not sparse_model.is_ready()

    sparse_model.train()

    assert 0.0 <= sparse_model.transition_probability_floor <= 1.0
    assert isinstance(sparse_model.trigram_counts, dict)
    assert isinstance(sparse_model.bigram_counts, dict)

    likelihoods = sparse_model.calculate_likelihoods(test_text)
    assert len(likelihoods) > 100


def test_sparse_somm_training_from_tokens(sparse_model, test_text):
    tokenizer = tokenizer_registry[tokenizer_version]
    ids = tokenizer.encode_as_ids(test_text)
    sparse_model._initialize()
    sparse_model._train_from_tokens(ids)

    assert sparse_model.is_ready()

    trigram_key = list(sparse_model.trigram_counts.keys())[0]
    trigram_value = list(sparse_model.trigram_counts.values())[0]
    bigram_key = list(sparse_model.bigram_counts.keys())[0]
    bigram_value = list(sparse_model.bigram_counts.values())[0]
    assert isinstance(trigram_key, tuple)
    assert isinstance(trigram_key[0], int)
    assert isinstance(trigram_value, int)
    assert isinstance(bigram_key, tuple)
    assert isinstance(bigram_key[0], int)
    assert isinstance(bigram_value, int)

    assert len(sparse_model.trigram_counts) >= int(len(ids) / 10)
    assert len(sparse_model.bigram_counts) <= len(sparse_model.trigram_counts)

    test_seq = ids[7:10]
    trigram_key = tuple(test_seq)
    bigram_key = tuple(test_seq[:2])
    bigram_count = sparse_model.bigram_counts.get(
        bigram_key, sparse_model.epsilon
    )
    trigram_count = sparse_model.trigram_counts.get(trigram_key, 0)
    likelihood = (
        trigram_count / bigram_count + sparse_model.transition_probability_floor
    )
    assert sparse_model.calculate_likelihoods_from_ids(ids[7:10])[
        2
    ] == pytest.approx(likelihood)

    assert (
        np.min(sparse_model.calculate_likelihoods_from_ids(ids[22:122]))
        >= sparse_model.transition_probability_floor
    )


def test_registry_retrieval(test_text):
    model = registry[somm_id_for_retrieval]

    assert model.version == "16"
    assert model.tokenizer_version == "05"
    assert model.corpus_versions[0] == "00"

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
        assert len(likelihoods) > 49
        model.delete()
