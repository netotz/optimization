"""Module for validating inputs.
"""

def isNonNegativeInteger(string):
    '''If the string argument represents a valid non-negative integer (> 0), returns True.
    '''
    try:
        integer = int(string)
        if integer <= 0:
            return False
    except ValueError:
        return False
    else:
        return True
