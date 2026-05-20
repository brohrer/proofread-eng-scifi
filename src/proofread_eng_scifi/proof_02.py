"""
Use a first order Markov model to predict errors
"""

import sys
import numpy as np
import proofread_eng_scifi.models.fomm.fomm as lm
from proofread_eng_scifi.models.tokenizer.tokenizer_tools import (
    load as load_tokenizer,
)
from proofread_eng_scifi.models.fomm.fomm import load as load_fomm

fomm_name = "fomm_00"


def proof_file(filename):
    with open(filename, "rt") as f:
        body = f.read()
    return proof_text(body)


def proof_text(body):
    lm = load_fomm(fomm_name)
    tokenizer = load_tokenizer(lm.tokenizer_name)

    # Pass the text through a tokenizer
    body_ids = tokenizer.encode_as_ids(body)
    likelihoods = lm.calculate_likelihoods(body_ids)

    body_pieces = tokenizer.encode_as_pieces(body)
    # calculate character start and stop indices for each piece
    lengths = [len(piece) for piece in body_pieces]
    piece_stops = np.cumsum(lengths)
    piece_starts = [
        stop - length for (stop, length) in zip(piece_stops, lengths)
    ]

    # The top 5% least expected tokens are errors.
    error_detections = [likelihood < 0.05 for likelihood in likelihoods]

    # Pull out starts and stops for errors
    errors = []
    for i_piece, error_detected in enumerate(error_detections):
        if error_detected:
            errors.append(
                {
                    "first_char": int(piece_starts[i_piece]),
                    "last_char": int(piece_stops[i_piece] - 1),
                    "error_text": body_pieces[i_piece],
                }
            )

    metrics = calculate_metrics(body, errors)

    # Report the indices and text associated with each error.
    report_errors_to_console(errors)
    report_metrics_to_console(metrics)

    return errors, metrics


def calculate_metrics(body, errors):
    metrics = {
        "error_count": len(errors),
        "errors_per_kchar": 1000 * len(errors) / len(body),
    }
    return metrics


def report_errors_to_console(errors):
    print()
    print("-------------------------------------------------------------")
    print("Errors detected")
    for error in errors:
        print(f'  "{error["error_text"]}"  at position {error["first_char"]}')


def report_metrics_to_console(metrics):
    print()
    print(f"Total of {metrics['error_count']} errors found,")
    print(f"which is {metrics['errors_per_kchar']} errors per 1,000 characters")
    print()


if __name__ == "__main__":
    """
    If a command line argument of "tokenizer" is given,
    train the tokenizer.

    Otherwise assume the argument is a filename and try to proofread it.

    If no arguments are given, show a help message.
    """
    if len(sys.argv) > 1:
        result = proof_file(sys.argv[1])

    else:
        print("""
  Run

      uv run proof_01.py <filename>

  to proofread <filename>.
""")
