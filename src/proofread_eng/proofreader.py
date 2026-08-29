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

# from proofread_eng.models.somm.somm import registry as somm_registry


class ProofreaderCore:
    def __init__(
        self,
        version=None,
        alpha=None,
        beta=None,
        error_threshold=None,
        verbose=True,
    ):
        self.version = version
        self.alpha = alpha
        self.beta = beta
        self.error_threshold = error_threshold
        self.verbose = verbose

    def proof_file(self, filename):
        with open(filename, "rt") as f:
            body = f.read()
        return self.proof_text(body)

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


class BaseProofreader(ProofreaderCore):
    def __init__(self, model=None, **kwargs):
        super().__init__(**kwargs)
        self.model = model

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
        likelihoods = self.model.calculate_likelihoods_from_ids(
            body_ids, self.alpha, self.beta
        )

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

    def delete(self):
        self.model.delete()


class BaseMultimodelProofreader(ProofreaderCore):
    """
    A proofreader that uses an ensemble of models.

    All models must use the same tokenizer.
    """

    def __init__(self, model=None, combination_method=None, **kwargs):
        super().__init__(**kwargs)
        self.models = model
        self.combination_method = combination_method

        # Check that there is a list of models provided and
        # that they all have the same tokenizer.
        assert isinstance(self.models, list)
        assert len(self.models) > 1
        for m in self.models[1:]:
            assert self.models[0].tokenizer_version == m.tokenizer_version

        self.tokenizer = self.models[0].tokenizer

        valid_combination_methods = [
            "min",
            "max",
            "mean",
            "geometric_mean",
        ]
        assert self.combination_method in valid_combination_methods, (
            "combination_method must be either "
            + "min, max, mean, or geometric_mean"
        )

    def proof_text(self, body):
        # Pass the text through a tokenizer
        body_ids = self.tokenizer.encode_as_ids(body)
        body_pieces = self.tokenizer.encode_as_pieces(body)

        # calculate character start and stop indices for each piece
        lengths = [len(piece) for piece in body_pieces]
        piece_stops = np.cumsum(lengths)
        piece_starts = [
            stop - length for (stop, length) in zip(piece_stops, lengths)
        ]

        # Identify unlikely tokens
        all_likelihoods = []
        for model in self.models:
            all_likelihoods.append(
                model.calculate_likelihoods_from_ids(
                    body_ids, self.alpha, self.beta
                )
            )

        all_likelihoods = np.array(all_likelihoods)
        # combine them
        if self.combination_method == "max":
            likelihoods = np.max(all_likelihoods, axis=0)
        elif self.combination_method == "min":
            likelihoods = np.min(all_likelihoods, axis=0)
        elif self.combination_method == "mean":
            likelihoods = np.mean(all_likelihoods, axis=0)
        elif self.combination_method == "geometric_mean":
            likelihoods = np.exp(np.mean(np.log(all_likelihoods), axis=0))
        else:
            raise ValueError

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

    def delete(self):
        for model in self.models:
            model.delete()


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
    "24": BaseProofreader(
        model=fomm_registry["07"],
        error_threshold=1e-4,
    ),
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
    # "31": BaseProofreader(
    #     model=somm_registry["16"],
    #     error_threshold=1e-5,
    # ),
    # "32": BaseProofreader(
    #     model=somm_registry["17"],
    #     error_threshold=1e-5,
    # ),
    # "33": BaseProofreader(
    #     model=somm_registry["18"],
    #     error_threshold=1e-5,
    # ),
    # "34": BaseProofreader(
    #     model=somm_registry["19"],
    #     error_threshold=1e-5,
    # ),
    # "35": BaseProofreader(
    #     model=somm_registry["19"],
    #     error_threshold=1e-8,
    # ),
    # "36": BaseProofreader(
    #     model=somm_registry["19"],
    #     error_threshold=1e-7,
    # ),
    # "37": BaseProofreader(
    #     model=somm_registry["19"],
    #     error_threshold=1e-6,
    # ),
    # "38": BaseProofreader(
    #     model=somm_registry["19"],
    #     error_threshold=1e-4,
    # ),
    # "39": BaseProofreader(
    #     model=somm_registry["19"],
    #     error_threshold=1e-3,
    # ),
    # "40": BaseProofreader(
    #     model=somm_registry["19"],
    #     error_threshold=1e-2,
    # ),
    # "41": BaseProofreader(
    #     model=somm_registry["20"],
    #     error_threshold=1e-6,
    # ),
    # "42": BaseProofreader(
    #     model=somm_registry["21"],
    #     error_threshold=1e-4,
    # ),
    # "43": BaseProofreader(
    #     model=somm_registry["22"],
    #     error_threshold=1e-4,
    # ),
    # "44": BaseProofreader(
    #     model=somm_registry["23"],
    #     error_threshold=1e-4,
    # ),
    # "45": BaseProofreader(
    #     model=somm_registry["24"],
    #     error_threshold=1e-4,
    # ),
    # "46": BaseProofreader(
    #     model=somm_registry["25"],
    #     error_threshold=1e-4,
    # ),
    # "47": BaseProofreader(
    #     model=somm_registry["21"],
    #     error_threshold=1e-8,
    # ),
    # "48": BaseProofreader(
    #     model=somm_registry["21"],
    #     error_threshold=1e-7,
    # ),
    # "49": BaseProofreader(
    #     model=somm_registry["21"],
    #     error_threshold=1e-6,
    # ),
    # "50": BaseProofreader(
    #     model=somm_registry["21"],
    #     error_threshold=1e-5,
    # ),
    # "51": BaseProofreader(
    #     model=somm_registry["21"],
    #     error_threshold=1e-3,
    # ),
    # "52": BaseProofreader(
    #     model=somm_registry["21"],
    #     error_threshold=1e-2,
    # ),
    # "53": BaseProofreader(
    #    model=somm_registry["26"],
    #     error_threshold=1e-4,
    # ),
    # "54": BaseProofreader(
    #     model=somm_registry["27"],
    #     error_threshold=1e-4,
    # ),
    # "55": BaseProofreader(
    #     model=somm_registry["28"],
    #     error_threshold=1e-4,
    # ),
    # "56": BaseProofreader(
    #     model=somm_registry["29"],
    #     error_threshold=1e-4,
    # ),
    # "57": BaseProofreader(
    #     model=somm_registry["30"],
    #     error_threshold=1e-4,
    # ),
    # "58": BaseProofreader(
    #     model=somm_registry["31"],
    #     error_threshold=1e-4,
    # ),
    # "59": BaseProofreader(
    #     model=somm_registry["32"],
    #     error_threshold=1e-4,
    # ),
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
    "68": BaseProofreader(
        model=fomm_registry["15"],
        error_threshold=1e-4,
    ),
    "69": BaseProofreader(
        model=fomm_registry["16"],
        error_threshold=1e-4,
    ),
    "70": BaseProofreader(
        model=fomm_registry["17"],
        error_threshold=1e-4,
    ),
    "71": BaseProofreader(
        model=fomm_registry["18"],
        error_threshold=1e-4,
    ),
    "72": BaseProofreader(
        model=fomm_registry["19"],
        error_threshold=1e-4,
    ),
    # "73": BaseProofreader(
    #     model=fomm_registry["20"],
    #     error_threshold=1e-4,
    # ),
    "74": BaseProofreader(
        model=fomm_registry["21"],
        error_threshold=1e-4,
    ),
    "75": BaseProofreader(
        model=fomm_registry["22"],
        error_threshold=1e-4,
    ),
    # tokenizer 06
    "76": BaseMultimodelProofreader(
        model=[fomm_registry["08"], fomm_registry["16"]],
        combination_method="min",
        error_threshold=1e-4,
    ),
    # tokenizer 07
    "77": BaseMultimodelProofreader(
        model=[fomm_registry["09"], fomm_registry["17"]],
        combination_method="min",
        error_threshold=1e-4,
    ),
    # tokenizer 08
    "78": BaseMultimodelProofreader(
        model=[fomm_registry["10"], fomm_registry["18"]],
        combination_method="min",
        error_threshold=1e-4,
    ),
    # tokenizer 09
    "79": BaseMultimodelProofreader(
        model=[fomm_registry["11"], fomm_registry["19"]],
        combination_method="min",
        error_threshold=1e-4,
    ),
    # tokenizer 11
    "80": BaseMultimodelProofreader(
        model=[fomm_registry["12"], fomm_registry["21"]],
        combination_method="min",
        error_threshold=1e-4,
    ),
    # tokenizer 12
    "81": BaseMultimodelProofreader(
        model=[fomm_registry["13"], fomm_registry["22"]],
        combination_method="min",
        error_threshold=1e-4,
    ),
    "82": BaseMultimodelProofreader(
        model=[fomm_registry["08"], fomm_registry["16"]],
        combination_method="min",
        error_threshold=1e-7,
    ),
    "83": BaseMultimodelProofreader(
        model=[fomm_registry["08"], fomm_registry["16"]],
        combination_method="min",
        error_threshold=1e-6,
    ),
    "84": BaseMultimodelProofreader(
        model=[fomm_registry["08"], fomm_registry["16"]],
        combination_method="min",
        error_threshold=1e-5,
    ),
    "85": BaseMultimodelProofreader(
        model=[fomm_registry["08"], fomm_registry["16"]],
        combination_method="min",
        error_threshold=1e-3,
    ),
    "86": BaseMultimodelProofreader(
        model=[fomm_registry["08"], fomm_registry["16"]],
        combination_method="min",
        error_threshold=1e-2,
    ),
    # tokenizer 05
    "87": BaseMultimodelProofreader(
        model=[fomm_registry["05"], fomm_registry["15"]],
        combination_method="min",
        error_threshold=1e-4,
    ),
    # All texts
    "88": BaseMultimodelProofreader(
        model=[fomm_registry["07"], fomm_registry["23"]],
        combination_method="min",
        error_threshold=1e-4,
    ),
    "89": BaseProofreader(
        model=fomm_registry["23"],
        error_threshold=1e-4,
    ),
    "90": BaseProofreader(
        model=fomm_registry["23"],
        beta=1,
        error_threshold=1e-4,
    ),
    "91": BaseProofreader(
        model=fomm_registry["23"],
        beta=0.5,
        error_threshold=1e-4,
    ),
    "92": BaseProofreader(
        model=fomm_registry["23"],
        beta=2,
        error_threshold=1e-4,
    ),
    "93": BaseProofreader(
        model=fomm_registry["23"],
        beta=5,
        error_threshold=1e-4,
    ),
    "94": BaseProofreader(
        model=fomm_registry["23"],
        beta=10,
        error_threshold=1e-4,
    ),
    "95": BaseProofreader(
        model=fomm_registry["23"],
        beta=20,
        error_threshold=1e-4,
    ),
    "96": BaseProofreader(
        model=fomm_registry["23"],
        beta=50,
        error_threshold=1e-4,
    ),
    "97": BaseProofreader(
        model=fomm_registry["23"],
        beta=100,
        error_threshold=1e-4,
    ),
    "98": BaseProofreader(
        model=fomm_registry["23"],
        beta=200,
        error_threshold=1e-4,
    ),
    "99": BaseProofreader(
        model=fomm_registry["23"],
        beta=500,
        error_threshold=1e-4,
    ),
    "100": BaseProofreader(
        model=fomm_registry["23"],
        beta=1000,
        error_threshold=1e-4,
    ),
    "101": BaseProofreader(
        model=fomm_registry["23"],
        beta=2000,
        error_threshold=1e-4,
    ),
    "102": BaseProofreader(
        model=fomm_registry["23"],
        beta=3000,
        error_threshold=1e-4,
    ),
    "103": BaseProofreader(
        model=fomm_registry["23"],
        beta=10000,
        error_threshold=1e-4,
    ),
    "104": BaseProofreader(
        model=fomm_registry["23"],
        beta=20000,
        error_threshold=1e-4,
    ),
    "105": BaseProofreader(
        model=fomm_registry["23"],
        beta=50000,
        error_threshold=1e-4,
    ),
    "106": BaseProofreader(
        model=fomm_registry["23"],
        beta=100,
        error_threshold=1e-6,
    ),
    "107": BaseProofreader(
        model=fomm_registry["23"],
        beta=100,
        error_threshold=1e-5,
    ),
    "108": BaseProofreader(
        model=fomm_registry["23"],
        beta=100,
        error_threshold=1e-3,
    ),
    "109": BaseProofreader(
        model=fomm_registry["23"],
        beta=100,
        error_threshold=1e-2,
    ),
    "110": BaseProofreader(
        model=fomm_registry["23"],
        beta=100,
        error_threshold=1e-1,
    ),
    # Explore betas @error_threshold 1e-5
    "111": BaseProofreader(
        model=fomm_registry["23"],
        beta=0.5,
        error_threshold=1e-5,
    ),
    "112": BaseProofreader(
        model=fomm_registry["23"],
        beta=1,
        error_threshold=1e-5,
    ),
    "113": BaseProofreader(
        model=fomm_registry["23"],
        beta=2,
        error_threshold=1e-5,
    ),
    "114": BaseProofreader(
        model=fomm_registry["23"],
        beta=5,
        error_threshold=1e-5,
    ),
    "115": BaseProofreader(
        model=fomm_registry["23"],
        beta=10,
        error_threshold=1e-5,
    ),
    "116": BaseProofreader(
        model=fomm_registry["23"],
        beta=20,
        error_threshold=1e-5,
    ),
    "117": BaseProofreader(
        model=fomm_registry["23"],
        beta=50,
        error_threshold=1e-5,
    ),
    "118": BaseProofreader(
        model=fomm_registry["23"],
        beta=100,
        error_threshold=1e-5,
    ),
    "119": BaseProofreader(
        model=fomm_registry["23"],
        beta=200,
        error_threshold=1e-5,
    ),
    "120": BaseProofreader(
        model=fomm_registry["23"],
        beta=500,
        error_threshold=1e-5,
    ),
    "121": BaseProofreader(
        model=fomm_registry["23"],
        beta=1000,
        error_threshold=1e-5,
    ),
    "122": BaseProofreader(
        model=fomm_registry["23"],
        beta=2000,
        error_threshold=1e-5,
    ),
    "123": BaseProofreader(
        model=fomm_registry["23"],
        beta=3000,
        error_threshold=1e-5,
    ),
    "124": BaseProofreader(
        model=fomm_registry["23"],
        beta=10000,
        error_threshold=1e-5,
    ),
    "125": BaseProofreader(
        model=fomm_registry["23"],
        beta=20000,
        error_threshold=1e-5,
    ),
    "126": BaseProofreader(
        model=fomm_registry["23"],
        beta=50000,
        error_threshold=1e-5,
    ),
    "127": BaseProofreader(
        model=fomm_registry["24"],
        beta=1,
        error_threshold=1e-4,
    ),
    "128": BaseProofreader(
        model=fomm_registry["24"],
        beta=0.05,
        error_threshold=1e-4,
    ),
    "129": BaseProofreader(
        model=fomm_registry["24"],
        beta=0.1,
        error_threshold=1e-4,
    ),
    "130": BaseProofreader(
        model=fomm_registry["24"],
        beta=0.2,
        error_threshold=1e-4,
    ),
    "131": BaseProofreader(
        model=fomm_registry["24"],
        beta=0.5,
        error_threshold=1e-4,
    ),
    "132": BaseProofreader(
        model=fomm_registry["24"],
        beta=2,
        error_threshold=1e-4,
    ),
    "133": BaseProofreader(
        model=fomm_registry["24"],
        beta=5,
        error_threshold=1e-4,
    ),
    "134": BaseProofreader(
        model=fomm_registry["24"],
        beta=10,
        error_threshold=1e-4,
    ),
    "135": BaseProofreader(
        model=fomm_registry["24"],
        beta=20,
        error_threshold=1e-4,
    ),
    "136": BaseProofreader(
        model=fomm_registry["24"],
        beta=50,
        error_threshold=1e-4,
    ),
    "137": BaseProofreader(
        model=fomm_registry["24"],
        beta=100,
        error_threshold=1e-4,
    ),
    "138": BaseProofreader(
        model=fomm_registry["24"],
        beta=200,
        error_threshold=1e-4,
    ),
    "139": BaseProofreader(
        model=fomm_registry["24"],
        beta=500,
        error_threshold=1e-4,
    ),
    "140": BaseProofreader(
        model=fomm_registry["24"],
        beta=1000,
        error_threshold=1e-4,
    ),
    "141": BaseProofreader(
        model=fomm_registry["24"],
        beta=2000,
        error_threshold=1e-4,
    ),
    "142": BaseProofreader(
        model=fomm_registry["25"],
        beta=0.05,
        error_threshold=1e-4,
    ),
    "143": BaseProofreader(
        model=fomm_registry["25"],
        beta=0.1,
        error_threshold=1e-4,
    ),
    "144": BaseProofreader(
        model=fomm_registry["25"],
        beta=0.2,
        error_threshold=1e-4,
    ),
    "145": BaseProofreader(
        model=fomm_registry["25"],
        beta=0.5,
        error_threshold=1e-4,
    ),
    "146": BaseProofreader(
        model=fomm_registry["25"],
        beta=1,
        error_threshold=1e-4,
    ),
    "147": BaseProofreader(
        model=fomm_registry["25"],
        beta=2,
        error_threshold=1e-4,
    ),
    "148": BaseProofreader(
        model=fomm_registry["25"],
        beta=5,
        error_threshold=1e-4,
    ),
    "149": BaseProofreader(
        model=fomm_registry["25"],
        beta=10,
        error_threshold=1e-4,
    ),
    "150": BaseProofreader(
        model=fomm_registry["25"],
        beta=20,
        error_threshold=1e-4,
    ),
    "151": BaseProofreader(
        model=fomm_registry["25"],
        beta=50,
        error_threshold=1e-4,
    ),
    "152": BaseProofreader(
        model=fomm_registry["25"],
        beta=100,
        error_threshold=1e-4,
    ),
    "153": BaseProofreader(
        model=fomm_registry["25"],
        beta=200,
        error_threshold=1e-4,
    ),
    "154": BaseProofreader(
        model=fomm_registry["25"],
        beta=500,
        error_threshold=1e-4,
    ),
    "155": BaseProofreader(
        model=fomm_registry["25"],
        beta=1000,
        error_threshold=1e-4,
    ),
    "156": BaseProofreader(
        model=fomm_registry["25"],
        beta=2000,
        error_threshold=1e-4,
    ),
    "157": BaseProofreader(
        model=fomm_registry["25"],
        beta=1000,
        error_threshold=1e-6,
    ),
    "158": BaseProofreader(
        model=fomm_registry["25"],
        beta=1000,
        error_threshold=1e-5,
    ),
    "159": BaseProofreader(
        model=fomm_registry["25"],
        beta=1000,
        error_threshold=1e-3,
    ),
    "160": BaseProofreader(
        model=fomm_registry["25"],
        beta=1000,
        error_threshold=1e-2,
    ),
    "161": BaseProofreader(
        model=fomm_registry["25"],
        beta=1000,
        error_threshold=1e-1,
    ),
    # Backwards models, by error threshold
    "162": BaseProofreader(
        model=fomm_registry["26"],
        beta=1000,
        error_threshold=1e-6,
    ),
    "163": BaseProofreader(
        model=fomm_registry["26"],
        beta=1000,
        error_threshold=3e-6,
    ),
    "164": BaseProofreader(
        model=fomm_registry["26"],
        beta=1000,
        error_threshold=1e-5,
    ),
    "165": BaseProofreader(
        model=fomm_registry["26"],
        beta=1000,
        error_threshold=3e-5,
    ),
    "166": BaseProofreader(
        model=fomm_registry["26"],
        beta=1000,
        error_threshold=1e-4,
    ),
    "167": BaseProofreader(
        model=fomm_registry["26"],
        beta=1000,
        error_threshold=3e-4,
    ),
    "168": BaseProofreader(
        model=fomm_registry["26"],
        beta=1000,
        error_threshold=1e-3,
    ),
    "169": BaseProofreader(
        model=fomm_registry["26"],
        beta=1000,
        error_threshold=3e-3,
    ),
    "170": BaseProofreader(
        model=fomm_registry["26"],
        beta=1000,
        error_threshold=1e-2,
    ),
    "171": BaseProofreader(
        model=fomm_registry["26"],
        beta=1000,
        error_threshold=3e-2,
    ),
    "172": BaseProofreader(
        model=fomm_registry["26"],
        beta=1000,
        error_threshold=1e-1,
    ),
    "173": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="min",
        error_threshold=1e-5,
    ),
    "174": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="min",
        error_threshold=2e-5,
    ),
    "175": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="min",
        error_threshold=5e-5,
    ),
    "176": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="min",
        error_threshold=1e-4,
    ),
    "177": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="min",
        error_threshold=2e-4,
    ),
    "178": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="min",
        error_threshold=5e-4,
    ),
    "179": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="min",
        error_threshold=1e-3,
    ),
    "180": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="min",
        error_threshold=2e-3,
    ),
    "181": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="min",
        error_threshold=5e-3,
    ),
    "182": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="min",
        error_threshold=1e-2,
    ),
    "183": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="max",
        error_threshold=1e-5,
    ),
    "184": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="max",
        error_threshold=2e-5,
    ),
    "185": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="max",
        error_threshold=5e-5,
    ),
    "186": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="max",
        error_threshold=1e-4,
    ),
    "187": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="max",
        error_threshold=2e-4,
    ),
    "188": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="max",
        error_threshold=5e-4,
    ),
    "189": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="max",
        error_threshold=1e-3,
    ),
    "190": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="max",
        error_threshold=2e-3,
    ),
    "191": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="max",
        error_threshold=5e-3,
    ),
    "192": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="max",
        error_threshold=1e-2,
    ),
    "193": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="mean",
        error_threshold=1e-5,
    ),
    "194": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="mean",
        error_threshold=2e-5,
    ),
    "195": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="mean",
        error_threshold=5e-5,
    ),
    "196": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="mean",
        error_threshold=1e-4,
    ),
    "197": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="mean",
        error_threshold=2e-4,
    ),
    "198": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="mean",
        error_threshold=5e-4,
    ),
    "199": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="mean",
        error_threshold=1e-3,
    ),
    "200": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="mean",
        error_threshold=2e-3,
    ),
    "201": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="mean",
        error_threshold=5e-3,
    ),
    "202": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="mean",
        error_threshold=1e-2,
    ),
    "203": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="geometric_mean",
        error_threshold=1e-5,
    ),
    "204": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="geometric_mean",
        error_threshold=2e-5,
    ),
    "205": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="geometric_mean",
        error_threshold=5e-5,
    ),
    "206": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="geometric_mean",
        error_threshold=1e-4,
    ),
    "207": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="geometric_mean",
        error_threshold=2e-4,
    ),
    "208": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="geometric_mean",
        error_threshold=5e-4,
    ),
    "209": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="geometric_mean",
        error_threshold=1e-3,
    ),
    "210": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="geometric_mean",
        error_threshold=2e-3,
    ),
    "211": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="geometric_mean",
        error_threshold=5e-3,
    ),
    "212": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1000,
        combination_method="geometric_mean",
        error_threshold=1e-2,
    ),
    "213": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=1,
        combination_method="geometric_mean",
        error_threshold=5e-4,
    ),
    # Duplicate
    # "214": BaseMultimodelProofreader(
    #     model=[fomm_registry["25"], fomm_registry["26"]],
    #     beta=1000,
    #     combination_method="geometric_mean",
    #     error_threshold=5e-4,
    # ),
    "215": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=3,
        combination_method="geometric_mean",
        error_threshold=5e-4,
    ),
    "216": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=10,
        combination_method="geometric_mean",
        error_threshold=5e-4,
    ),
    "217": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=30,
        combination_method="geometric_mean",
        error_threshold=5e-4,
    ),
    "218": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=100,
        combination_method="geometric_mean",
        error_threshold=5e-4,
    ),
    "219": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=300,
        combination_method="geometric_mean",
        error_threshold=5e-4,
    ),
    "220": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=3000,
        combination_method="geometric_mean",
        error_threshold=5e-4,
    ),
    "221": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=10000,
        combination_method="geometric_mean",
        error_threshold=5e-4,
    ),
    "222": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=30000,
        combination_method="geometric_mean",
        error_threshold=5e-4,
    ),
    "223": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=100000,
        combination_method="geometric_mean",
        error_threshold=5e-4,
    ),
    "224": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=300000,
        combination_method="geometric_mean",
        error_threshold=5e-4,
    ),
    "225": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=0.3,
        combination_method="geometric_mean",
        error_threshold=5e-4,
    ),
    "226": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=0.1,
        combination_method="geometric_mean",
        error_threshold=5e-4,
    ),
    "227": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=0.03,
        combination_method="geometric_mean",
        error_threshold=5e-4,
    ),
    "228": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=0.01,
        combination_method="geometric_mean",
        error_threshold=5e-4,
    ),
    "229": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=0.003,
        combination_method="geometric_mean",
        error_threshold=5e-4,
    ),
    # try with a range of dictionary sizes
    # models trained on corpus 05
    # tok_ver tok_alpha  fomm_fwd_ver  fomm_bak_ver
    # 05      20K        07            23
    # 06      10K        27            28
    # 07      5K         29            30
    # 08      2K         24            31
    # 09      1K         32            33
    # 11      500        25            26
    # 12      200        34            35
    # 13      100        36            37
    "230": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        beta=0.001,
        combination_method="geometric_mean",
        error_threshold=5e-4,
    ),
    "231": BaseMultimodelProofreader(
        model=[fomm_registry["07"], fomm_registry["23"]],
        beta=5000,
        combination_method="geometric_mean",
        error_threshold=5e-4,
    ),
    "232": BaseMultimodelProofreader(
        model=[fomm_registry["27"], fomm_registry["28"]],
        beta=5000,
        combination_method="geometric_mean",
        error_threshold=5e-4,
    ),
    "233": BaseMultimodelProofreader(
        model=[fomm_registry["29"], fomm_registry["30"]],
        beta=5000,
        combination_method="geometric_mean",
        error_threshold=5e-4,
    ),
    "234": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=5000,
        combination_method="geometric_mean",
        error_threshold=5e-4,
    ),
    "235": BaseMultimodelProofreader(
        model=[fomm_registry["32"], fomm_registry["33"]],
        beta=5000,
        combination_method="geometric_mean",
        error_threshold=5e-4,
    ),
    "236": BaseMultimodelProofreader(
        model=[fomm_registry["34"], fomm_registry["35"]],
        beta=5000,
        combination_method="geometric_mean",
        error_threshold=5e-4,
    ),
    # Explore paired models with 2k dictionaries
    "237": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=5000,
        combination_method="geometric_mean",
        error_threshold=1e-6,
    ),
    "238": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=5000,
        combination_method="geometric_mean",
        error_threshold=3e-6,
    ),
    "239": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=5000,
        combination_method="geometric_mean",
        error_threshold=1e-5,
    ),
    "240": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=5000,
        combination_method="geometric_mean",
        error_threshold=3e-5,
    ),
    "241": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=5000,
        combination_method="geometric_mean",
        error_threshold=1e-4,
    ),
    "242": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=5000,
        combination_method="geometric_mean",
        error_threshold=3e-4,
    ),
    "243": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=5000,
        combination_method="geometric_mean",
        error_threshold=1e-3,
    ),
    "244": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=5000,
        combination_method="geometric_mean",
        error_threshold=3e-3,
    ),
    "245": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=5000,
        combination_method="geometric_mean",
        error_threshold=1e-2,
    ),
    "246": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=5000,
        combination_method="geometric_mean",
        error_threshold=3e-2,
    ),
    # Explore paired models with 2k dictionaries, beta 1000
    "247": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=1000,
        combination_method="geometric_mean",
        error_threshold=1e-6,
    ),
    "248": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=1000,
        combination_method="geometric_mean",
        error_threshold=3e-6,
    ),
    "249": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=1000,
        combination_method="geometric_mean",
        error_threshold=1e-5,
    ),
    "250": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=1000,
        combination_method="geometric_mean",
        error_threshold=3e-5,
    ),
    "251": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=1000,
        combination_method="geometric_mean",
        error_threshold=1e-4,
    ),
    "252": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=1000,
        combination_method="geometric_mean",
        error_threshold=3e-4,
    ),
    "253": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=1000,
        combination_method="geometric_mean",
        error_threshold=1e-3,
    ),
    "254": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=1000,
        combination_method="geometric_mean",
        error_threshold=3e-3,
    ),
    "255": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=1000,
        combination_method="geometric_mean",
        error_threshold=1e-2,
    ),
    "256": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=1000,
        combination_method="geometric_mean",
        error_threshold=3e-2,
    ),
    # Explore paired models with 2k dictionaries, beta 500
    "257": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=500,
        combination_method="geometric_mean",
        error_threshold=1e-6,
    ),
    "258": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=500,
        combination_method="geometric_mean",
        error_threshold=3e-6,
    ),
    "259": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=500,
        combination_method="geometric_mean",
        error_threshold=1e-5,
    ),
    "260": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=500,
        combination_method="geometric_mean",
        error_threshold=3e-5,
    ),
    "261": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=500,
        combination_method="geometric_mean",
        error_threshold=1e-4,
    ),
    "262": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=500,
        combination_method="geometric_mean",
        error_threshold=3e-4,
    ),
    "263": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=500,
        combination_method="geometric_mean",
        error_threshold=1e-3,
    ),
    "264": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=500,
        combination_method="geometric_mean",
        error_threshold=3e-3,
    ),
    "265": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=500,
        combination_method="geometric_mean",
        error_threshold=1e-2,
    ),
    "266": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=500,
        combination_method="geometric_mean",
        error_threshold=3e-2,
    ),
    # Explore paired models with 2k dictionaries, beta 2000
    "267": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=2000,
        combination_method="geometric_mean",
        error_threshold=1e-6,
    ),
    "268": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=2000,
        combination_method="geometric_mean",
        error_threshold=3e-6,
    ),
    "269": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=2000,
        combination_method="geometric_mean",
        error_threshold=1e-5,
    ),
    "270": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=2000,
        combination_method="geometric_mean",
        error_threshold=3e-5,
    ),
    "271": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=2000,
        combination_method="geometric_mean",
        error_threshold=1e-4,
    ),
    "272": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=2000,
        combination_method="geometric_mean",
        error_threshold=3e-4,
    ),
    "273": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=2000,
        combination_method="geometric_mean",
        error_threshold=1e-3,
    ),
    "274": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=2000,
        combination_method="geometric_mean",
        error_threshold=3e-3,
    ),
    "275": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=2000,
        combination_method="geometric_mean",
        error_threshold=1e-2,
    ),
    "276": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=2000,
        combination_method="geometric_mean",
        error_threshold=3e-2,
    ),
    # Explore paired models with 2k dictionaries, beta 200
    "277": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=200,
        combination_method="geometric_mean",
        error_threshold=1e-6,
    ),
    "278": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=200,
        combination_method="geometric_mean",
        error_threshold=3e-6,
    ),
    "279": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=200,
        combination_method="geometric_mean",
        error_threshold=1e-5,
    ),
    "280": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=200,
        combination_method="geometric_mean",
        error_threshold=3e-5,
    ),
    "281": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=200,
        combination_method="geometric_mean",
        error_threshold=1e-4,
    ),
    "282": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=200,
        combination_method="geometric_mean",
        error_threshold=3e-4,
    ),
    "283": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=200,
        combination_method="geometric_mean",
        error_threshold=1e-3,
    ),
    "284": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=200,
        combination_method="geometric_mean",
        error_threshold=3e-3,
    ),
    "285": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=200,
        combination_method="geometric_mean",
        error_threshold=1e-2,
    ),
    "286": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        beta=200,
        combination_method="geometric_mean",
        error_threshold=3e-2,
    ),
    # Add in alpha, starting with alpha = 1
    "287": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=1,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-7,
    ),
    "288": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=1,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-7,
    ),
    "289": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=1,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-6,
    ),
    "290": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=1,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-6,
    ),
    "291": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=1,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-5,
    ),
    "292": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=1,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-5,
    ),
    "293": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=1,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-4,
    ),
    "294": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=1,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-4,
    ),
    "295": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=1,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-3,
    ),
    "296": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=1,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-3,
    ),
    # Alpha = 10
    "297": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=10,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-7,
    ),
    "298": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=10,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-7,
    ),
    "299": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=10,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-6,
    ),
    "300": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=10,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-6,
    ),
    "301": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=10,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-5,
    ),
    "302": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=10,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-5,
    ),
    "303": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=10,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-4,
    ),
    "304": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=10,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-4,
    ),
    "305": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=10,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-3,
    ),
    "306": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=10,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-3,
    ),
    # Alpha = 100
    "307": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-7,
    ),
    "308": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-7,
    ),
    "309": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-6,
    ),
    "310": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-6,
    ),
    "311": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-5,
    ),
    "312": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-5,
    ),
    "313": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-4,
    ),
    "314": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-4,
    ),
    "315": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-3,
    ),
    "316": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-3,
    ),
    # Alpha = 1000
    "317": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=1000,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-7,
    ),
    "318": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=1000,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-7,
    ),
    "319": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=1000,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-6,
    ),
    "320": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=1000,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-6,
    ),
    "321": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=1000,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-5,
    ),
    "322": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=1000,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-5,
    ),
    "323": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=1000,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-4,
    ),
    "324": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=1000,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-4,
    ),
    "325": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=1000,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-3,
    ),
    "326": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=1000,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-3,
    ),
    # try with a range of dictionary sizes
    # models trained on corpus 05
    # tok_ver tok_alpha  fomm_fwd_ver  fomm_bak_ver
    # 05      20K        07            23
    # 06      10K        27            28
    # 07      5K         29            30
    # 08      2K         24            31
    # 09      1K         32            33
    # 11      500        25            26
    # 12      200        34            35
    # 13      100        36            37
    "327": BaseMultimodelProofreader(
        model=[fomm_registry["07"], fomm_registry["23"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-4,
    ),
    "328": BaseMultimodelProofreader(
        model=[fomm_registry["27"], fomm_registry["28"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-4,
    ),
    "329": BaseMultimodelProofreader(
        model=[fomm_registry["29"], fomm_registry["30"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-4,
    ),
    "330": BaseMultimodelProofreader(
        model=[fomm_registry["24"], fomm_registry["31"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-4,
    ),
    "331": BaseMultimodelProofreader(
        model=[fomm_registry["32"], fomm_registry["33"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-4,
    ),
    "332": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-4,
    ),
    "333": BaseMultimodelProofreader(
        model=[fomm_registry["34"], fomm_registry["35"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-4,
    ),
    # The the whole thing again with models 25, 26, alphabet size = 500
    # starting with alpha = 1
    "334": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-7,
    ),
    "335": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-7,
    ),
    "336": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-6,
    ),
    "337": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-6,
    ),
    "338": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-5,
    ),
    "339": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-5,
    ),
    "340": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-4,
    ),
    "341": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-4,
    ),
    "342": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-3,
    ),
    "343": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-3,
    ),
    # Alpha = 10
    "344": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=10,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-7,
    ),
    "345": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=10,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-7,
    ),
    "346": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=10,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-6,
    ),
    "347": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=10,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-6,
    ),
    "348": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=10,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-5,
    ),
    "349": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=10,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-5,
    ),
    "350": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=10,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-4,
    ),
    "351": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=10,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-4,
    ),
    "352": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=10,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-3,
    ),
    "353": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=10,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-3,
    ),
    # Alpha = 100
    "354": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-7,
    ),
    "355": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-7,
    ),
    "356": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-6,
    ),
    "357": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-6,
    ),
    "358": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-5,
    ),
    "359": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-5,
    ),
    "360": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-4,
    ),
    "361": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-4,
    ),
    "362": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-3,
    ),
    "363": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-3,
    ),
    # Alpha = 1000
    "364": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1000,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-7,
    ),
    "365": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1000,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-7,
    ),
    "366": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1000,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-6,
    ),
    "367": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1000,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-6,
    ),
    "368": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1000,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-5,
    ),
    "369": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1000,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-5,
    ),
    "370": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1000,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-4,
    ),
    "371": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1000,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-4,
    ),
    "372": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1000,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-3,
    ),
    "373": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1000,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-3,
    ),
    # Back to min, combine alpha and beta
    "374": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=1000,
        combination_method="min",
        error_threshold=1e-5,
    ),
    "375": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=1000,
        combination_method="min",
        error_threshold=2e-5,
    ),
    "376": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=1000,
        combination_method="min",
        error_threshold=5e-5,
    ),
    "377": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=1000,
        combination_method="min",
        error_threshold=1e-4,
    ),
    "378": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=1000,
        combination_method="min",
        error_threshold=2e-4,
    ),
    "379": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=1000,
        combination_method="min",
        error_threshold=5e-4,
    ),
    "380": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=1000,
        combination_method="min",
        error_threshold=1e-3,
    ),
    "381": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=1000,
        combination_method="min",
        error_threshold=2e-3,
    ),
    "382": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=1000,
        combination_method="min",
        error_threshold=5e-3,
    ),
    "383": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=1000,
        combination_method="min",
        error_threshold=1e-2,
    ),
    # Alpha = 100, geom mean retake with shifted error range
    "384": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-6,
    ),
    "385": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-6,
    ),
    "386": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-5,
    ),
    "387": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-5,
    ),
    "388": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-4,
    ),
    "389": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-4,
    ),
    "390": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-3,
    ),
    "391": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-3,
    ),
    "392": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=1e-2,
    ),
    "393": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=100,
        beta=None,
        combination_method="geometric_mean",
        error_threshold=3e-2,
    ),
    # Back to min, combine alpha and beta
    "394": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1000,
        beta=1000,
        combination_method="min",
        error_threshold=1e-5,
    ),
    "395": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1000,
        beta=1000,
        combination_method="min",
        error_threshold=2e-5,
    ),
    "396": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1000,
        beta=1000,
        combination_method="min",
        error_threshold=5e-5,
    ),
    "397": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1000,
        beta=1000,
        combination_method="min",
        error_threshold=1e-4,
    ),
    "398": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1000,
        beta=1000,
        combination_method="min",
        error_threshold=2e-4,
    ),
    "399": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1000,
        beta=1000,
        combination_method="min",
        error_threshold=5e-4,
    ),
    "400": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1000,
        beta=1000,
        combination_method="min",
        error_threshold=1e-3,
    ),
    "401": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1000,
        beta=1000,
        combination_method="min",
        error_threshold=2e-3,
    ),
    "402": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1000,
        beta=1000,
        combination_method="min",
        error_threshold=5e-3,
    ),
    "403": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=1000,
        beta=1000,
        combination_method="min",
        error_threshold=1e-2,
    ),
    # Back to min, combine alpha and beta, alpha = 10000
    "404": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=10000,
        beta=1000,
        combination_method="min",
        error_threshold=1e-5,
    ),
    "405": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=10000,
        beta=1000,
        combination_method="min",
        error_threshold=2e-5,
    ),
    "406": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=10000,
        beta=1000,
        combination_method="min",
        error_threshold=5e-5,
    ),
    "407": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=10000,
        beta=1000,
        combination_method="min",
        error_threshold=1e-4,
    ),
    "408": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=10000,
        beta=1000,
        combination_method="min",
        error_threshold=2e-4,
    ),
    "409": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=10000,
        beta=1000,
        combination_method="min",
        error_threshold=5e-4,
    ),
    "410": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=10000,
        beta=1000,
        combination_method="min",
        error_threshold=1e-3,
    ),
    "411": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=10000,
        beta=1000,
        combination_method="min",
        error_threshold=2e-3,
    ),
    "412": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=10000,
        beta=1000,
        combination_method="min",
        error_threshold=5e-3,
    ),
    "413": BaseMultimodelProofreader(
        model=[fomm_registry["25"], fomm_registry["26"]],
        alpha=10000,
        beta=1000,
        combination_method="min",
        error_threshold=1e-2,
    ),
}
