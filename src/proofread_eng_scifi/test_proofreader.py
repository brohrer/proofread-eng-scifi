import pytest
from proofread_eng_scifi.data_registry import registry as data_registry
from proofread_eng_scifi.models.fomm.fomm import (
    registry as model_registry,
)
from proofread_eng_scifi.proofreader import BaseProofreader, registry

data_corpus = data_registry["100"]
error_threshold = 0.0005
model = model_registry["03"]


@pytest.fixture
def proofreader():
    proofreader_instance = BaseProofreader(
        model=model,
        error_threshold=error_threshold,
    )
    return proofreader_instance


def test_proof_file(proofreader):
    data_path = data_corpus.get_filepaths_list()[0]

    errors, metrics = proofreader.proof_file(data_path)

    assert isinstance(errors, list)
    assert len(errors) > 3
    assert isinstance(errors[0], dict)
    assert isinstance(errors[1]["first_char"], int)
    assert isinstance(errors[1]["last_char"], int)
    assert isinstance(errors[1]["error_text"], str)
    assert errors[2]["first_char"] <= errors[2]["last_char"]


def test_proof_text(proofreader):
    body = next(data_corpus.get_text_files())
    errors, metrics = proofreader.proof_text(body)

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
        errors, metrics = proofreader.proof_file(data_path)

        assert isinstance(errors, list)
        assert len(errors) > 3
        assert isinstance(errors[0], dict)
        assert isinstance(errors[1]["first_char"], int)
        assert isinstance(errors[1]["last_char"], int)
        assert isinstance(errors[1]["error_text"], str)
        assert errors[2]["first_char"] <= errors[2]["last_char"]
