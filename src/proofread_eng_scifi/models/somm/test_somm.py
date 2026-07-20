import os
import pytest
import time
import numpy as np
from proofread_eng_scifi.data_registry import registry as data_registry
from proofread_eng_scifi.models.somm.somm import (
    DBSecondOrderMarkovModel,
    registry,
    SecondOrderMarkovModel,
    SparseSecondOrderMarkovModel,
)
from proofread_eng_scifi.models.tokenizer.tokenizer import (
    registry as tokenizer_registry,
)

test_version = f"temp_model_{int(time.time())}"
corpus_version = "100"
tokenizer_version = "10"
somm_id_for_retrieval = "02"


@pytest.fixture
def test_text():
    corpus = data_registry[corpus_version]
    body = list(corpus.get_text_files())[0]
    return body[:20000]


@pytest.fixture
def model():
    somm = SecondOrderMarkovModel(
        version=test_version,
        corpus_versions=[corpus_version],
        tokenizer_version=tokenizer_version,
    )

    yield somm

    try:
        os.remove(somm.model_path)
    except FileNotFoundError:
        pass


@pytest.fixture
def sparse_model():
    somm = SparseSecondOrderMarkovModel(
        version=test_version,
        corpus_versions=[corpus_version],
        tokenizer_version=tokenizer_version,
    )

    yield somm

    try:
        os.remove(somm.model_path)
    except FileNotFoundError:
        pass


@pytest.fixture
def db_model():
    somm = DBSecondOrderMarkovModel(
        version=test_version,
        corpus_versions=[corpus_version],
        tokenizer_version=tokenizer_version,
    )

    yield somm

    somm.close()
    try:
        os.remove(somm.db_name)
    except FileNotFoundError:
        pass


def test_somm_creation(model, test_text):
    model.train()

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

    likelihoods = model.calculate_likelihoods(test_text)
    assert len(likelihoods) > 100


def test_somm_training_from_tokens(model, test_text):
    assert not model.is_ready()

    tokenizer = tokenizer_registry[tokenizer_version]
    ids = tokenizer.encode_as_ids(test_text)
    model._initialize()
    model._train_from_tokens(ids)

    assert model.is_ready()

    assert np.sum(model.transition_counts) >= len(ids) - 2
    assert 0.0 < np.mean(model.transition_probabilities) < 1.0

    assert model.transition_counts[ids[1], ids[2], ids[3]] >= 1
    assert model.transition_probabilities[ids[4], ids[5], ids[6]] > 0.0

    assert (
        model.calculate_likelihoods_from_ids(ids[7:10])[2]
        == model.transition_probabilities[ids[7], ids[8], ids[9]]
    )
    assert (
        np.min(model.calculate_likelihoods_from_ids(ids[22:122]))
        >= model.transition_probability_floor
    )


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


def test_db_somm_creation(db_model, test_text):

    assert db_model.connection is None
    assert db_model.cursor is None
    assert db_model.bigram_table_name == "bigrams"
    assert db_model.trigram_table_name == "trigrams"
    assert not db_model.is_ready()


def test_db_somm_initialization(db_model, test_text):
    assert not db_model.is_ready()
    assert not db_model._both_tables_exist()

    db_model._initialize()
    assert db_model._both_tables_exist()

    db_model.cursor.execute(f"""
        SELECT COUNT(*) FROM {db_model.bigram_table_name}
    """)
    assert db_model.cursor.fetchall()[0][0] == 0
    db_model.cursor.execute(f"""
        SELECT COUNT(*) FROM {db_model.trigram_table_name}
    """)
    assert db_model.cursor.fetchall()[0][0] == 0

    db_model.cursor.execute(f"""
        SELECT * FROM PRAGMA_TABLE_INFO('{db_model.bigram_table_name}')
    """)
    table_info = db_model.cursor.fetchall()

    assert table_info[0][1] == "tokenid1"
    assert table_info[0][2] == "INTEGER"
    assert table_info[1][1] == "tokenid2"
    assert table_info[2][1] == "count"

    db_model.cursor.execute(f"""
        SELECT * FROM PRAGMA_TABLE_INFO('{db_model.trigram_table_name}')
    """)
    table_info = db_model.cursor.fetchall()

    assert table_info[0][1] == "tokenid1"
    assert table_info[1][1] == "tokenid2"
    assert table_info[1][2] == "INTEGER"
    assert table_info[2][1] == "tokenid3"
    assert table_info[3][1] == "count"

    assert not db_model.is_ready()


def test_db_somm_training(db_model, test_text):
    db_model.train()

    assert db_model.connection is not None
    assert db_model.cursor is not None
    assert db_model.is_ready()

    likelihoods = db_model.calculate_likelihoods(test_text)
    assert len(likelihoods) > 100


def test_db_somm_calc_triggers_training(db_model, test_text):
    assert db_model.connection is None
    assert db_model.cursor is None
    assert not db_model._both_tables_exist()
    assert not db_model.is_ready()

    likelihoods = db_model.calculate_likelihoods(test_text)
    assert len(likelihoods) > 100

    assert db_model.connection is not None
    assert db_model.cursor is not None
    assert db_model._both_tables_exist()
    assert db_model.is_ready()


def test_registry_retrieval(test_text):
    model = registry[somm_id_for_retrieval]

    assert model.version == "02"
    assert model.tokenizer_version == "00"
    assert model.corpus_versions[1] == "01"

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
