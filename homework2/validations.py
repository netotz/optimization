"""Module for validating inputs.
"""

def isPositiveInteger(string):
    '''If the string argument represents a valid positive integer, returns True.
    '''
    try:
        integer = int(string)
        if integer <= 0:
            return False
    except ValueError:
        return False
    else:
        return True