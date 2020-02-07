from os import path
from random import randint
from item import Item

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
    '''Loads the instance saved in file_name.dat.

    Returns a tuple of 3 elements: the number of items, the capacity and the list of the items.
    '''
    file_path = getInstancePath(file_name)
    with open(file_path, 'r') as file:
        total_items, capacity = file.readline().split()
        items = []
        for _ in range(int(total_items)):
            raw_item = file.readline().rstrip('\n').split()
            item = Item(int(raw_item[0]), int(raw_item[1]), int(raw_item[2]))
            items.append(item)
    return (total_items, capacity, items)