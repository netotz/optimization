from random import randint

from item import Item, Instance

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
        items = list()
        first_line = True
        for line in file:
            if not first_line:
                index, value, weight = line.split()
                item = Item(int(index),int(value),int(weight))
                items.append(item)
            else:
                total_items, capacity = line.split()
                first_line = False
    return Instance(int(total_items), int(capacity), items)