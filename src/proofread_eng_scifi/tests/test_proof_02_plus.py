import os

import proofread_eng_scifi.proof_02 as proof_02
import proofread_eng_scifi.proof_03 as proof_03
import proofread_eng_scifi.proof_04 as proof_04
import proofread_eng_scifi.proof_05 as proof_05
import proofread_eng_scifi.proof_06 as proof_06
import proofread_eng_scifi.proof_07 as proof_07
import proofread_eng_scifi.proof_08 as proof_08

filename_00 = os.path.join(
    os.path.dirname(__file__), "resources", "frankenstein_00.txt"
)

proofreaders = [
    proof_02,
    proof_03,
    proof_04,
    proof_05,
    proof_06,
    proof_07,
    proof_08,
]


def test_proof_file():
    for proofreader in proofreaders:
        print(f"    proofing file with {proofreader.MODEL_NAME}")
        errors, metrics = proofreader.proof_file(filename_00, verbose=False)

        assert isinstance(errors, list)
        assert len(errors) > 3
        assert isinstance(errors[0], dict)
        assert isinstance(errors[1]["first_char"], int)
        assert isinstance(errors[1]["last_char"], int)
        assert isinstance(errors[1]["error_text"], str)
        assert errors[2]["first_char"] <= errors[2]["last_char"]


def test_proof_text():
    for proofreader in proofreaders:
        print(f"    proofing text with {proofreader.MODEL_NAME}")
        with open(filename_00, "rt") as f:
            body = f.read()
            errors, metrics = proofreader.proof_text(body, verbose=False)

        assert isinstance(errors, list)
        assert len(errors) > 3
        assert isinstance(errors[0], dict)
        assert isinstance(errors[1]["first_char"], int)
        assert isinstance(errors[1]["last_char"], int)
        assert isinstance(errors[1]["error_text"], str)
        assert errors[2]["first_char"] <= errors[2]["last_char"]
