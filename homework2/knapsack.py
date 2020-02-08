"""Module for the Instance class.
"""
from random import randint

from item import Item
from file_handling import getFilePath, generateFileName

class Knapsack:
    '''Data of a basic Knapsack problem: number of items, knapsack's capacity and the items.
    
    Also includes methods to both generate and read an instance saved in a file.'''
    def __init__(self, total_items, capacity, items):
        '''Constructs an Knapsack instance by specifying its data: n items, the capacity and a list of items.
        '''
        self.total_items = total_items
        self.capacity = capacity
        self.items = items

    @classmethod
    def random(cls, total_items, min_weight, max_weight, min_value, max_value, percentage = 0.3):
        '''Constructs an random Knapsack given the number of total items, limits for both values and weights, and an default percentage (0.3) to calculate the capacity.
        '''
        W = total_items * percentage * ((min_weight + max_weight) / 2.0)
        items = [Item(index, randint(min_value, max_value), randint(min_weight, max_weight)) for index in range(total_items)]
        return cls(total_items, W, items)

    @classmethod
    def fromFile(cls, total_items, capacity):
        '''Loads the instance saved in file_name.dat.

        Returns a Knapsack with the instance's data.
        '''
        file_path = getFilePath(generateFileName(total_items, capacity))
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

    def toFile(self):
        '''Saves the instance to a .dat file in the instances/ subdirectory.
        '''
        data = str(self.total_items) + ' ' + str(self.capacity) + '\n'
        data += '\n'.join([str(item) for item in self.items])

        file_path = getFilePath(generateFileName(self.total_items, self.capacity))
        with open(file_path, 'w') as file:
            file.write(data)
