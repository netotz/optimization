"""Module for reading and writing files that contain instances of a Knapsack problem.
"""
from os.path import dirname, join

def generateFileName(total_items, capacity, index = 0):
    '''Generates a name for the file which will store the n items and capacity of an instance.

    The index parameter distinguishes instances of same size.
    '''
    return '_'.join([str(total_items), str(capacity), str(index)]) + '.dat'

def getInstancePath(file_name):
    '''Returns the path of file_name.
    '''
    subdirectory = dirname(__file__)
    file_path = join(subdirectory, 'instances/{}.dat'.format(file_name))
    return file_path