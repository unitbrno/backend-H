"""
Author: Patrik Holop, Matej Hrabal
About: Module that extracts output information from recognized patterns
       Input sphere vector's shape:
       {[[T,F,T], [F,F,T], ...} where T means border pixel,
                                      F inside of outside pixel
"""


import math
from src.image.Detector import Detector
from src.core.io import get_image_vector, write_to_csv
from src.core.args import get_path_csv, get_path_img


def get_width(sphere):
    """Get width of sphere vector
    :param sphere: matrix representing circle
    :return width of matrix
    """
    return len(sphere[0])


def get_height(sphere):
    """Get width of sphere vector
    :param sphere: matrix representing circle
    :return height of matrix
    """
    return len(sphere)


def get_max_width(sphere):
    """Get maximum width of sphere
    :param sphere: matrix representing circle
    :return max width of circle
    """
    true_vector = []
    for i in range(len(sphere)):
        for j in range(len(sphere[0])):
            if sphere[i][j] == True:
                true_vector.append((i,j))
    max_dist = 0
    x_min = 0
    x_max = 0
    y_min = 0
    y_max = 0
    i = 0
    j = 0

    for i in range(0, len(true_vector), 5):
        for j in range(i+1, len(true_vector), 5):
            length = math.sqrt((true_vector[i][0] - true_vector[j][0])**2 + (true_vector[i][1] - true_vector[j][1])**2)
            if length > max_dist:
                max_dist = length
                x_min = true_vector[i][0]
                y_min = true_vector[i][1]
                x_max = true_vector[j][0]
                y_max = true_vector[j][1]

    return max_dist, (x_min, y_min), (x_max, y_max)


def call_normal_vector(x, y, matrix, abs_vector):
    """For one point on the main line between points with the highest distance
       calculates the highest distance between points on it's normale vector
       :param x: x coordinate
       :param y: y coordinate
       :param matrix: matrix representing sphere
       :param abs_vector: normale vector
       :return maximum distance of normalne vector of point
    """

    x = int(x)
    y = int(y)

    # if the point lies in the matrix borders
    if (x >= 0) and (y >= 0) and x < get_height(matrix) and y < get_width(matrix):
        # calculate it's normale vector
        b_point_1 = (x+abs_vector[0], y+abs_vector[1])
        b_point_2 = (x-abs_vector[0], y-abs_vector[1])

        # get max distance on normale
        points = get_normal_points(matrix, b_point_1, b_point_2)

        i = 0
        j = 0
        lengths = []
        z = 0
        # iterate through even and odd indexes and calcutes euklid distances
        while z < len(points)-1:
            i = points[z]
            j = points[z+1]
            lengths.append(math.sqrt((j[0]-i[0])**2+(j[1]-i[1])**2))
            z += 1

        # if not correct shape, return min
        if len(lengths) == 0:
            return 0
        return max(lengths)
    return 0


def extract_border_point(x, y, matrix, state):
    """Decides, whether point is not is not inversible point in length measurement in normale vector
    :param x: x coordinate
    :param y: y coordinate
    :param matrix: matrix representing sphere
    :param state: which border point is given
    :return (next_state, border_point)
    """
    x = int(x)
    y = int(y)

    if state == True:
        # if point meets requeirements
        if x >= 0 and y >= 0 and x < get_height(matrix) and y < get_width(matrix):
            # must be border point
            if matrix[x][y] == True:
                return (False, (x,y))
    else:
        if x >= 0 and y >= 0 and x < get_height(matrix) and y < get_width(matrix):
            if matrix[x][y] == True:
                return (True, (x,y))
    # if not requirements are met, None is returned
    return None


def get_thickness(sphere, point1, point2):
    """Get maximum thickness of sphere
    :param sphere: matrix representing point
    :param point1: starting point of line
    :param point2: ending point of line
    :return Maximum thickness of function
    """
    absolute_vector = (point2[0]-point1[0], point2[1]-point1[1])
    normal_vector = (-absolute_vector[1], absolute_vector[0])

    # initial points
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    lengths = []

    # derivatives
    dx = x2 - x1
    dy = y2 - y1

    # DDA algorithm
    j = False
    if abs(dy) > abs(dx):
        j = True
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    if dx == 0 and dy == 0:
        # line is one point
        lengths.append(call_normal_vector(x1, y1, sphere, normal_vector))
        return
    dx = x2 - x1
    dy = y2 - y1
    k = dy / dx
    y = y1
    for x in range(x1, x2+1):
        if j:
            lengths.append(call_normal_vector(y, x, sphere, normal_vector))
        else:
            lengths.append(call_normal_vector(x, y, sphere, normal_vector))
            y += k

    if len(lengths) == 0:
        return 0
    return max(lengths)


def get_normal_points(sphere, point1, point2):
    """Gets all border points on normale vector line
    :param sphere: Matrix representing function
    :param point1: Starting point of normale
    :param point2: Ending point of normale
    :return list of border points
    """

    state = False
    points = []

    # initial points
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]

    #derivatives
    dx = x2 - x1
    dy = y2 - y1

    # DDA algorithm for normale line
    j = False
    if abs(dy) > abs(dx):
        j = True
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    if x1>x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    if dx == 0 and dy == 0:
        # line is just one point
        ret = extract_border_point(x1, y1, sphere, state)
        if ret is not None:
            state = ret[0]
            points.append(ret[1])
        return []
    dx = x2 - x1
    dy = y2 - y1
    k = dy / dx
    y = y1
    # iterate through points on line
    for x in range(x1, x2+1):
        if j:
            ret = extract_border_point(y, x, sphere, state)
            if ret is not None:
                points.append(ret[1])
        else:
            ret = extract_border_point(x, y, sphere, state)
            if ret is not None:
                state = ret[0]
                points.append(ret[1])
            y += k
    return points


# main program

tiff_filename = get_path_img()
csv_filename = get_path_csv()

matrixes = get_image_vector(tiff_filename, load=True)
dec = Detector(matrixes)

i = 1
results = []
for matrix in dec.balls:
    width = get_width(matrix)
    height = get_height(matrix)
    if width*height > 100:
        dist, p1, p2 = get_max_width(matrix)
        length = get_thickness(matrix, p1, p2)
        dist = round(dist, 3)
        length = round(length, 3)
        results.append([i, width, height, dist, length])
        i += 1

write_to_csv(results, csv_filename)