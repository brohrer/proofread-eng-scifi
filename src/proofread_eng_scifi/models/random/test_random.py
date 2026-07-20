import random
from proofread_eng_scifi.models.random.random import RandomModel, registry

model = registry["00"]


def test_model_creation():
    test_model = RandomModel(
        version="00",
        tokenizer_version="00",
        description="random baseline",
    )
    ids = [1, 2, 3, 4, 5, 6, 7]
    likelihoods = test_model.calculate_likelihoods_from_ids(ids)
    assert len(likelihoods) > 5


def test_likelihood_generation():
    n_ids = 100
    ids = [random.randint(1, 10000) for _ in range(n_ids)]
    likelihoods = model.calculate_likelihoods_from_ids(ids)

    assert len(likelihoods) == 100
    assert max(likelihoods) <= 1.0
    assert min(likelihoods) >= 0.0
