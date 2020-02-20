"""
Module for the CLI (command line interface).
"""

from typing import List
from sys import maxsize

# from PyInquirer import prompt
# symbols used by PyInquirer aren't showing in CMD
from questionary import select, checkbox, Choice

from validation import isPositiveNumber, isValidPercentage, delimitItems, messages

#! global variables
# last given value in inputs
__last = 0

def saveLast(string):
    '''
    Saves the last given value within the prompt.
    '''
    if isPositiveNumber(int, string):
        global __last
        __last = int(string)
        if __last > maxsize - 1:
            return messages['lower'].format(maxsize - 1)
        return True
    return messages['valid']

def validateMax(string):
    '''
    Returns True if the string represents a greater number than LAST, otherwise returns an error string.
    '''
    if isPositiveNumber(int, string):
        integer = int(string)
        if integer > maxsize:
            return messages['lower'].format(maxsize)
        elif integer > __last:
            return True
        else:
            return messages['greater']
    return messages['valid']

def createInputQuestion(name, message, function = saveLast, cast = int):
    '''
    Returns a dictionary of type input.
    '''
    return {
        'type': 'input',
        'name': name,
        'qmark': '>',
        'message':  message,
        'validate': function,
        'filter': lambda n: cast(n)
    }

def createInstanceQuestions():
    '''
    Returns a tuple with questions asking for data to generate an instance.
    '''
    return (
        createInputQuestion('n', 'How many items?', delimitItems),
        createInputQuestion('p', 'What percentage of the items can fit in the knapsack?', isValidPercentage, float),
        createInputQuestion('min v', 'How low can the value of an item be?'),
        createInputQuestion('max v', 'And how high?', validateMax),
        createInputQuestion('min w', 'How low can the weight of an item be?'),
        createInputQuestion('max w', 'And how high?', validateMax)
    )

def menu(files = []):
    '''
    Ask to select an option of the menu and returns it.
    '''
    # list of option to display
    options = [Choice('Generate random instances', 1)]
    # if there is at least one available file to load
    if files:
        # add option to load
        options.append(Choice('Load instances from files', 2))
    # add option to exit
    options.append(Choice('Exit', 0))

    return select(
        'What do you want to do?',
        options,
        qmark='~'
    ).ask()

def filesCheckbox(files):
    '''
    Returns a checkbox of the available files.
    '''
    files_listed = [Choice(name) for name in files]
    return checkbox(
        'Which instances do you want to load?',
        files_listed,
        qmark='~'
    )

def heuristicsCheckbox():
    '''
    Returns a checkbox to select a heuristic.
    '''
    return checkbox(
        'Which heuristic techniques do you want to use?',
        [
            Choice('Pick the most valuable items', 1),
            Choice('Pick the lightest items', 2),
            Choice('Pick the items with the highest value-weight ratio', 3)
        ],
        qmark='~'
    )

def validateChoices(name, files = [])  -> List[str]:
    '''
    Enters a loop until at least one element of the checkbox is chosen.

    Returns a list of the chosen elements.
    '''
    if name == 'file':
        local_checkbox = filesCheckbox(files)
    elif name == 'heuristic':
        local_checkbox = heuristicsCheckbox()

    while True:
        print()
        choices = local_checkbox.ask()
        if len(choices) > 0:
            return choices
        else:
            print('Please select at least one %s.' % name)
