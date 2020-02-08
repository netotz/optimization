"""Module for the heuristic technique to solve a Knapsack problem.
"""
from knapsack import Knapsack

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
