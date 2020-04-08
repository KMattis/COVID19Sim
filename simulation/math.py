import randomfile

def truncated_gauss(mu: int, sigma: int, _min: int) -> int:
    return round(max(_min, randomfile.randomgauss(mu, sigma)))