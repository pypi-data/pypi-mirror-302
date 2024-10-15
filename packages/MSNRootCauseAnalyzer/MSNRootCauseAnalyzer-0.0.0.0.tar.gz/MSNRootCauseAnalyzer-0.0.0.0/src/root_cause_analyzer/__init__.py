from .algorithms.adtributor import Adtributor
from .algorithms.r_adtributor import RecursiveAdtributor


def get_analyzer(name):
    if name == 'adtributor':
        return Adtributor()
    elif name == 'r_adtributor':
        return RecursiveAdtributor()
    else:
        raise ValueError(f"Unknown algorithm: {name}, available algorithms: ['adtributor', 'r_adtributor']")