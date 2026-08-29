"""
A base class, ready for extension as a nth-order Markov chain model.

Note: Because these models can occupy GB of memory, this model family is
designed to initialize and load them lazily, only when they are needed for
training or inference. This means that the first time they run can
include a long startup time, especially if they haven't been trained yet.
"""

import os
import pickle

from proofread_eng.data.train.registry import registry as training_data_registry
from proofread_eng.models.tokenizer.tokenizer import (
    registry as tokenizer_registry,
)


class MarkovBase:
    def __init__(
        self,
        version=None,
        tokenizer_version=None,
        corpus_versions=None,
        description="",
        transition_probability_floor=1e-9,
        epsilon=1e-10,
        not_empty_threshold=50,
        verbose=True,
    ):
        self.version = version
        self.corpus_versions = corpus_versions
        self.tokenizer_version = tokenizer_version
        self.tokenizer = tokenizer_registry[self.tokenizer_version]
        self.n_unique_tokens = self.tokenizer.get_piece_size()
        self.transition_probability_floor = transition_probability_floor
        self.epsilon = epsilon
        self.not_empty_threshold = not_empty_threshold
        self.description = description
        self.model_filename = self.version + ".pkl"
        self.model_dir = os.path.dirname(__file__)
        self.model_path = os.path.join(self.model_dir, self.model_filename)
        self.verbose = verbose

    def train(self):
        if self.verbose:
            print()
            print(f"Training {self.description} v{self.version} ...")

        self._initialize()
        for corpus_version in self.corpus_versions:
            corpus = training_data_registry[corpus_version]
            for training_text in corpus.get_text_files(verbose=self.verbose):
                ids = self.tokenizer.encode_as_ids(training_text)
                self._train_from_tokens(ids)

        # If there is a _tune() function, call it
        try:
            self._tune()
        except AttributeError:
            pass

        self._save()

    def calculate_likelihoods(self, text, alpha=None, beta=None):
        ids = self.tokenizer.encode_as_ids(text)
        return self.calculate_likelihoods_from_ids(ids, alpha, beta)

    def calculate_likelihoods_from_ids(self, ids, alpha=None, beta=None):
        """
        Rely on lazy training. Don't train until the model is requested
        to start calculating likelihoods.
        """
        # If the model isn't ready yet, try to load it.
        # If that doesn't work, train it fresh.
        if not self.is_ready():
            try:
                print(f"attempting to load model {self.version}")
                model = self._load()
                self.__dict__.update(model.__dict__)
                # Catch the case of loading an empty model
                if model is None or not model.is_ready():
                    print(
                        "loading was not successful. retraining from scratch."
                    )
                    self.train()
            except FileNotFoundError:
                print("model not found. retraining from scratch.")
                self.train()
        if alpha is None and beta is None:
            return self._calc_likelihoods(ids)
        else:
            return self._calc_likelihoods(ids, alpha, beta)

    def _initialize(self):
        raise NotImplementedError

    def _train_from_tokens(self, ids):
        raise NotImplementedError

    def _calc_likelihoods(self, ids):
        raise NotImplementedError

    def is_ready(self):
        # Check whether the model is trained and loaded
        raise NotImplementedError

    def _save(self):
        with open(self.model_path, "wb") as f:
            pickle.dump(self, f)

    def _load(self):
        with open(self.model_path, "rb") as f:
            model = pickle.load(f)
        return model

    def delete(self):
        # Remove memory footprint
        raise NotImplementedError
