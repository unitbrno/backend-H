"""
Testing module
Author: Patrik Holop
About: Modules provide function to calculate general error of extractor
"""


import csv
import numpy as np


def compare_results(list1, list2):
    """Function compares 2 lists
    :param list1 list of results
    :param list2 list of results
    :return total error
    """
    first = np.array([float(x) for x in list1])
    second = np.array([float(x) for x in list2])
    print(first-second)
    return sum(abs(first-second))


def compare_files(filename1, filename2, ind):
    """Function compares 2 files
    :param filename1: Name of the file
    :param filename2: Name of the file
    :return total error
    """
    total_error = 0

    with open(filename1, 'r') as csvfile, open(filename2, 'r') as csvfile2:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        spamreader2 = csv.reader(csvfile2, delimiter=',', quotechar='|')
        counter = 0
        for row1, row2 in zip(spamreader, spamreader2):
            if counter == 0:
                counter += 1
                continue
            total_error += compare_results(row1, row2)

    print("Total Error ", ind, ":", total_error, "\n")
    return total_error




