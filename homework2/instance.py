"""Module for the Instance class.
"""

class Instance:
    '''Data of a basic Knapsack problem: number of items, knapsack's capacity and the items.
    
    Also includes methods to both generate and read an instance saved in a file.'''
    def __init__(self, n, capacity, items):
        self.total_items = n
        self.capacity = capacity
        self.items = items
