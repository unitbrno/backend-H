"""
Package: core
Authors: Matej Hrabal
About: Argument parser
"""


import sys, os

def check_args(argv):
    if (len(argv) != 3):
        print("Usage: python3 Path_to_TIFF Path_to_CSV\n")
        exit()

def get_path_img(argv):
    check_args(argv)
    if (os.path.exists(argv[1])):
        return argv[1]

def get_path_csv(argv):
    check_args(argv)
    return argv[2]






