"""
Module for the heuristic technique to solve a Knapsack problem.
"""

from time import time

from knapsack import Knapsack
from item import Item

def pickItems(knapsack: Knapsack, heuristic):
    '''
    Use the heuristic specified in the argument to get a solution for the knapsack problem.

    Returns a generator containing the items that were picked.
    '''
    items_sorted = knapsack.sortItems(heuristic)
    W = knapsack.capacity
    for item in items_sorted:
        weight = item.weight
        if weight <= W:
            # add item to generator
            yield item
            W -= weight
            # if no more items fit in the knapsack
            if W == 0:
                break
        # if heuristic by weight is used, the rest of the items won't fit
        elif heuristic == 2:
            break

def solveInstance(knapsack: Knapsack, index, heuristics):
    '''
    Solve the generated or loaded instance by the specified heuristics.
    '''
    print(f' {index}° instance:\n   {knapsack.total_items} items\n   {knapsack.capacity} of capacity')
    for h in heuristics:
        print('\tSolving instance... ', end='')
        start = time()
        # heuristics take 0 seconds to run:
        items = pickItems(knapsack, h)
        # the measured time is actually just the sum of the values:
        value = sum(i.value for i in items)
        end = time()
        print('done\r', end='')
        print('                                    \r', end='')
        print(f'\tTotal value by heuristic {h}: {value}')
        
        measured_time = end - start
        if measured_time >= 0.1:
            print(f'\t   Measured time: {measured_time:.3g} seconds')
