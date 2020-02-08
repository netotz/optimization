from os import path
from random import randint

from item import Item, Instance

def getInstancePath(file_name):
    '''Returns the path of file_name.
    '''
    subdirectory = path.dirname(__file__)
    file_path = path.join(subdirectory, 'instances/{}.dat'.format(file_name))
    return file_path

def generateInstance(file_name, items, capacity, min_weight, max_weight, min_value, max_value):
    '''Creates a custom instance and saves it to a file_name.dat in the instances/ subdirectory.
    '''
    file_path = getInstancePath(file_name)
    with open(file_path, 'w') as file:
        line = str(items) + ' ' + str(capacity) + '\n'
        file.write(line)
        for index in range(items):
            value = randint(min_value, max_value)
            weight = randint(min_weight, max_weight)
            line = str(index) + ' ' + str(value) + ' ' + str(weight) + '\n'
            file.write(line)

def readInstance(file_name):
    '''Loads the instance's data saved in file_name.dat.

    Returns an object of type Instance.
    '''
    file_path = getInstancePath(file_name)
    with open(file_path, 'r') as file:
        total_items, capacity = list(map(int, file.readline().rstrip('\n').split()))
        items = []
        for _ in range(total_items):
            index, value, weight = file.readline().rstrip('\n').split()
            item = Item(int(index),int(value),int(weight))
            items.append(item)
    return Instance(total_items, capacity, items)