"""
A first-order Markov Model for predicting the liklihood of a language
token, given the previous token.
"""

import os
import pickle
import numpy as np

default_model_name = "fomm_no_9"


class FirstOrderMarkovModel:
    def __init__(
        self,
        n_unique_tokens=None,
        model_name=default_model_name,
        tokenizer_name="tokenizer_00",
    ):
        if n_unique_tokens is None:
            raise RuntimeError("n_unique_tokens is a required argument")

        self.n_unique_tokens = int(n_unique_tokens)
        self.model_name = model_name
        self.tokenizer_name = tokenizer_name
        self.transition_probability_floor = 10e-4
        self.initialize()

    def initialize(self):
        self.transition_counts = np.zeros(
            (self.n_unique_tokens, self.n_unique_tokens),
            dtype=np.int32,
        )
        self.transition_probabilities = np.zeros(
            (self.n_unique_tokens, self.n_unique_tokens),
            dtype=np.float64,
        )

    def train_from_tokens(self, ids):
        # Doesn't re-initialize. Multiple calls will accumulate
        # training experience.
        for i_transition in range(len(ids) - 1):
            self.transition_counts[
                ids[i_transition], ids[i_transition + 1]
            ] += 1

        self.transition_probabilities = (
            self.transition_counts
            / (np.sum(self.transition_counts, axis=1) + 1e-12)[:, np.newaxis]
        ) + self.transition_probability_floor

    def calculate_likelihoods(self, ids):
        if len(ids) < 2:
            return None

        likelihoods = []
        for i_transition in range(len(ids) - 1):
            likelihoods.append(
                self.transition_probabilities[
                    ids[i_transition], ids[i_transition + 1]
                ]
            )

        return likelihoods

    def save(self):
        model_filename = self.model_name + ".pkl"
        model_path = os.path.join(os.path.dirname(__file__), model_filename)
        with open(model_path, "wb") as f:
            pickle.dump(self, f)


def load(model_name=default_model_name):
    """
    model_name: str
    The name of the model, minus the .pkl suffix.
    """
    model_filename = model_name + ".pkl"
    model_path = os.path.join(os.path.dirname(__file__), model_filename)
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model
