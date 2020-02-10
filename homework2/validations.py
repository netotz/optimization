"""Module for validating inputs.
"""

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
