"""
CIE 1976 (L*, a*, b*)
reference: https://en.wikipedia.org/wiki/CIELAB_color_space#From_CIEXYZ_to_CIELAB
"""

import numpy as np
from enum import Enum
from functools import partial


class ReferenceWhite(Enum):
    D65 = "D65"
    D50 = "D50"


__reference_white_xyz = {
    ReferenceWhite.D65: (95.0489, 100, 108.8840),
    ReferenceWhite.D50: (96.4212, 100, 82.5188)
}


def get_reference_white_xyz(white: ReferenceWhite) -> np.array:
    """returns *normalized* xyz of reference white"""
    if white in __reference_white_xyz:
        # be careful with the normalization "/ 100"
        # it's not mentioned in reference
        return np.array(
            __reference_white_xyz[white]
        ) / 100
    else:
        raise Exception


def __f(epsilon: float, kappa: float, x: float):
    """
    reference: http://www.brucelindbloom.com/index.html?LContinuity.html
    typical value of (epsilon, kappa) is (216/24389, 24389/27)
    """
    if x > epsilon:
        return x ** (1 / 3)
    else:
        return (kappa * x + 16) / 116


f = np.vectorize(
    partial(__f, 216 / 24389, 24389 / 27),
    otypes=[np.float64]
)


def xyz_to_lab(xyz: np.array, white: ReferenceWhite) -> np.array:
    """
    :param white: enum of reference white
    :param xyz: [x, y, z], normalized, each channel ranges in [0, 1]
    :return:
    """

    xyz_rw = get_reference_white_xyz(white)  # reference white
    xyz_r = xyz / xyz_rw  # relative xyz
    f_xyz = f(xyz_r)

    return np.array(
        [
            116 * f_xyz[1] - 16,
            500 * (f_xyz[0] - f_xyz[1]),
            200 * (f_xyz[1] - f_xyz[2])
        ]
    )
