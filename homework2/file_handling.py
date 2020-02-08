"""Module for reading and writing files that contain instances of a Knapsack problem.
"""
from os.path import dirname, join

def generateFileName(total_items, capacity, index = 0):
    '''Generates a name for the file which will store the n items and capacity of an instance.

    The index parameter distinguishes instances of same size.
    '''
    return str(total_items) + '_' + str(capacity) + '_' + str(index) + '.dat'

def getFilePath(file_name):
    '''Returns the path of file_name.
    '''
    subdirectory = dirname(__file__)
    file_path = join(subdirectory, 'instances/{}'.format(file_name))
    return file_path

def saveInstance(instance):
    '''Saves the Instance object to a .dat file in the instances/ subdirectory.
    '''
    total_items, capacity = instance.total_items, instance.capacity
    data = str(total_items) + ' ' + str(capacity) + '\n'
    data += '\n'.join([str(item) for item in instance.items])

    file_path = getFilePath(generateFileName(total_items, capacity))
    with open(file_path, 'w') as file:
        file.write(data)