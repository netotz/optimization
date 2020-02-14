"""Module for the Instance class.
"""
from random import randint
from typing import List
from os import stat, makedirs
from os.path import exists

from item import Item
from file_handling import getFilePath, generateFileName

class Knapsack:
    '''Data of a basic Knapsack problem: number of items, knapsack's capacity and the items.
    
    Also includes methods to both generate and read an instance saved in a file.'''
    def __init__(self, total_items, capacity, items: List[Item]):
        '''Constructs an Knapsack instance by specifying its data: n items, the capacity and a list of items.
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
    def items(self) -> List[Item]:
        return self.__items

    @classmethod
    def random(cls, total_items, min_weight, max_weight, min_value, max_value, capacity_percentage = 30):
        '''Constructs an random Knapsack given the number of total items, limits for both values and weights, and an default percentage (0.3) to calculate the capacity.
        '''
        W = total_items * (capacity_percentage / 100.0) * ((min_weight + max_weight) / 2.0)
        # truncate decimals
        capacity = float(format(W, 'g'))
        items = [Item(index, randint(min_value, max_value), randint(min_weight, max_weight)) for index in range(total_items)]
        return cls(total_items, capacity, items)

    @classmethod
    def fromFile(cls, file_name):
        '''Loads the instance saved in file_name.dat.

        Returns a Knapsack with the instance's data.
        '''
        file_path = getFilePath(file_name)
        try:
            if stat(file_path).st_size == 0:
                print('\t{} is empty!'.format(file_name))
                return None
            with open(file_path, 'r') as file:
                items = list()
                first_line = True
                for line in file:
                    if not first_line:
                        index, value, weight = line.split()
                        items.append(Item(int(index),int(value),int(weight)))
                    else:
                        n, W = line.split()
                        first_line = False
            return cls(int(n), float(W), items)
        except FileNotFoundError as error:
            print('\tFile {} not found: {}'.format(file_name, error))
            return None
        except ValueError:
            print('\t{} has invalid format!'.format(file_name))
            return None

    def toFile(self):
        '''Saves the instance to a .dat file in the instances/ subdirectory.
        '''
        data = str(self.total_items) + ' ' + str(self.capacity) + '\n'
        data += '\n'.join([str(item) for item in self.items])

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
        '''Sort items by specified attribute: value = 1, weight = 2 or ratio = 3 (default).
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
        unsorted_items = self.items
        self.__items = sorted(unsorted_items, key = function, reverse = descending)
