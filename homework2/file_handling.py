"""Module for reading and writing files that contain instances of a Knapsack problem.
"""
from os.path import dirname, join

def generateFileName(total_items, capacity, index = 0):
    '''Generates a name for the file which will store the n items and capacity of an instance.

    The index parameter distinguishes instances of same size.
    '''
    file_name = '_'.join([str(total_items), str(capacity), str(index)])
    return file_name
