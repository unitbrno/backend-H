import src.core.io as io
from PIL import Image
import numpy as np
from operator import itemgetter

class Threshold(object):
    array = None
    thr_value = None
    histogram = None

    def __init__(self, array):
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

        self.coefficient = 0.75
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
        arraytest = list()
        max_black = self.histogram[70]
        min_white = self.histogram[100]

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


if __name__ == "__main__":
    folder = "8"
    obj = io.load_image("../../tests/" + folder + "/field/0.tif")
    array = io.get_image_vector(obj)
    io.show_image(Image.fromarray(Threshold(array).get_image(), mode='L'))