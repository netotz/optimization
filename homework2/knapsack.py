'''
Module for the Instance class.
'''

from random import randint
from os import stat, makedirs
from os.path import exists
from itertools import tee

from item import Item
from file_handling import getFilePath, generateFileName

class Knapsack:
    '''
    Data of a basic Knapsack problem: number of items, knapsack's capacity and the items.
    
    Also includes methods to both generate and read an instance saved in a file.
    '''
    def __init__(self, total_items, capacity, items):
        '''
        Constructs an Knapsack instance by specifying its data: n items, the capacity and a list of items.
        '''
        self.__total_items = total_items
        self.__capacity = capacity
        self.__items = items

    @property
    def total_items(self):
        return self.__total_items

    @property
    def capacity(self):
        return self.__capacity

    @property
    def items(self):
        return self.__items
    @items.setter
    def items(self, new_items):
        self.__items = new_items

    @classmethod
    def random(cls, total_items, min_weight, max_weight, min_value, max_value, capacity_percentage = 30):
        '''
        Constructs an random Knapsack given the number of total items, limits for both values and weights, and an default percentage (0.3) to calculate the capacity.
        '''
        W = total_items * (capacity_percentage / 100) * ((min_weight + max_weight) / 2)
        # truncate decimals
        capacity = float('%g' % W)

        # create generator expression to iterate over the items
        items = (Item(index, randint(min_value, max_value), randint(min_weight, max_weight)) for index in range(total_items))
        return cls(total_items, capacity, items)

    @classmethod
    def fromFile(cls, file_name):
        '''
        Loads the instance saved in file_name.dat.

        Returns a Knapsack with the instance's data.
        '''
        file_path = getFilePath(file_name)
        try:
            # if file is empty
            if stat(file_path).st_size == 0:
                print('\t{} is empty!'.format(file_name))
                return None
            
            items = list()
            with open(file_path, 'r') as file:
                # read first line which includes number of items and capacity
                n, W = file.readline().rstrip('\n').split()

                items_append = items.append
                # read rest of file (items' data)
                for line in file:
                    index, value, weight = line.split()
                    items_append(Item(int(index), int(value), int(weight)))
            
            return cls(int(n), float(W), (_ for _ in items))
        except FileNotFoundError as error:
            print('\tFile {} not found: {}'.format(file_name, error))
            return None
        except ValueError:
            print('\t{} has invalid format!'.format(file_name))
            return None

    def toFile(self):
        '''
        Saves the instance to a .dat file in the instances/ subdirectory.
        '''
        items_to_write = self.copyItems()
        # concatenate all data to write
        data = f'{self.total_items} {self.capacity}\n'
        data += '\n'.join([str(_) for _ in items_to_write])

        try:
            index = 0
            # loop until a name that doesn't already exist is generated
            while True:
                file_path = getFilePath(generateFileName(self.total_items, self.capacity, index))
                if exists(file_path):
                    index += 1
                else:
                    break
            
            # if instances/ folder doesn't exist, create it
            subdirectory = getFilePath('')
            if not exists(subdirectory):
                makedirs(subdirectory)
                
            with open(file_path, 'w') as file:
                file.write(data)
        except (IOError, OSError, ValueError) as error:
            print("\tInstance could not be saved: {}".format(error))

    def sortItems(self, by):
        '''
        Sort items by specified attribute: value = 1, weight = 2 or ratio = 3 (default).
        '''
        if by == 1:
            function = lambda item: item.value
            descending = True
        elif by == 2:
            function = lambda item: item.weight
            descending = False
        else:
            function = lambda item: item.ratio
            descending = True
        items_to_sort = self.copyItems()
        return sorted(items_to_sort, key = function, reverse = descending)

    def copyItems(self):
        '''
        Returns a copy of self.items.
        '''
        self.items, items_copy = tee(self.items)
        return items_copy
