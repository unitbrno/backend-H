"""
Thresholding module
Author: Halas Timotej
About: Edits image and returns in form so Detector class can detect balls
"""


import numpy as np
from operator import itemgetter


class Threshold(object):
    array = None
    thr_value = None
    histogram = None

    def __init__(self, array):
        """
        This method computes histogram and edit it so image have bigger contrast
        """
        self.array = list(array)
        self.x_s = len(self.array[0])
        self.y_s = len(self.array)
        histogram = [0] * 256
        for row in array:
            for val in row:
                histogram[val] += 1

        self.thr_value, val = max(enumerate(histogram), key=itemgetter(1))

        last_val = None
        first_val = None

        for index, val in enumerate(histogram):
            if val:
                first_val = index
                break

        for index, val in enumerate(reversed(histogram)):
            if val:
                last_val = 255 - index
                break

        self.coefficient = 0.5
        size = last_val - first_val
        middle = round(first_val + size * self.coefficient)
        step = 255 / size

        self.histogram = [0] * 256
        self.histogram[middle] = 128
        last_value = 128
        for i in range(middle, 256):
            last_value += step
            self.histogram[i] = round(last_value) if round(last_value) < 256 else 255
        last_value = 128
        for i in reversed(range(0, middle)):
            last_value -= step
            self.histogram[i] = round(last_value) if round(last_value) >= 0 else 0

    def get_image(self):
        """
        This method finds blacks and whites in picture and sets pixels to:
        Black color 0% ossibility of ball
        Grey color 50% possibility of ball
        White color 100% possibility of ball
        :return: Returns edited image
        """
        arraytest = list()
        max_black = self.histogram[45]
        min_white = self.histogram[90]

        for x, row in enumerate(self.array):
            new_row = list()
            for y, val in enumerate(row):
                # new_row.append(self.histogram[val])
                val = self.histogram[val]
                if val > min_white:
                    new_row.append(255)
                elif val <= max_black:
                    new_row.append(0)
                else:
                    new_row.append(128)
            arraytest.append(new_row)
        return np.array(arraytest).astype(np.uint8)
