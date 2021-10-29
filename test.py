"""
convert color in different color space
"""
import numpy as np

from srgb_to_xyz import srgb_to_xyz
from xyz_to_lab import xyz_to_lab, ReferenceWhite
from delta_e import delta_e_cie1976


if __name__ == "__main__":
    srgb = [
        np.array([0xC9, 0xC4, 0xBE]) / 255.0,
        np.array([0xC6, 0xC4, 0xC5]) / 255.0
    ]
    xyz = [srgb_to_xyz(x) for x in srgb]
    d65 = ReferenceWhite.D65
    lab = [xyz_to_lab(x, d65) for x in xyz]

    for i in range(len(srgb)):
        print(srgb[i], xyz[i], lab[i])

    delta_e = delta_e_cie1976(lab[0], lab[1])
    print(delta_e)
