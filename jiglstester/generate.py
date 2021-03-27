from itertools import product


def permutations(componentdict):
    for v in product(*componentdict.values()):
        yield dict(zip(componentdict, v))