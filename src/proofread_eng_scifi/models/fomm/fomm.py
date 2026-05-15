"""
A first-order Markov Model for predicting the liklihood of a language
token, given the previous token.
"""

import numpy as np


class FirstOrderMarkovModel:
    def __init__(self, n_unique_tokens=None):
        if n_unique_tokens is None:
            raise RuntimeError

        self.n_unique_tokens = int(n_unique_tokens)
        self.transition_counts = np.zeros((n_unique_tokens, n_unique_tokens))
        self.transition_probabilities = np.zeros(
            (n_unique_tokens, n_unique_tokens)
        )
        self.transition_probability_floor = 10e-4

    def train(self, ids):
        for i_transition in range(len(ids) - 1):
            self.transition_counts[
                ids[i_transition], ids[i_transition + 1]
            ] += 1

        self.transition_probabilities = (
            self.transition_counts /
            (np.sum(self.transition_counts, axis=1) + 1e-12)[:, np.newaxis]
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
