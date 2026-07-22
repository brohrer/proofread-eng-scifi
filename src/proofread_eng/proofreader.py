"""
A base proofreader that uses a next-token-prediction model to identify
very unlikely next tokens, anomalies, and flags these as potential errors.

Must be supplied with an error threshold and a model which has
- a `calculate_likelihoods_from_ids(List[Int]) -> List[Float]` method
- a `tokenizer_name`
"""

import numpy as np
from proofread_eng.models.fomm.fomm import registry as fomm_registry
from proofread_eng.models.random.random import registry as random_registry
from proofread_eng.models.somm.somm import registry as somm_registry


class BaseProofreader:
    def __init__(
        self,
        version=None,
        model=None,
        error_threshold=None,
        verbose=True,
    ):
        self.version = version
        self.model = model
        self.error_threshold = error_threshold
        self.verbose = verbose

    def proof_file(self, filename):
        with open(filename, "rt") as f:
            body = f.read()
        return self.proof_text(body)

    def proof_text(self, body):
        # Pass the text through a tokenizer
        body_ids = self.model.tokenizer.encode_as_ids(body)
        body_pieces = self.model.tokenizer.encode_as_pieces(body)

        # calculate character start and stop indices for each piece
        lengths = [len(piece) for piece in body_pieces]
        piece_stops = np.cumsum(lengths)
        piece_starts = [
            stop - length for (stop, length) in zip(piece_stops, lengths)
        ]

        # Identify unlikely tokens
        likelihoods = self.model.calculate_likelihoods_from_ids(body_ids)

        # show all probabilities and transitions
        debug = False
        if debug:
            for i_piece, body_piece in enumerate(body_pieces[:-1]):
                likelihood = likelihoods[i_piece]
                print(
                    f"{int(likelihood * 1e6)}: "
                    + f"{body_piece} - {body_pieces[i_piece + 1]}"
                )

        # The least expected tokens are errors.
        error_detections = [
            likelihood < self.error_threshold for likelihood in likelihoods
        ]

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

        metrics = self.calculate_metrics(body, errors)

        # Report the indices and text associated with each error.
        if self.verbose:
            self.report_errors_to_console(errors)
            self.report_metrics_to_console(metrics)

        return errors, metrics

    def calculate_metrics(self, body, errors):
        metrics = {
            "error_count": len(errors),
            "errors_per_kchar": 1000 * len(errors) / len(body),
        }
        return metrics

    def report_errors_to_console(self, errors):
        print()
        print("-------------------------------------------------------------")
        print("Errors detected")
        for error in errors:
            print(
                f'  "{error["error_text"]}"  at position {error["first_char"]}'
            )

    def report_metrics_to_console(self, metrics):
        print()
        print(f"Total of {metrics['error_count']} errors found,")
        print(
            f"which is {metrics['errors_per_kchar']} errors per 1,000 characters"
        )
        print()

    def delete(self):
        self.model.delete()


