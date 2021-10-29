import numpy as np


def delta_e_cie1976(lab1: np.array, lab2: np.array) -> float:
    """
    reference: http://www.brucelindbloom.com/Eqn_DeltaE_CIE76.html
    """
    return np.sqrt(np.sum((lab1 - lab2) ** 2))
