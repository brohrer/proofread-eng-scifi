"""
A first-order Markov Model for predicting the liklihood of a language
token, given the previous token.
"""

import os
import pickle

from proofread_eng.models.markov_base import MarkovBase


class FirstOrderMarkovModelBase(MarkovBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_dir = os.path.dirname(__file__)
        self.model_path = os.path.join(self.model_dir, self.model_filename)
        self.unigram_filename = self.version + "_unigrams.pkl"
        self.unigram_path = os.path.join(self.model_dir, self.unigram_filename)
        self.bigram_filename = self.version + "_bigrams.pkl"
        self.bigram_path = os.path.join(self.model_dir, self.bigram_filename)

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

    def _save(self):
        with open(self.unigram_path, "wb") as f:
            pickle.dump(self.unigram_counts, f)
        with open(self.bigram_path, "wb") as f:
            pickle.dump(self.bigram_counts, f)

    def _load(self):
        try:
            with open(self.unigram_path, "rb") as f:
                self.unigram_counts = pickle.load(f)
            with open(self.bigram_path, "rb") as f:
                self.bigram_counts = pickle.load(f)

        except FileNotFoundError:
            model = super()._load()
            self.unigram_counts = model.unigram_counts
            self.bigram_counts = model.bigram_counts
            self._save()

        return self

    def delete(self):
        # Remove memory footprint
        self.unigram_counts.clear()
        self.bigram_counts.clear()


class SparseFirstOrderMarkovModel(FirstOrderMarkovModelBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.description = "Forward 1st-order Markov"

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

    def _calc_likelihoods(self, ids, alpha=None, beta=None):
        """
        beta is being used here to impliment a variation of additive smoothing.
        https://en.wikipedia.org/wiki/Additive_smoothing
        https://brandonrohrer.org/alms_composite.html#Upward-biased-additive-smoothing
        """
        if len(ids) < 2:
            return None

        if alpha is None:
            alpha = self.epsilon

        if beta is None:
            beta = self.epsilon

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

        return likelihoods


class ReverseFirstOrderMarkovModel(FirstOrderMarkovModelBase):
    """
    Identical to SparseFirstOrderMarkovModel, but runs back to front
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.description = "Reverse 1st-order Markov"

    def _train_from_tokens(self, ids):
        for i_transition in range(len(ids) - 1):
            unigram_key = (ids[i_transition + 1],)
            bigram_key = (ids[i_transition], ids[i_transition + 1])
            self.unigram_counts[unigram_key] = (
                self.unigram_counts.get(unigram_key, 0) + 1
            )
            self.bigram_counts[bigram_key] = (
                self.bigram_counts.get(bigram_key, 0) + 1
            )

    def _calc_likelihoods(self, ids, alpha=None, beta=None):
        """
        beta is being used here to impliment a variation of additive smoothing.
        https://en.wikipedia.org/wiki/Additive_smoothing
        https://brandonrohrer.org/alms_composite.html#Upward-biased-additive-smoothing
        """
        if len(ids) < 2:
            return None

        if alpha is None:
            alpha = self.epsilon

        if beta is None:
            beta = self.epsilon

        likelihoods = []
        for i_transition in range(len(ids) - 1):
            unigram_key = (ids[i_transition + 1],)
            bigram_key = (ids[i_transition], ids[i_transition + 1])
            unigram_count = self.unigram_counts.get(unigram_key, 0)
            bigram_count = self.bigram_counts.get(bigram_key, 0)
            likelihoods.append(
                (bigram_count + alpha + beta)
                / (unigram_count + self.tokenizer.vocab_size * alpha + beta)
            )

        # The model doesn't have anything useful to say about the last
        # token, so initialize it by hand.
        likelihoods.append(1.0)

        return likelihoods


registry = {
    # "00": FirstOrderMarkovModel(
    #     version="00",
    #     tokenizer_version="00",
    #     corpus_versions=["00"],
    # ),
    # "01": FirstOrderMarkovModel(
    #     version="01",
    #     tokenizer_version="00",
    #     corpus_versions=["00", "01"],
    # ),
    # "02": FirstOrderMarkovModel(
    #     version="02",
    #     tokenizer_version="05",
    #     corpus_versions=["02"],
    # ),
    # "03": SparseFirstOrderMarkovModel(
    #     version="03",
    #     tokenizer_version="05",
    #     corpus_versions=["02"],
    # ),
    # "04": SparseFirstOrderMarkovModel(
    #     version="04",
    #     tokenizer_version="05",
    #     corpus_versions=["03"],
    # ),
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
    # "14": SparseFirstOrderMarkovModel(
    #     version="14",
    #     tokenizer_version="13",
    #     corpus_versions=["04"],
    # ),
    "15": ReverseFirstOrderMarkovModel(
        version="15",
        tokenizer_version="05",
        corpus_versions=["04"],
    ),
    "16": ReverseFirstOrderMarkovModel(
        version="16",
        tokenizer_version="06",
        corpus_versions=["04"],
    ),
    "17": ReverseFirstOrderMarkovModel(
        version="17",
        tokenizer_version="07",
        corpus_versions=["04"],
    ),
    "18": ReverseFirstOrderMarkovModel(
        version="18",
        tokenizer_version="08",
        corpus_versions=["04"],
    ),
    "19": ReverseFirstOrderMarkovModel(
        version="19",
        tokenizer_version="09",
        corpus_versions=["04"],
    ),
    # "20": ReverseFirstOrderMarkovModel(
    #     version="20",
    #     tokenizer_version="10",
    #     corpus_versions=["04"],
    # ),
    "21": ReverseFirstOrderMarkovModel(
        version="21",
        tokenizer_version="11",
        corpus_versions=["04"],
    ),
    "22": ReverseFirstOrderMarkovModel(
        version="22",
        tokenizer_version="12",
        corpus_versions=["04"],
    ),
    "23": ReverseFirstOrderMarkovModel(
        version="23",
        tokenizer_version="05",
        corpus_versions=["05"],
    ),
    # 2K alphabet models on a 38K book corpus
    "24": SparseFirstOrderMarkovModel(
        version="24",
        tokenizer_version="08",
        corpus_versions=["05"],
    ),
    # 500 alphabet
    "25": SparseFirstOrderMarkovModel(
        version="25",
        tokenizer_version="11",
        corpus_versions=["05"],
    ),
    "26": ReverseFirstOrderMarkovModel(
        version="26",
        tokenizer_version="11",
        corpus_versions=["05"],
    ),
    "27": SparseFirstOrderMarkovModel(
        version="27",
        tokenizer_version="06",
        corpus_versions=["05"],
    ),
    "28": ReverseFirstOrderMarkovModel(
        version="28",
        tokenizer_version="06",
        corpus_versions=["05"],
    ),
    "29": SparseFirstOrderMarkovModel(
        version="29",
        tokenizer_version="07",
        corpus_versions=["05"],
    ),
    "30": ReverseFirstOrderMarkovModel(
        version="30",
        tokenizer_version="07",
        corpus_versions=["05"],
    ),
    "31": ReverseFirstOrderMarkovModel(
        version="31",
        tokenizer_version="08",
        corpus_versions=["05"],
    ),
    "32": SparseFirstOrderMarkovModel(
        version="32",
        tokenizer_version="09",
        corpus_versions=["05"],
    ),
    "33": ReverseFirstOrderMarkovModel(
        version="33",
        tokenizer_version="09",
        corpus_versions=["05"],
    ),
    "34": SparseFirstOrderMarkovModel(
        version="34",
        tokenizer_version="12",
        corpus_versions=["05"],
    ),
    "35": ReverseFirstOrderMarkovModel(
        version="35",
        tokenizer_version="12",
        corpus_versions=["05"],
    ),
    "36": SparseFirstOrderMarkovModel(
        version="36",
        tokenizer_version="13",
        corpus_versions=["05"],
    ),
    "37": ReverseFirstOrderMarkovModel(
        version="37",
        tokenizer_version="13",
        corpus_versions=["05"],
    ),
}
