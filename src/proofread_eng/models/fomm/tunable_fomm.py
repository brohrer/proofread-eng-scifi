"""
First-order Markov models whose hyperparameters are tuned on a corpus
of validation data.
"""

import os
import pickle

import numpy as np
from redsho.optimizer import Redsho

from proofread_eng.data.eval.eval_tunable_proofreading import calculate_results
from proofread_eng.data.train.registry import registry as training_data_registry
from proofread_eng.data.tune.tuning_data import eval_dict
from proofread_eng.models.markov_base import MarkovBase


class TunableFommBase(MarkovBase):
    def __init__(
        self,
        alpha_min=1e2,
        alpha_max=1e6,
        alpha_n=9,
        beta_min=1e2,
        beta_max=1e6,
        beta_n=9,
        error_threshold_min=1e2,
        error_threshold_max=1e6,
        error_threshold_n=9,
        rho=1,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.model_dir = os.path.dirname(__file__)
        self.model_path = os.path.join(self.model_dir, self.model_filename)
        self.unigram_filename = self.version + "_unigrams.pkl"
        self.unigram_path = os.path.join(self.model_dir, self.unigram_filename)
        self.bigram_filename = self.version + "_bigrams.pkl"
        self.bigram_path = os.path.join(self.model_dir, self.bigram_filename)
        self.hyperparam_filename = self.version + "_hyperparams.pkl"
        self.hyperparam_path = os.path.join(
            self.model_dir, self.hyperparam_filename
        )
        self.alpha_values = list(
            np.exp(np.linspace(np.log(alpha_min), np.log(alpha_max), alpha_n))
        )
        self.beta_values = list(
            np.exp(np.linspace(np.log(beta_min), np.log(beta_max), beta_n))
        )
        self.error_threshold_values = list(
            np.exp(
                np.linspace(
                    np.log(error_threshold_min),
                    np.log(error_threshold_max),
                    error_threshold_n,
                )
            )
        )
        self.rho = rho

    def _initialize(self):
        self.unigram_counts = {}
        self.bigram_counts = {}
        self.alpha = None
        self.beta = None
        self.error_threshold = None

    def stats_summary(self):
        n_books = training_data_registry[self.corpus_version].n_files
        if n_books >= 1000:
            books_str = f"{int(n_books / 1000)}k"
        else:
            books_str = str(int(n_books))

        summary = ", ".join(
            [
                f"mm{self.version}",
                f"{self.description}",
                f"alpha={self.alpha}",
                f"beta={self.beta}",
                f"err={self.error_threshold}",
                f"books={books_str}",
            ]
        )
        return summary

    def is_ready(self):
        # Check whether the model is trained and loaded
        try:
            if (
                len(self.unigram_counts) > self.not_empty_threshold
                and len(self.bigram_counts) > self.not_empty_threshold
                and self.alpha is not None
                and self.beta is not None
                and self.error_threshold is not None
            ):
                return True
        except AttributeError:
            pass
        return False

    def _tune(self):
        """
        Use the eval datasets to choose the best performing hyperparameters.
        """
        # Pull in condition sets from input args
        conditions = {
            "alpha": self.alpha_values,
            "beta": self.beta_values,
            "error_threshold": self.error_threshold_values,
        }

        # Choose your optimization algorithm and run its optimize() method.
        optimizer = Redsho(verbose=self.verbose)
        best_f_score, best_condition, results_logfile = optimizer.optimize(
            self._evaluate_condition, conditions
        )
        self.alpha = best_condition["alpha"]
        self.beta = best_condition["beta"]
        self.error_threshold = best_condition["error_threshold"]

        if self.verbose:
            print(f"{self.name} tuned to F-score= {best_f_score} with")
            print(f"    alpha= {self.alpha}")
            print(f"    beta= {self.beta}")
            print(f"    error_threshold= {self.error_threshold}")
            print(f"Details in {results_logfile}")

    def _evaluate_condition(self, alpha=None, beta=None, error_threshold=None):
        """
        Create evaluation function based on eval data and F-score
        """
        true_pos_total = 0
        false_pos_total = 0
        true_neg_total = 0
        false_neg_total = 0

        for eval_name, dataset in eval_dict.values():
            for paragraph_group in dataset:
                true_pos, false_pos, true_neg, false_neg = (
                    self._proof_tuning_text(
                        paragraph_group,
                        alpha=alpha,
                        beta=beta,
                        error_threshold=error_threshold,
                    )
                )
                true_pos_total += true_pos
                false_pos_total += false_pos
                true_neg_total += true_neg
                false_neg_total += false_neg

        # A small number to avoid division by zero
        epsilon = 1e-17
        precision = true_pos_total / (
            true_pos_total + false_pos_total + epsilon
        )
        # recall = true positive rate
        recall = true_pos_total / (true_pos_total + false_neg_total + epsilon)

        # calculate F-score
        # rho = 1 gives the F1 score, the most commone variant.
        # Higher rho means that recall is more important that precision
        # rho = 2 weights recall twice as heavily as precision.
        # (It should be beta instead of rho, but I'm already using beta
        # for the upward biased additive smoothing factor.)
        f_score = (
            (1 + self.rho**2)
            * (precision * recall)
            / (self.rho**2 * precision + recall)
        )

        return f_score

    def _proof_tuning_text(self, paragraph_group, alpha, beta, error_threshold):

        body = paragraph_group["paragraph"]
        paragraph_group["mistakes"]

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
        error_signal = self._calculate_token_error_signal(
            body_ids, alpha=alpha, beta=beta, error_threhsold=error_threshold
        )

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
        error_detections = [error_score < 1.0 for error_score in error_signal]

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

        true_pos, false_pos, true_neg, false_neg = calculate_results(
            paragraph_group["mistakes"], errors
        )

        return true_pos, false_pos, true_neg, false_neg

    def _save(self):
        with open(self.unigram_path, "wb") as f:
            pickle.dump(self.unigram_counts, f)
        with open(self.bigram_path, "wb") as f:
            pickle.dump(self.bigram_counts, f)
        with open(self.hyperparam_path, "wb") as f:
            pickle.dump((self.alpha, self.beta, self.error_threshold), f)

    def _load(self):
        with open(self.unigram_path, "rb") as f:
            self.unigram_counts = pickle.load(f)
        with open(self.bigram_path, "rb") as f:
            self.bigram_counts = pickle.load(f)
        with open(self.hyperparam_path, "rb") as f:
            self.alpha, self.beta, self.error_threshold = pickle.load(f)
        return self

    def delete(self):
        # Remove memory footprint
        self.unigram_counts.clear()
        self.bigram_counts.clear()
        self.alpha = None
        self.beta = None
        self.error_threshold = None


class TunableFommForward(TunableFommBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.description = "Tunable forward 1st-order Markov"

    def _train_from_tokens(self, ids):
        for i_transition in range(len(ids) - 1):
            unigram_key = (ids[i_transition],)
            bigram_key = (ids[i_transition], ids[i_transition + 1])
            self.unigram_counts[unigram_key] = (
                self.unigram_counts.get(unigram_key, 0) + 1
            )
            self.bigram_counts[bigram_key] = (
                self.bigram_counts.get(bigram_key, 0) + 1
            )

    def _calculate_token_error_signal(
        self,
        ids,
        alpha=None,
        beta=None,
        error_threshold=None,
    ):
        if alpha is None:
            alpha = self.alpha
        if beta is None:
            beta = self.beta
        if error_threshold is None:
            error_threshold = self.error_threshold
        if len(ids) < 2:
            return None

        # The model doesn't have anything useful to say about the first
        # token, so initialize it by hand.
        likelihoods = [1.0]
        for i_transition in range(len(ids) - 1):
            unigram_key = (ids[i_transition],)
            bigram_key = (ids[i_transition], ids[i_transition + 1])
            unigram_count = self.unigram_counts.get(unigram_key, 0)
            bigram_count = self.bigram_counts.get(bigram_key, 0)
            likelihoods.append(
                (bigram_count + alpha + beta)
                / (unigram_count + self.tokenizer.vocab_size * alpha + beta)
            )
            error_signal = np.array(likelihoods) / error_threshold

        return error_signal


registry = {
    "00": TunableFommForward(
        version="00",
        tokenizer_version="09",
        corpus_versions=["05"],
    ),
}
