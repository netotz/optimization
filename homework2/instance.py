"""Module for the Instance class.
"""
from random import randint

from item import Item

class Instance:
    '''Data of a basic Knapsack problem: number of items, knapsack's capacity and the items.
    
    Also includes methods to both generate and read an instance saved in a file.'''
    def __init__(self, n, capacity, items):
        '''Constructs an Instance by specifying its data: n items, the capacity and a list of items.
        '''
        self.total_items = n
        self.capacity = capacity
        self.items = items

    @classmethod
    def generateRandom(cls, total_items, capacity, min_weight, max_weight, min_value, max_value):
        '''Constructs an random Instance.
        '''
        items = list()
        for index in range(total_items):
            value = randint(min_value, max_value)
            weight = randint(min_weight, max_weight)
            items.append(Item(index, value, weight))
        return cls(total_items, capacity, items)