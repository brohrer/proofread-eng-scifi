import random
from proofread_eng_scifi.models.tokenizer.tokenizer import (
    registry as tokenizer_registry,
)


class RandomModel:
    def __init__(self, version=None, tokenizer_version=None, description=""):
        self.version = version
        # The model doesn't use the tokenizer, but including it
        # so that this model has the same interface as others.
        self.tokenizer_version = tokenizer_version
        self.tokenizer = tokenizer_registry[tokenizer_version]
        self.description = description

    def calculate_likelihoods_from_ids(self, body_ids):
        # For each token, generate a random number, representing
        # how unexpected it is.
        likelihoods = [random.random() for body_id in body_ids]
        return likelihoods


registry = {
    "00": RandomModel(
        version="00",
        tokenizer_version="00",
        description="random baseline",
    )
}
