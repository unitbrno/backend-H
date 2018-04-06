import numpy as np
import src.core.io as io
from PIL import Image
from operator import itemgetter


class Detector:

    pixel_type = dict(ball=255, background=0, actual=100, visited=200)

    def __init__(self, image_vector):
        self.image = image_vector
        self.threshold()

    def threshold(self):
        histogram = [0] * 256
        for row in self.image:
            for val in row:
                histogram[val] += 1

        index, value = max(enumerate(histogram), key=itemgetter(1))
        thr_val = 0
        for i in range(index + 1, len(histogram)):
            if histogram[i] / histogram[i - 1] > 0.8:
                thr_val = i
                break

        arraytest = list()
        for row in self.image:
            new_row = list()
            for val in row:
                new_row.append(255) if val > thr_val * 1.3 else new_row.append(0)
            arraytest.append(new_row)

        self.image = np.array(arraytest).astype(np.uint8)

    def wave(self, x, y):
        """
        Najde a oznaci jednu kouli
        :param x: souradnice bodu, ktery patri kouli
        :param y: souradnice bodu, ktery patri kouli
        :return: souradnice obalky, ve ktere lezi koule
        """
        max_x = 0
        min_x = 1000000000000000
        max_y = 0
        min_y = 1000000000000000

        queue = [[x, y]]

        while queue:
            front = queue.pop(0)
            pixel_x = front[0]
            pixel_y = front[1]
            if self.image[pixel_x][pixel_y] != self.pixel_type['ball']:
                continue

            self.image[pixel_x][pixel_y] = self.pixel_type['actual']

            queue.append([pixel_x + 1, pixel_y])
            queue.append([pixel_x - 1, pixel_y])
            queue.append([pixel_x, pixel_y + 1])
            queue.append([pixel_x, pixel_y - 1])

            max_x = max(max_x, pixel_x)
            min_x = min(min_x, pixel_x)
            max_y = max(max_y, pixel_y)
            min_y = min(min_y, pixel_y)

        return dict(max_x=max_x, min_x=min_x, max_y=max_y, min_y=min_y)

    def copy_ball(self, **kvargs):
        """
        Vrati 2D pole bool hodnot koule,
        :param kvargs:
        :return:
        """
        xx = kvargs['min_x']
        XX = kvargs['max_x']
        yy = kvargs['min_y']
        YY = kvargs['max_y']
        ball = []
        for _ in range(xx - 1, XX):
            ball.append([150] * ((YY - yy) + 1))        # TODO

        for x in range(xx, XX + 1):
            for y in range(yy, YY + 1):
                if self.image[x][y] == self.pixel_type['actual']:
                    if self.is_border(x, y):
                        ball[x - xx][y - yy] = True
                    self.image[x][y] = self.pixel_type['visited']
        io.show_image(Image.fromarray(np.array(ball).astype(np.uint8), mode='L'))
        return ball

    def is_border(self, x, y):
        """
        Vyhodnoti, zda je bod
        :param x: souradnice bodu, ktery patri kouli
        :param y: souradnice bodu, ktery patri kouli
        :return:
        """
        return self.image[x + 1][y] == self.pixel_type['background'] or \
               self.image[x - 1][y] == self.pixel_type['background'] or \
               self.image[x][y + 1] == self.pixel_type['background'] or \
               self.image[x][y - 1] == self.pixel_type['background']

    @property
    def balls(self):
        """
        Vrati obrysy svetlich objektu na tmavem pozadi
        :return: pole 2D poli kouli
        """
        balls = []
        for x in range(len(self.image)):
            for y in range(len(self.image[0])):
                if self.image[x][y] == self.pixel_type['ball']:
                    balls.append(self.copy_ball(**self.wave(x, y)))
        return balls
