"""Module for the heuristic technique to solve a Knapsack problem.
"""
from typing import List

from knapsack import Knapsack
from item import Item

def pickItems(knapsack: Knapsack, heuristic = 3):
    '''Use the heuristic specified in the argument to get a solution for the knapsack problem.
    '''
    knapsack.sortItems(heuristic)
    solution = list()
    W = knapsack.capacity
    for item in knapsack.items:
        if item.weight <= W:
            solution.append(item)
            W -= item.weight
            if W == 0:
                break
        elif heuristic == 2:
            break
    return solution

def sumValues(items: List[Item]):
    '''Objective function of the Knapsack problem. Sums the value of each item in the items list.
    '''
    total_value = 0
    for item in items:
        total_value += item.value
    return total_value