import os

import proofread_eng_scifi.proof_00 as proof

filename_00 = os.path.join(
    os.path.dirname(__file__), "resources", "frankenstein_00.txt"
)


def test_proof_file():
    result = proof.proof_file(filename_00)

    print(result)
    assert result == "checked"


def test_proof_text():
    with open(filename_00, "rt") as f:
        body = f.read()
        result = proof.proof_text(body)

    print(result)
    assert result == "checked"
