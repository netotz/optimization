from os import path
from random import randint

def getInstancePath(file_name):
    '''Retrieves the path of the instance file.
    '''
    subdirectory = path.dirname(__file__)
    file_path = path.join(subdirectory, 'instances/{}.dat'.format(file_name))
    return file_path

def generateInstance(items, capacity, min_weight, max_weight, min_value, max_value):
    '''Creates a custom instance and saves it to a .dat file in the instances/ subdirectory.
    '''
    file_path = getInstancePath('test2')
    with open(file_path, 'w') as file:
        line = str(items) + ' ' + str(capacity) + '\n'
        file.write(line)
        for index in range(items):
            value = randint(min_value, max_value)
            weight = randint(min_weight, max_weight)
            line = str(index) + ' ' + str(value) + ' ' + str(weight) + '\n'
            file.write(line)