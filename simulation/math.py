import random

def truncated_gauss(mu, sigma, _min):
    return max(_min, random.gauss(mu, sigma))