registry = {
    "01": BaseProofreader(
        model=random_registry["00"],
        error_threshold=0.05,
    ),
    # "02": BaseProofreader(
    #     model=fomm_registry["00"],
    #     error_threshold=0.0005,
    # ),
    # "03": BaseProofreader(
    #     model=somm_registry["00"],
    #     error_threshold=0.0005,
    # ),
    # "04": BaseProofreader(
    #     model=fomm_registry["01"],
    #     error_threshold=0.0005,
    # ),
    # "05": BaseProofreader(
    #     model=somm_registry["01"],
    #     error_threshold=0.0005,
    # ),
    # "06": BaseProofreader(
    #     model=somm_registry["02"],
    #     error_threshold=0.0005,
    # ),
    # "07": BaseProofreader(
    #     model=fomm_registry["02"],
    #     error_threshold=0.0005,
    # ),
    # "08": BaseProofreader(
    #     model=somm_registry["03"],
    #     error_threshold=1e-8,
    # ),
    # "09": BaseProofreader(
    #     model=somm_registry["04"],
    #     error_threshold=1e-8,
    # ),
    # "10": BaseProofreader(
    #     model=somm_registry["05"],
    #     error_threshold=1e-8,
    # ),
    # "11": BaseProofreader(
    #     model=fomm_registry["03"],
    #     error_threshold=0.0005,
    # ),
    # "12": BaseProofreader(
    #     model=somm_registry["06"],
    #     error_threshold=1e-8,
    # ),
    # "13": BaseProofreader(
    #     model=somm_registry["07"],
    #     error_threshold=1e-8,
    # ),
    # "14": BaseProofreader(
    #     model=somm_registry["08"],
    #     error_threshold=1e-8,
    # ),
    # "15": BaseProofreader(
    #     model=somm_registry["09"],
    #     error_threshold=1e-5,
    # ),
    # "16": BaseProofreader(
    #     model=somm_registry["10"],
    #     error_threshold=1e-8,
    # ),
    # "17": BaseProofreader(
    #     model=somm_registry["11"],
    #     error_threshold=1e-8,
    # ),
    # "18": BaseProofreader(
    #     model=somm_registry["12"],
    #     error_threshold=1e-5,
    # ),
    # "19": BaseProofreader(
    #     model=fomm_registry["04"],
    #     error_threshold=1e-8,
    # ),
    "20": BaseProofreader(
        model=fomm_registry["05"],
        error_threshold=1e-8,
    ),
    # "21": BaseProofreader(
    #     model=fomm_registry["06"],
    #     error_threshold=1e-8,
    # ),
    # "22": BaseProofreader(
    #     model=fomm_registry["07"],
    #     error_threshold=1e-8,
    # ),
    # "23": BaseProofreader(
    #     model=fomm_registry["07"],
    #     error_threshold=1e-6,
    # ),
    # "24": BaseProofreader(
    #     model=fomm_registry["07"],
    #     error_threshold=1e-4,
    # ),
    # "25": BaseProofreader(
    #     model=fomm_registry["07"],
    #     error_threshold=1e-3,
    # ),
    # "26": BaseProofreader(
    #     model=fomm_registry["07"],
    #     error_threshold=1e-2,
    # ),
    # "27": BaseProofreader(
    #     model=fomm_registry["07"],
    #     error_threshold=1e-7,
    # ),
    # "28": BaseProofreader(
    #     model=somm_registry["13"],
    #     error_threshold=1e-5,
    # ),
    # "29": BaseProofreader(
    #     model=somm_registry["14"],
    #     error_threshold=1e-5,
    # ),
    # "30": BaseProofreader(
    #     model=somm_registry["15"],
    #     error_threshold=1e-5,
    # ),
    "31": BaseProofreader(
        model=somm_registry["16"],
        error_threshold=1e-5,
    ),
    "32": BaseProofreader(
        model=somm_registry["17"],
        error_threshold=1e-5,
    ),
    "33": BaseProofreader(
        model=somm_registry["18"],
        error_threshold=1e-5,
    ),
    "34": BaseProofreader(
        model=somm_registry["19"],
        error_threshold=1e-5,
    ),
    "35": BaseProofreader(
        model=somm_registry["19"],
        error_threshold=1e-8,
    ),
    "36": BaseProofreader(
        model=somm_registry["19"],
        error_threshold=1e-7,
    ),
    "37": BaseProofreader(
        model=somm_registry["19"],
        error_threshold=1e-6,
    ),
    "38": BaseProofreader(
        model=somm_registry["19"],
        error_threshold=1e-4,
    ),
    "39": BaseProofreader(
        model=somm_registry["19"],
        error_threshold=1e-3,
    ),
    "40": BaseProofreader(
        model=somm_registry["19"],
        error_threshold=1e-2,
    ),
    "41": BaseProofreader(
        model=somm_registry["20"],
        error_threshold=1e-6,
    ),
    "42": BaseProofreader(
        model=somm_registry["21"],
        error_threshold=1e-4,
    ),
    "43": BaseProofreader(
        model=somm_registry["22"],
        error_threshold=1e-4,
    ),
    "44": BaseProofreader(
        model=somm_registry["23"],
        error_threshold=1e-4,
    ),
    # "45": BaseProofreader(
    #     model=somm_registry["24"],
    #     error_threshold=1e-4,
    # ),
    # "46": BaseProofreader(
    #     model=somm_registry["25"],
    #     error_threshold=1e-4,
    # ),
    "47": BaseProofreader(
        model=somm_registry["21"],
        error_threshold=1e-8,
    ),
    "48": BaseProofreader(
        model=somm_registry["21"],
        error_threshold=1e-7,
    ),
    "49": BaseProofreader(
        model=somm_registry["21"],
        error_threshold=1e-6,
    ),
    "50": BaseProofreader(
        model=somm_registry["21"],
        error_threshold=1e-5,
    ),
    "51": BaseProofreader(
        model=somm_registry["21"],
        error_threshold=1e-3,
    ),
    "52": BaseProofreader(
        model=somm_registry["21"],
        error_threshold=1e-2,
    ),
    "53": BaseProofreader(
        model=somm_registry["26"],
        error_threshold=1e-4,
    ),
    "54": BaseProofreader(
        model=somm_registry["27"],
        error_threshold=1e-4,
    ),
    "55": BaseProofreader(
        model=somm_registry["28"],
        error_threshold=1e-4,
    ),
    "56": BaseProofreader(
        model=somm_registry["29"],
        error_threshold=1e-4,
    ),
    "57": BaseProofreader(
        model=somm_registry["30"],
        error_threshold=1e-4,
    ),
    "58": BaseProofreader(
        model=somm_registry["31"],
        error_threshold=1e-4,
    ),
    "59": BaseProofreader(
        model=somm_registry["32"],
        error_threshold=1e-4,
    ),
    "60": BaseProofreader(
        model=fomm_registry["05"],
        error_threshold=1e-4,
    ),
    "61": BaseProofreader(
        model=fomm_registry["08"],
        error_threshold=1e-4,
    ),
    "62": BaseProofreader(
        model=fomm_registry["09"],
        error_threshold=1e-4,
    ),
    "63": BaseProofreader(
        model=fomm_registry["10"],
        error_threshold=1e-4,
    ),
    "64": BaseProofreader(
        model=fomm_registry["11"],
        error_threshold=1e-4,
    ),
    "65": BaseProofreader(
        model=fomm_registry["12"],
        error_threshold=1e-4,
    ),
    "66": BaseProofreader(
        model=fomm_registry["13"],
        error_threshold=1e-4,
    ),
    # "67": BaseProofreader(
    #     model=fomm_registry["14"],
    #     error_threshold=1e-4,
    # ),
}
