import os

import proofread_eng_scifi.proof_01 as proof

filename_00 = os.path.join(
    os.path.dirname(__file__), "resources", "frankenstein_00.txt"
)


def test_proof_file():
    errors, metrics = proof.proof_file(filename_00)

    print(errors)
    print(metrics)
    assert isinstance(errors, list)
    assert len(errors) > 3
    assert isinstance(errors[0], dict)
    assert isinstance(errors[1]["first_char"], int)
    assert isinstance(errors[1]["last_char"], int)
    assert isinstance(errors[1]["error_text"], str)
    assert errors[2]["first_char"] <= errors[2]["last_char"]


def test_proof_text():
    with open(filename_00, "rt") as f:
        body = f.read()
        errors, metrics = proof.proof_text(body)

    print(errors)
    print(metrics)
    assert isinstance(errors, list)
    assert len(errors) > 3
    assert isinstance(errors[0], dict)
    assert isinstance(errors[1]["first_char"], int)
    assert isinstance(errors[1]["last_char"], int)
    assert isinstance(errors[1]["error_text"], str)
    assert errors[2]["first_char"] <= errors[2]["last_char"]
