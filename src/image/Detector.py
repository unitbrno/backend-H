import numpy as np
import src.core.io as io
from PIL import Image
from src.image.thresholding import Threshold

class Detector:

    pixel_type = dict(ball=255, background=0, actual=100, visited=200, gray=128, selected=10)

    def __init__(self, image_vector):
        self.image = Threshold(image_vector).get_image()
        # io.show_image(Image.fromarray(self.image))
        self.solve_gray()
        # io.show_image(Image.fromarray(self.image))

    def solve_gray(self):
        width = len(self.image)
        height = len(self.image[0])
        for x in range(width):
            for y in range(height):
                if self.image[x][y] == self.pixel_type['gray']:
                    self.balance(x, y, width, height)

    def balance(self, x, y, width, height):
        white_counter = 0
        black_counter = 0

        queue = [[x, y]]

        while queue:
            front = queue.pop(0)
            pixel_x = front[0]
            pixel_y = front[1]
            if self.image[pixel_x][pixel_y] != self.pixel_type['gray']:
                continue

            self.image[pixel_x][pixel_y] = self.pixel_type['selected']

            if pixel_x + 1 < width:
                if self.image[pixel_x + 1][pixel_y] == self.pixel_type['ball']:
                    white_counter += 1
                elif self.image[pixel_x + 1][pixel_y] == self.pixel_type['background']:
                    black_counter += 1
            if pixel_x > 0:
                if self.image[pixel_x - 1][pixel_y] == self.pixel_type['ball']:
                    white_counter += 1
                elif self.image[pixel_x - 1][pixel_y] == self.pixel_type['background']:
                    black_counter += 1
            if pixel_y + 1 < height:
                if self.image[pixel_x][pixel_y + 1] == self.pixel_type['ball']:
                    white_counter += 1
                elif self.image[pixel_x][pixel_y + 1] == self.pixel_type['background']:
                    black_counter += 1
            if pixel_y > 0:
                if self.image[pixel_x][pixel_y - 1] == self.pixel_type['ball']:
                    white_counter += 1
                elif self.image[pixel_x][pixel_y - 1] == self.pixel_type['background']:
                    black_counter += 1

            if pixel_x + 1 < width:
                queue.append([pixel_x + 1, pixel_y])
            if pixel_x > 0:
                queue.append([pixel_x - 1, pixel_y])
            if pixel_y + 1 < height:
                queue.append([pixel_x, pixel_y + 1])
            if pixel_y > 0:
                queue.append([pixel_x, pixel_y - 1])

        color = self.pixel_type['background']
        if white_counter > black_counter * 0.7:
            color = self.pixel_type['ball']

        queue = [[x, y]]
        while queue:
            front = queue.pop(0)
            pixel_x = front[0]
            pixel_y = front[1]
            if self.image[pixel_x][pixel_y] != self.pixel_type['selected']:
                continue

            self.image[pixel_x][pixel_y] = color

            if pixel_x + 1 < width:
                queue.append([pixel_x + 1, pixel_y])
            if pixel_x > 0:
                queue.append([pixel_x - 1, pixel_y])
            if pixel_y + 1 < height:
                queue.append([pixel_x, pixel_y + 1])
            if pixel_y > 0:
                queue.append([pixel_x, pixel_y - 1])

    def wave(self, x, y, width, height):
        """
        Najde a oznaci jednu kouli
        :param x: souradnice bodu, ktery patri kouli
        :param y: souradnice bodu, ktery patri kouli
        :param width: sirka obrazku
        :param height: vyska obrazku
        :return: souradnice obalky, ve ktere lezi koule
        """
        max_x = 0
        min_x = width
        max_y = 0
        min_y = height

        queue = [[x, y]]

        while queue:
            front = queue.pop(0)
            pixel_x = front[0]
            pixel_y = front[1]
            if self.image[pixel_x][pixel_y] != self.pixel_type['ball']:
                continue

            self.image[pixel_x][pixel_y] = self.pixel_type['actual']

            if pixel_x + 1 < width:
                queue.append([pixel_x + 1, pixel_y])
            if pixel_x > 0:
                queue.append([pixel_x - 1, pixel_y])
            if pixel_y + 1 < height:
                queue.append([pixel_x, pixel_y + 1])
            if pixel_y > 0:
                queue.append([pixel_x, pixel_y - 1])

            max_x = max(max_x, pixel_x)
            min_x = min(min_x, pixel_x)
            max_y = max(max_y, pixel_y)
            min_y = min(min_y, pixel_y)

        # removes small objects
        if max_x - min_x <= 10 or max_y - min_y <= 10:
            max_x = width

        return dict(max_x=max_x, min_x=min_x, max_y=max_y, min_y=min_y)

    def copy_ball(self, **kwargs):
        """
        Vrati 2D pole bool hodnot koule,
        :param kvargs: minimalni/maximalni hranice
        :return: 2D pole bool hodnot, True pro okraje
        """
        xx = kwargs['min_x']
        XX = kwargs['max_x']
        yy = kwargs['min_y']
        YY = kwargs['max_y']
        ball = []
        for _ in range(xx, XX + 1):
            ball.append([150] * ((YY - yy) + 1))        # TODO

        for x in range(xx, XX + 1):
            for y in range(yy, YY + 1):
                if self.image[x][y] == self.pixel_type['actual']:
                    if self.is_border(x, y, XX, YY):
                        ball[x - xx][y - yy] = True
                    self.image[x][y] = self.pixel_type['visited']
        #io.show_image(Image.fromarray(np.array(ball).astype(np.uint8), mode='L'))
        return ball

    def is_border(self, x, y, width, height):
        """
        Vyhodnoti, zda je bod
        :param x: souradnice bodu, ktery patri kouli
        :param y: souradnice bodu, ktery patri kouli
        :param width: sirka obrazku
        :param height: vyska obrazku
        :return: True, pokud je hranicni bod
        """
        return x < width and self.image[x + 1][y] == self.pixel_type['background'] or \
               x > 0 and self.image[x - 1][y] == self.pixel_type['background'] or \
               y < height and self.image[x][y + 1] == self.pixel_type['background'] or \
               y > 0 and self.image[x][y - 1] == self.pixel_type['background'] or \
               x == width or y == height

    @property
    def balls(self):
        """
        Vrati obrysy svetlich objektu na tmavem pozadi
        :return: pole 2D poli kouli
        """
        balls = []
        width = len(self.image)
        height = len(self.image[0])
        for x in range(width):
            for y in range(height):
                if self.image[x][y] == self.pixel_type['ball']:
                    dct = self.wave(x, y, width, height)
                    if dct['max_x'] + 1 < width and dct['min_x'] > 0 and dct['max_y'] + 1 < height and dct['min_y'] > 0:
                        balls.append(self.copy_ball(**dct))
        return balls
