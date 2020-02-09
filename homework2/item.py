"""
Module for the Item class.
"""

class Item:
    def __init__(self, index, value, weight):
        '''Construct an Item object by its value, its weight and an index to identify it.
        '''
        self.__index = index
        self.__value = value
        self.__weight = weight
        self.__ratio = value / weight
    
    @property
    def index(self):
        return self.__index
    
    @property
    def value(self):
        return self.__value
    
    @property
    def weight(self):
        return self.__weight

    @property
    def ratio(self):
        return self.__ratio

    def __str__(self):
        '''To String method.
        '''
        return str(self.index) + ' ' + str(self.value) + ' ' + str(self.weight)
