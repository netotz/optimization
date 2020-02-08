"""Module for the Instance class.
"""

class Instance:
    '''Contains the data of a Knapsack problem instance: number of items, knapsack's capacity and the items.
    '''
    def __init__(self, n, capacity, items):
        self.total_items = n
        self.capacity = capacity
        self.items = items