import os
import pytest
import time
from proofread_eng_scifi.models.markov_base import MarkovBase


test_version = f"temp_model_{int(time.time())}"
corpus_version = "100"
tokenizer_version = "00"


@pytest.fixture
def model():
    markov_base_model = MarkovBase(
        version=test_version,
        corpus_versions=[corpus_version],
        tokenizer_version=tokenizer_version,
    )

    yield markov_base_model

    os.remove(markov_base_model.model_path)


def test_fomm_creation(model):
    assert isinstance(model.n_unique_tokens, int)
    assert model.n_unique_tokens > 0
    assert model.version == test_version
    assert model.tokenizer_version == tokenizer_version

    model.train()
    assert 0.0 <= model.transition_probability_floor <= 1.0
