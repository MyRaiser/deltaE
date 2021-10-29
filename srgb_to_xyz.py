"""
reference: https://en.wikipedia.org/wiki/SRGB
"""

import numpy as np


def __inverse_gamma_expansion_srgb(x: float):
    """
    :param x: each channel in srgb, nominal
    :return: linear value
    """
    if x > 0.04045:
        return ((x + 0.055) / 1.055) ** 2.4
    else:
        return x / 12.92


inverse_gamma_expansion_srgb = np.vectorize(__inverse_gamma_expansion_srgb, otypes=[np.float64])


def srgb_to_xyz(srgb: np.array) -> np.array:
    """
    :param srgb: [r, g, b], normalized, each channel ranges in [0, 1]
    :return: [x, y, z], normalized, each channel ranges in [0, 1]
    """

    # Step1: srgb -> linear rgb
    linear_srgb = inverse_gamma_expansion_srgb(srgb)

    # Step 2: linear rgb -> xyz
    # matrix M according to http://www.brucelindbloom.com/Eqn_RGB_XYZ_Matrix.html
    m_srgb = np.array(
        [[0.4124564, 0.3575761, 0.1804375],
         [0.2126729, 0.7151522, 0.0721750],
         [0.0193339, 0.1191920, 0.9503041]]
    )
    return m_srgb @ linear_srgb
