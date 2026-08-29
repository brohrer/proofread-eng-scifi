import pytest

from proofread_eng.data.eval.registry import registry as data_registry
from proofread_eng.models.fomm.fomm import (
    registry as model_registry,
)
from proofread_eng.proofreader import BaseProofreader, registry

data_corpus = data_registry["100"]
beta_value = 2
error_threshold = 0.0005
model = model_registry["05"]


@pytest.fixture
def proofreader():
    proofreader_instance = BaseProofreader(
        model=model,
        error_threshold=error_threshold,
    )
    return proofreader_instance


@pytest.fixture
def proofreader_conservative():
    proofreader_instance = BaseProofreader(
        model=model,
        beta=beta_value,
        error_threshold=error_threshold,
    )
    return proofreader_instance


def test_proof_file(proofreader):
    data_path = data_corpus.get_filepaths_list()[0]

    errors, _ = proofreader.proof_file(data_path)

    assert isinstance(errors, list)
    assert len(errors) > 3
    assert isinstance(errors[0], dict)
    assert isinstance(errors[1]["first_char"], int)
    assert isinstance(errors[1]["last_char"], int)
    assert isinstance(errors[1]["error_text"], str)
    assert errors[2]["first_char"] <= errors[2]["last_char"]


def test_proof_text(proofreader):
    body = next(data_corpus.get_text_files())
    errors, _ = proofreader.proof_text(body)

    assert isinstance(errors, list)
    assert len(errors) > 3
    assert isinstance(errors[0], dict)
    assert isinstance(errors[1]["first_char"], int)
    assert isinstance(errors[1]["last_char"], int)
    assert isinstance(errors[1]["error_text"], str)
    assert errors[2]["first_char"] <= errors[2]["last_char"]


def test_proof_text_conservative(proofreader_conservative):
    body = next(data_corpus.get_text_files())
    errors, _ = proofreader_conservative.proof_text(body)

    assert isinstance(errors, list)
    assert len(errors) > 3
    assert isinstance(errors[0], dict)
    assert isinstance(errors[1]["first_char"], int)
    assert isinstance(errors[1]["last_char"], int)
    assert isinstance(errors[1]["error_text"], str)
    assert errors[2]["first_char"] <= errors[2]["last_char"]


def test_check_proofreaders():
    data_path = data_corpus.get_filepaths_list()[0]
    for version, proofreader in registry.items():
        print(f"    proofing file with {version}")
        errors, _ = proofreader.proof_file(data_path)

        assert isinstance(errors, list)
        assert len(errors) > 3
        assert isinstance(errors[0], dict)
        assert isinstance(errors[1]["first_char"], int)
        assert isinstance(errors[1]["last_char"], int)
        assert isinstance(errors[1]["error_text"], str)
        assert errors[2]["first_char"] <= errors[2]["last_char"]

        try:
            proofreader.delete()
        except AttributeError:
            # If the model doesn't have a delete method, don't panic.
            pass
