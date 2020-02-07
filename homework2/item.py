"""
Module for the Item class.
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