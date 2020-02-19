"""
Module for the heuristic technique to solve a Knapsack problem.
"""

from knapsack import Knapsack
from item import Item

def pickItems(knapsack: Knapsack, heuristic):
    '''
    Use the heuristic specified in the argument to get a solution for the knapsack problem.
    '''
    items_sorted = knapsack.sortItems(heuristic)
    W = knapsack.capacity
    for item in items_sorted:
        weight = item.weight
        if weight <= W:
            # add item to generator expression
            yield item
            W -= weight
            # if no more items fit in the knapsack
            if W == 0:
                break
        # if heuristic by weight is used, the rest of the items won't fit
        elif heuristic == 2:
            break
