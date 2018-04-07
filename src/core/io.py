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
import csv
from PIL import Image


def load_image(filename):
    """Loads image into memory
    :param filename: Name of the file
    :return Image object
    """
    return Image.open(filename)


def get_image_vector(obj, load=False):
    """Gets number vector from obj
    :param obj filename or image object
    :param load: if obj is filename, load from file
    :return Image vector
    """
    object = load_image(obj) if load else obj
    return np.array(object)


def show_image(obj):
    """Shows image
    :param obj Image object
    """
    obj.show()


def write_to_csv(array, filename):
    """Writes statistics to file
    :param array: Array with results
    :param filename: Name of the file
    """
    with open(filename, 'w') as file:
        spamwriter = csv.writer(file, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["Part #", "Width", "Height", "Max Length", "Thickness"])
        for line in array:
            spamwriter.writerow(line)
