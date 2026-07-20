"""
A first-order Markov Model for predicting the liklihood of a language
token, given the previous token.
"""

import os
import numpy as np
from proofread_eng_scifi.models.markov_base import MarkovBase


class FirstOrderMarkovModel(MarkovBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_dir = os.path.dirname(__file__)
        self.model_path = os.path.join(self.model_dir, self.model_filename)
        self.description = "1st-order Markov"

    def _initialize(self):
        self.transition_counts = np.zeros(
            (self.n_unique_tokens, self.n_unique_tokens),
            dtype=np.int32,
        )
        self.transition_probabilities = np.zeros(
            (self.n_unique_tokens, self.n_unique_tokens),
            dtype=np.float64,
        )

    def is_ready(self):
        # Check whether the model is trained and loaded
        try:
            if np.sum(self.transition_counts) > 100:
                return True
        except AttributeError:
            pass
        return False

    def _train_from_tokens(self, ids):
        # Doesn't re-initialize. Multiple calls will accumulate
        # training experience.
        for i_transition in range(len(ids) - 1):
            self.transition_counts[
                ids[i_transition], ids[i_transition + 1]
            ] += 1

        self.transition_probabilities = (
            self.transition_counts
            / (np.sum(self.transition_counts, axis=1) + self.epsilon)[
                :, np.newaxis
            ]
        ) + self.transition_probability_floor

    def _calc_likelihoods(self, ids):
        if len(ids) < 2:
            return None

        # The model doesn't have anything useful to say about the first
        # token, so initialize it by hand.
        likelihoods = [1.0]
        for i_transition in range(len(ids) - 1):
            likelihoods.append(
                self.transition_probabilities[
                    ids[i_transition], ids[i_transition + 1]
                ]
            )
        return likelihoods


class SparseFirstOrderMarkovModel(MarkovBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_dir = os.path.dirname(__file__)
        self.model_path = os.path.join(self.model_dir, self.model_filename)
        self.description = "Sparse 1st-order Markov"

    def _initialize(self):
        self.unigram_counts = {}
        self.bigram_counts = {}

    def is_ready(self):
        # Check whether the model is trained and loaded
        try:
            if (
                len(self.unigram_counts) > self.not_empty_threshold
                and len(self.bigram_counts) > self.not_empty_threshold
            ):
                return True
        except AttributeError:
            pass
        return False

    def _train_from_tokens(self, ids):
        for i_transition in range(len(ids) - 1):
            unigram_key = tuple([ids[i_transition]])
            bigram_key = tuple(
                [
                    ids[i_transition],
                    ids[i_transition + 1],
                ]
            )
            self.unigram_counts[unigram_key] = (
                self.unigram_counts.get(unigram_key, 0) + 1
            )
            self.bigram_counts[bigram_key] = (
                self.bigram_counts.get(bigram_key, 0) + 1
            )

    def _calc_likelihoods(self, ids):
        if len(ids) < 2:
            return None

        # The model doesn't have anything useful to say about the first
        # token, so initialize it by hand.
        likelihoods = [1.0]
        for i_transition in range(len(ids) - 1):
            unigram_key = tuple([ids[i_transition]])
            bigram_key = tuple(
                [
                    ids[i_transition],
                    ids[i_transition + 1],
                ]
            )
            unigram_count = self.unigram_counts.get(unigram_key, self.epsilon)
            bigram_count = self.bigram_counts.get(bigram_key, 0)
            likelihoods.append(
                bigram_count / unigram_count + self.transition_probability_floor
            )

        return likelihoods


registry = {
    "00": FirstOrderMarkovModel(
        version="00",
        tokenizer_version="00",
        corpus_versions=["00"],
    ),
    "01": FirstOrderMarkovModel(
        version="01",
        tokenizer_version="00",
        corpus_versions=["00", "01"],
    ),
    "02": FirstOrderMarkovModel(
        version="02",
        tokenizer_version="05",
        corpus_versions=["02"],
    ),
    "03": SparseFirstOrderMarkovModel(
        version="03",
        tokenizer_version="05",
        corpus_versions=["02"],
    ),
    "04": SparseFirstOrderMarkovModel(
        version="04",
        tokenizer_version="05",
        corpus_versions=["03"],
    ),
    "05": SparseFirstOrderMarkovModel(
        version="05",
        tokenizer_version="05",
        corpus_versions=["04"],
    ),
    # Duplicate
    # "06": SparseFirstOrderMarkovModel(
    #     version="06",
    #     tokenizer_version="05",
    #     corpus_versions=["04"],
    # ),
    "07": SparseFirstOrderMarkovModel(
        version="07",
        tokenizer_version="05",
        corpus_versions=["05"],
    ),
    "08": SparseFirstOrderMarkovModel(
        version="08",
        tokenizer_version="06",
        corpus_versions=["04"],
    ),
    "09": SparseFirstOrderMarkovModel(
        version="09",
        tokenizer_version="07",
        corpus_versions=["04"],
    ),
    "10": SparseFirstOrderMarkovModel(
        version="10",
        tokenizer_version="08",
        corpus_versions=["04"],
    ),
    "11": SparseFirstOrderMarkovModel(
        version="11",
        tokenizer_version="09",
        corpus_versions=["04"],
    ),
    "12": SparseFirstOrderMarkovModel(
        version="12",
        tokenizer_version="11",
        corpus_versions=["04"],
    ),
    "13": SparseFirstOrderMarkovModel(
        version="13",
        tokenizer_version="12",
        corpus_versions=["04"],
    ),
    "14": SparseFirstOrderMarkovModel(
        version="14",
        tokenizer_version="13",
        corpus_versions=["04"],
    ),
}
