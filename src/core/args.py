"""
Package: core
Authors: Matej Hrabal, Patrik Holop
About: Argument parser
"""


import sys, os


def check_args():
    """Checks number of arguments"""
    if len(sys.argv) != 3:
        print("Usage: python3 Path_to_TIFF Path_to_CSV")
        exit(1)


def get_path_img():
    """ Gets TIFF file from args"""
    check_args()
    if os.path.exists(sys.argv[1]):
        return sys.argv[1]
    else:
        print("Usage: python3 Path_to_TIFF Path_to_CSV")
        exit(1)


def get_path_csv():
    """Gets CSV from args"""
    return sys.argv[2]