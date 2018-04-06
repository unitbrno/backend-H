"""
Package: core
Authors: Patrik Holop
About: Basic function used in project
Usage examples:
    1)
    obj = load_image("../../tests/1/field/0.tif")
    show_image(obj)
    2)
    vector = get_image_vector("../data/obj.tif", load=True)
"""


import numpy as np
from PIL import Image


def load_image(filename):
    """Loads image into memory
    :return Image object
    """
    return Image.open(filename)


def get_image_vector(obj, load=False):
    """Gets number vector from obj"""
    object = load_image(obj) if load else obj
    return np.array(object)


def show_image(obj):
    """Shows image"""
    obj.show()


