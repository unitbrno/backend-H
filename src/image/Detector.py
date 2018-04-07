import numpy as np
import src.core.io as io
from PIL import Image
from src.image.thresholding import Threshold


class Detector:

    pixel_type = dict(ball=255, background=0, actual=100, visited=200, gray=128, selected=10)

    def __init__(self, image_vector):
        try:
            self.image = Threshold(image_vector).get_image()
        except TypeError:
            exit(1)
        self.width = len(self.image)
        self.height = len(self.image[0])
        io.show_image(Image.fromarray(self.image))
        self.solve_gray()
        io.show_image(Image.fromarray(self.image))

    def solve_gray(self):
        """
        Najde vsechny nerozhodne oblasti
        :return:
        """
        for x in range(self.width):
            for y in range(self.height):
                if self.image[x][y] == self.pixel_type['gray']:
                    self.balance(x, y)

    def balance(self, start_x, start_y):
        """
        Rozhodne nejiste oblasti
        :param start_x:
        :param start_y:
        :return:
        """
        white_counter = 0
        black_counter = 0

        queue = [(start_x, start_y)]

        while queue:
            front = queue.pop(0)
            x = front[0]
            y = front[1]
            if self.image[x][y] != self.pixel_type['gray']:
                continue

            self.image[x][y] = self.pixel_type['selected']

            if x + 1 < self.width:
                if self.image[x + 1][y] == self.pixel_type['ball']:
                    white_counter += 1
                elif self.image[x + 1][y] == self.pixel_type['background']:
                    black_counter += 1
                queue.append((x + 1, y))

            if x > 0:
                if self.image[x - 1][y] == self.pixel_type['ball']:
                    white_counter += 1
                elif self.image[x - 1][y] == self.pixel_type['background']:
                    black_counter += 1
                queue.append((x - 1, y))

            if y + 1 < self.height:
                if self.image[x][y + 1] == self.pixel_type['ball']:
                    white_counter += 1
                elif self.image[x][y + 1] == self.pixel_type['background']:
                    black_counter += 1
                queue.append((x, y + 1))

            if y > 0:
                if self.image[x][y - 1] == self.pixel_type['ball']:
                    white_counter += 1
                elif self.image[x][y - 1] == self.pixel_type['background']:
                    black_counter += 1
                queue.append((x, y - 1))

        color = self.pixel_type['background']
        if white_counter > black_counter * 0.7:
            color = self.pixel_type['ball']

        queue = [(start_x, start_y)]
        while queue:
            front = queue.pop(0)
            x = front[0]
            y = front[1]
            if self.image[x][y] != self.pixel_type['selected']:
                continue

            self.image[x][y] = color

            if x + 1 < self.width:
                queue.append((x + 1, y))
            if x > 0:
                queue.append((x - 1, y))
            if y + 1 < self.height:
                queue.append((x, y + 1))
            if y > 0:
                queue.append((x, y - 1))

    def wave(self, start_x, start_y):
        """
        Najde a oznaci jednu kouli
        :param start_x: souradnice bodu, ktery patri kouli
        :param start_y: souradnice bodu, ktery patri kouli
        :return: souradnice obalky, ve ktere lezi koule
        """
        max_x = 0
        min_x = self.width
        max_y = 0
        min_y = self.height

        queue = [(start_x, start_y)]

        while queue:
            front = queue.pop(0)
            x = front[0]
            y = front[1]
            if self.image[x][y] != self.pixel_type['ball']:
                continue

            self.image[x][y] = self.pixel_type['actual']

            if x + 1 < self.width:
                queue.append((x + 1, y))
            if x > 0:
                queue.append((x - 1, y))
            if y + 1 < self.height:
                queue.append((x, y + 1))
            if y > 0:
                queue.append((x, y - 1))

            max_x = max(max_x, x)
            min_x = min(min_x, x)
            max_y = max(max_y, y)
            min_y = min(min_y, y)

        # removes small objects
        if max_x - min_x <= 10 or max_y - min_y <= 10:
            max_x = self.width

        return dict(max_x=max_x, min_x=min_x, max_y=max_y, min_y=min_y)

    def copy_ball(self, **kwargs):
        """
        Vrati 2D pole bool hodnot koule,
        :return: 2D pole bool hodnot, True pro okraje
        """
        min_x = kwargs['min_x']
        max_x = kwargs['max_x']
        min_y = kwargs['min_y']
        max_y = kwargs['max_y']
        ball = []
        for _ in range(min_x, max_x + 1):
            ball.append([150] * ((max_y - min_y) + 1))        # TODO

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if self.image[x][y] == self.pixel_type['actual']:
                    if self.is_border(x, y, max_x, max_y):
                        ball[x - min_x][y - min_y] = True
                    self.image[x][y] = self.pixel_type['visited']
        # io.show_image(Image.fromarray(np.array(ball).astype(np.uint8), mode='L'))
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
        return x < width and self.image[x + 1][y] == self.pixel_type['background'] \
            or x > 0 and self.image[x - 1][y] == self.pixel_type['background'] \
            or y < height and self.image[x][y + 1] == self.pixel_type['background'] \
            or y > 0 and self.image[x][y - 1] == self.pixel_type['background'] \
            or x == width or y == height

    @property
    def balls(self):
        """
        Vrati obrysy svetlich objektu na tmavem pozadi
        :return: pole 2D poli kouli
        """
        balls = []
        for x in range(self.width):
            for y in range(self.height):
                if self.image[x][y] == self.pixel_type['ball']:
                    dct = self.wave(x, y)
                    if dct['max_x'] + 1 < self.width and dct['min_x'] > 0 \
                            and dct['max_y'] + 1 < self.height and dct['min_y'] > 0:
                        balls.append(self.copy_ball(**dct))
        return balls
