"""This module contains functions for comparing colors."""

import math
from typing import Tuple


def rgb2lab(input_color: Tuple[int, int, int]) -> Tuple[float, float, float]:
    """Converts an RGB color to a CIELAB color."""
    rgb = [prepare_input(x) for x in input_color]

    x = rgb[0] * 0.4124 + rgb[1] * 0.3576 + rgb[2] * 0.1805
    y = rgb[0] * 0.2126 + rgb[1] * 0.7152 + rgb[2] * 0.0722
    z = rgb[0] * 0.0193 + rgb[1] * 0.1192 + rgb[2] * 0.9505
    xyz = [round(x_, 4) for x_ in (x, y, z)]

    xyz[0] = float(xyz[0]) / 95.047  # ref_x =  95.047   observer= 2°, illuminant= d65
    xyz[1] = float(xyz[1]) / 100.0  # ref_y = 100.000
    xyz[2] = float(xyz[2]) / 108.883  # ref_z = 108.883
    xyz = [prepare_output(x_) for x_ in xyz]

    l_ = (116 * xyz[1]) - 16
    a = 500 * (xyz[0] - xyz[1])
    b = 200 * (xyz[1] - xyz[2])
    return round(l_, 4), round(a, 4), round(b, 4)


def prepare_output(value):
    """Prepare the output value."""
    if value > 0.008856:
        value **= 0.3333333333333333
    else:
        value = (7.787 * value) + (16 / 116)
    return value


def prepare_input(value):
    """Prepare the input value."""
    value = float(value) / 255
    if value > 0.04045:
        value = ((value + 0.055) / 1.055) ** 2.4
    else:
        value /= 12.92
    return value * 100


def delta_e(lab1: Tuple[float, float, float], lab2: Tuple[float, float, float]):
    """Calculate the color difference between two CIELAB colors."""
    return math.sqrt((lab2[0] - lab1[0]) ** 2 + (lab2[1] - lab1[1]) ** 2 + (lab2[2] - lab1[2]) ** 2)


def srgb(rgb1: Tuple[float, float, float], rgb2: Tuple[float, float, float]):
    """Calculate the color difference between two sRGB colors."""
    if rgb1[0] + rgb2[0] < 256:
        return math.sqrt(
            2 * ((rgb1[0] - rgb2[0]) ** 2) + 4 * ((rgb1[1] - rgb2[1]) ** 2) + 3 * ((rgb1[2] - rgb2[2]) ** 2)
        )
    return math.sqrt(3 * ((rgb1[0] - rgb2[0]) ** 2) + 4 * ((rgb1[1] - rgb2[1]) ** 2) + 2 * ((rgb1[2] - rgb2[2]) ** 2))
