"""
A script for exploring and illustrating the text chunks that a tokenizer learns.
"""

import random
from proofread_eng.models.tokenizer.tokenizer import registry

n_samples = 100
versions = ["05", "06", "07", "08", "09", "11", "12", "13"]

for version in versions:
    tok = registry[version]
    vocab_size = tok.get_piece_size()
    print()
    print(f"================  version {version} with size {vocab_size}")
    for _ in range(n_samples):
        piece_id = random.randrange(vocab_size)
        print(f"{tok.decode_ids([piece_id])}")
