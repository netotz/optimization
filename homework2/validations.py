"""Module for validating inputs.
"""

def isValidPercentage(string, minimum, maximum):
    '''If the string argument represents a valid percentage between the minimum and the maximum, returns True.
    '''
    if isPositiveNumber('float', string):
        percentage = float(string)
        if percentage >= minimum and percentage <= maximum:
            return True
    return False


def isPositiveNumber(_type, string):
    '''If the string argument represents a valid positive type number, returns True.
    '''
    try:
        if _type == 'int':
            number = int(string)
        else:
            number = float(string)
        
        if number <= 0:
            return False
    except ValueError:
        return False
    else:
        return True
