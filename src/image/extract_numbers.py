"""
Author: Patrik Holop
About: Module that extracts output information
       Sphere vector's shape:
         {[[T,F,T], [F,F,T], ...} where T means border pixel,
                                        F inside of outside pixel
"""


import math
from src.core.io import get_image_vector


testing_matrix = {((True,True,True,True),
                   (True,False,False,True),
                   (True,False,False,True),
                   (True,True,True,True))}


def get_width(sphere):
    """Get width of sphere vector"""
    return len(sphere[0])


def get_height(sphere):
    """Get width of sphere vector"""
    return len(sphere)


def get_max_width(sphere):
    """Get maximum width of sphere"""
    total_max = 0
    x_min = 0
    x_max = 0
    y_min = 0
    y_max = 0

    for i in range(len(sphere)):
        for j in range(len(sphere[0])):
            x,y = i,j
            max_dist = 0
            if sphere[x][y]:
                for i2 in range(i+1):
                    for j2 in range(j+1):
                        if sphere[i2][j2]:
                            length = math.sqrt((i2-i)**2 + (j2-j)**2)
                            max_dist = max(max_dist, length)
                            x_min = i
                            y_min = j
                            x_max = i2
                            y_max = j2
                total_max = max(total_max, max_dist)
    print(total_max)
    return x_min, y_min, x_max, y_max


def get_max_width(sphere):
    """Get maximum width of sphere"""


matrix = get_image_vector("../../tests/1/particles/00002.bmp", load=True)
x_min, y_min, x_max, y_max = get_max_width(matrix)

'''
for matrix in testing_matrix:
    print(get_height(matrix))
    print(get_width(matrix))
    get_max_width(matrix)
'''



