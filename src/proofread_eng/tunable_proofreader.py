import numpy as np

from proofread_eng.models.fomm.tunable_fomm import (
    registry as tunable_fomm_registry,
)


class BaseTunableProofreader:
    def __init__(
        self,
        version=None,
        models=None,
        combination_method="min",
        scaled_error_threshold=1.0,
        verbose=True,
    ):
        self.version = version
        self.models = models
        self.combination_method = combination_method
        self.scaled_error_threshold = scaled_error_threshold
        self.verbose = verbose

        # Check that there is a list of models provided and
        # that they all have the same tokenizer.
        assert isinstance(self.models, list)
        assert len(self.models) > 0
        for m in self.models[1:]:
            assert self.models[0].tokenizer_version == m.tokenizer_version

        # For now assume that all models use the same tokenizer.
        # TODO: Let every model have its own tokenizer and let the
        # proofreader operate on a character level.
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

    def stats_summary(self):
        summary = ", ".join(
            [
                f"pr{self.version}",
                f"combo={self.combination_method}",
                f"cutoff={self.scaled_error_threshold}",
            ]
        )
        return summary

    def proof_file(self, filename):
        with open(filename, "rt") as f:
            body = f.read()
        return self.proof_text(body)

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
        all_error_signals = []
        for model in self.models:
            all_error_signals.append(
                model.calculate_token_error_signal(body_ids)
            )

        all_error_signals = np.array(all_error_signals)
        # combine them
        if self.combination_method == "min":
            error_signal = np.min(all_error_signals, axis=0)
        elif self.combination_method == "max":
            error_signal = np.max(all_error_signals, axis=0)
        elif self.combination_method == "mean":
            error_signal = np.mean(all_error_signals, axis=0)
        elif self.combination_method == "geometric_mean":
            error_signal = np.exp(np.mean(np.log(all_error_signals), axis=0))
        else:
            raise ValueError

        # show all probabilities and transitions
        debug = False
        if debug:
            for i_piece, body_piece in enumerate(body_pieces[:-1]):
                error_signal = error_signal[i_piece]
                print(
                    f"{int(error_signal * 1e6)}: "
                    + f"{body_piece} - {body_pieces[i_piece + 1]}"
                )

        # The least expected tokens are errors.
        error_detections = [
            error_score < self.scaled_error_threshold
            for error_score in error_signal
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
        for model in self.models:
            model.delete()


registry = {
    "000": BaseTunableProofreader(
        models=[tunable_fomm_registry["00"]],
        combination_method="min",
        scaled_error_threshold=1,
    ),
}
