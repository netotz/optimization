"""Module for reading and writing files that contain instances of a Knapsack problem.
"""
from os import listdir
from os.path import dirname, join, isfile

def generateFileName(total_items, capacity, index = 0):
    '''Generates a name for the file which will store the n items and capacity of an instance.

    The index parameter distinguishes instances of same size.
    '''
    return str(total_items) + '_' + str(capacity) + '_' + str(index) + '.dat'

def getFilePath(file_name):
    '''Returns the path of file_name.
    '''
    current_directory = dirname(__file__)
    file_path = join(current_directory, 'instances/{}'.format(file_name))
    return file_path

def listFiles():
    '''Returns a list with the .dat files in the instances/ subdirectory.
    '''
    current_directory = dirname(__file__)
    subdirectory = join(current_directory, 'instances\\')
    return [file for file in listdir(subdirectory) if isfile(join(subdirectory, file)) and file[-3:].lower() == 'dat']
