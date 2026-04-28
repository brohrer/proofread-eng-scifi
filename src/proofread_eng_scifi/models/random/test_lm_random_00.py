import random
import proofread_eng_scifi.models.random.lm_random_00 as lm


def test_likelihood_generation():
    n_ids = 100
    ids = [random.randint(1, 10000) for _ in range(n_ids)]
    likelihoods = lm.calculate_likelihoods(ids)

    assert len(likelihoods) == 100
    assert max(likelihoods) <= 1.0
    assert min(likelihoods) >= 0.0
