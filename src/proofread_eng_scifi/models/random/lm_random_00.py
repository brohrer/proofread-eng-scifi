import random


def calculate_likelihoods(body_ids):
    # For each token, generate a random number, representing
    # how unexpected it is.
    likelihoods = [random.random() for body_id in body_ids]
    return likelihoods
