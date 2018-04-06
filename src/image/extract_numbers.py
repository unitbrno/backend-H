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
                            if length>max_dist:
                                max_dist = length
                                x_min = i
                                y_min = j
                                x_max = i2
                                y_max = j2
                total_max = max(total_max, max_dist)

    return (x_min, y_min), (x_max, y_max)


def putpixel(x, y, matrix, abs_vector):

    x = int(x)
    y = int(y)

    if (x>=0) and (y>=0) and x < get_height(matrix) and y < get_width(matrix):
        b_point_1 = (x+abs_vector[0], y+abs_vector[1])
        b_point_2 = (x-abs_vector[0], y-abs_vector[1])

        points = get_normal_max(matrix, b_point_1, b_point_2)

        i = 0
        j = 0
        lengths = []
        z = 0
        while z < len(points)-1:
            i = points[z]
            j = points[z+1]
            lengths.append(math.sqrt((j[0]-i[0])**2+(j[1]-i[1])**2))
            z += 1
        if len(lengths) == 0:
            return 0
        return max(lengths)
    return 0


def putpixel2(x, y, matrix, state):
    x = int(x)
    y = int(y)

    if state == True:
        if (x>=0) and (y>=0) and x < get_height(matrix) and y < get_width(matrix):
            if matrix[x][y]==True:
                return (False, (x,y))
    else:
        if (x>=0) and (y>=0) and x < get_height(matrix) and y < get_width(matrix):
            if matrix[x][y] == True:
                return (True, (x,y))
    return None


def get_thickness(sphere, point1, point2):
    """Get maximum width of sphere"""
    absolute_vector = (point2[0]-point1[0], point2[1]-point1[1])
    normal_vector = (-absolute_vector[1], absolute_vector[0])

    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    lengths = []

    dx = x2 - x1
    dy = y2 - y1

    j = False
    if abs(dy) > abs(dx):
        j = True
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    if x1>x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    if dx == 0 and dy == 0:
        lengths.append(putpixel(x1, y1, sphere, normal_vector))
        return
    dx = x2 - x1
    dy = y2 - y1
    k = dy / dx
    y = y1
    for x in range(x1, x2+1):
        if j:
            lengths.append(putpixel(y, x, sphere, normal_vector))
        else:
            lengths.append(putpixel(x, y, sphere, normal_vector))
            y += k

    if len(lengths) == 0:
        return 0
    return max(lengths)


def get_normal_max(sphere, point1, point2):
    """Get maximum width of sphere"""

    state = False
    points = []

    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]

    dx = x2 - x1
    dy = y2 - y1

    j = False
    if abs(dy) > abs(dx):
        j = True
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    if x1>x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    if dx == 0 and dy == 0:
        ret = putpixel2(x1, y1, sphere, state)
        if ret is not None:
            state = ret[0]
            points.append(ret[1])
        return
    dx = x2 - x1
    dy = y2 - y1
    k = dy / dx
    y = y1
    for x in range(x1, x2+1):
        if j:
            ret = putpixel2(y, x, sphere, state)
            if ret is not None:
                points.append(ret[1])
        else:
            ret = putpixel2(x, y, sphere, state)
            if ret is not None:
                state = ret[0]
                points.append(ret[1])
            y += k

    return points


matrix = get_image_vector("../../tests/1/particles/00002.bmp", load=True)
p1, p2 = get_max_width(matrix)
p1 = (168, 73)
p2 = (1, 67)
length = get_thickness(matrix, p1, p2)
print(length)

'''
for matrix in testing_matrix:
    print(get_height(matrix))
    print(get_width(matrix))
    p1, p2 = get_max_width(matrix)
    print(get_thickness(matrix, p1, p2))
'''
