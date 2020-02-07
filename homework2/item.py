"""
Module for the Item and the Instance classes.
"""

class Item:
    def __init__(self, index, value, weight):
        '''Construct an Item object by its value, its weight and an index to identify it.
        '''
        self.index = index
        self.value = value
        self.weight = weight
        self.ratio = value / weight
    def __str__(self):
        '''To String method.
        '''
        attributes = [
            str(self.index),
            str(self.value),
            str(self.weight),
            str(self.ratio)
        ]
        return ' '.join(attributes)

class Instance:
    '''Contains the data of a Knapsack problem instance: number of items, knapsack's capacity and the items.
    '''
    def __init__(self, n, capacity, items):
        self.total_items = n
        self.capacity = capacity
        self.items = items