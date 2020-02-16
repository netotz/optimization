"""
Module for validating inputs.
"""

# messages to show when input is incorrect
messages = {
    'valid': 'Please enter a valid positive integer.',
    'greater': 'Please enter a number greater than the lower limit.',
    'lower': 'Please enter a number lower than {}.',
    'percentage': 'Please enter a percentage between {} and {}.'
}

def isPositiveNumber(cast, string):
    '''
    If the string argument represents a valid positive cast (int or float) number, returns True.
    '''
    try:
        if cast(string) <= 0:
            return False
    except ValueError:
        return False
    else:
        return True

def isValidPercentage(string, minimum = 1, maximum = 75):
    '''
    If the string argument represents a valid percentage between the minimum and the maximum, returns True.
    '''
    if isPositiveNumber(float, string):
        percentage = float(string)
        if percentage >= minimum and percentage <= maximum:
            return True
    return messages['percentage'].format(minimum, maximum)
