from simulation import random

def truncated_gauss(mu: int, sigma: int, _min: int) -> int:
    return round(max(_min, random.gauss(mu, sigma)))