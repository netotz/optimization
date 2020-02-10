"""Module for the CLI (command line interface).
"""
from typing import List
from os import system

from PyInquirer import prompt
import examples as styles

from validations import isPositiveNumber, isValidPercentage
from knapsack import Knapsack
from file_handling import listFiles
from heuristic import pickItems, sumValues

# last given value
# ! global variable
__last__ = 0

def saveLast(string):
    '''Saves the last given value within the prompt.
    '''
    if isPositiveNumber('int', string):
        global __last__
        __last__ = int(string)
        return True
    return 'Please enter a valid positive integer.'

def validateMax(string):
    '''Returns True if the string represents a greater number than LAST, otherwise returns an error string.
    '''
    if isPositiveNumber('int', string):
        integer = int(string)
        global __last__
        if integer > __last__:
            return True
        else:
            return 'Please enter a number greater than the lower limit.'
    return 'Please enter a valid positive integer.'

def createInputQuestion(name, message, function = saveLast, cast = int):
    '''Returns a dictionary of type input.
    '''
    return {
        'type': 'input',
        'name': name,
        'message':  message,
        'validate': function,
        'filter': lambda n: cast(n)
    }

def createInstanceQuestions():
    '''Returns a tuple with questions asking for data to generate an instance.
    '''
    return (
        createInputQuestion('n', 'How many items?'),
        createInputQuestion('p', 'What percentage of the items can fit in the knapsack?', isValidPercentage, float),
        createInputQuestion('min v', 'How low can the value of an item be?'),
        createInputQuestion('max v', 'And how high?', validateMax),
        createInputQuestion('min w', 'How low can the weight of an item be?'),
        createInputQuestion('max w', 'And how high?', validateMax)
    )

def askAnotherInstance():
    '''Asks to prompt for another instance.
    '''
    return (
        {
            'type': 'confirm',
            'name': 'another',
            'message': 'Do you want to add another instance?'
        }
    )

def generateInstances() -> List[Knapsack]:
    '''Generate instances from prompt.
    '''
    knapsacks = list()
    i = 1
    while True:
        print('\n  === {}° instance ==='.format(i))
        answers = prompt(createInstanceQuestions(), style=styles.custom_style_1)
        print('  Generating instance... ', end='')
        knapsacks.append(Knapsack.random(answers['n'], answers['min w'], answers['max w'], answers['min v'], answers['max v'], answers['p']))
        print('done')
        answers = prompt(askAnotherInstance(), style=styles.custom_style_2)
        if not answers['another']:
            break
        i += 1
    return knapsacks

def createMenu():
    '''Create the main menu option.
    '''
    return (
        { # ask to generate or load an instance
            'type': 'list',
            'name': 'menu',
            'message': 'What do you want to do?',
            'choices': (
                {
                    'name': 'Generate random instances',
                    'value': 1
                },
                {
                    'name': 'Load instances from files',
                    'value': 2
                }
            )
        }
    )

def askForExit():
    return (
        {
            'type': 'confirm',
            'name': 'exit',
            'message': 'Do you want to exit?'
        }
    )

def createFilesCheckbox(files):
    '''Returns a checkbox of the available files.
    '''
    files_listed = [{'name': name} for name in files]
    return (
            {
                'type': 'checkbox',
                'qmark': '*',
                'name': 'files',
                'message': 'The first number is the total items and the second is the capacity.\nWhich instances do you want to load?',
                'choices': files_listed,
                'validate': lambda answer: 'Please select at least one file.' if len(answer) == 0 else True
        }
    )

def createHeuristicsCheckbox():
    '''Returns a checkbox to select a heuristic.
    '''
    return (
        {
            'type': 'checkbox',
            'qmark': '*',
            'name': 'heuristics',
            'message': 'Which heuristic techniques do you want to use?',
            'choices': (
                {
                    'name': 'Pick the most valuable items',
                    'value': 1
                },
                {
                    'name': 'Pick the lightest items',
                    'value': 2
                },
                {
                    'name': 'Pick the items with the highest value-weight ratio',
                    'checked': True,
                    'value': 3
                }
            ),
            'validate': lambda answer: 'Please select at least one heuristic.' if len(answer) == 0 else True
        }
    )

def solveInstances(knapsacks: List[Knapsack]):
    '''Solve the generated or loaded instances by the specified heuristics.
    '''
    heuristics = prompt(createHeuristicsCheckbox())['heuristics']
    for i, k in enumerate(knapsacks):
        print('\n{}° instance:\n   {} items\n   {} of capacity'.format(i + 1, k.total_items, k.capacity))
        for h in heuristics:
            items = pickItems(k, h)
            value = sumValues(items)
            print('\tTotal value by heuristic {}: {}\n\tPercentage of items picked: {}%'.format(h, value, (len(items) / k.total_items) * 100))
            print()

def runCLI():
    '''Runs the options selector.
    '''
    knapsacks = None
    option = prompt(createMenu(), style=styles.custom_style_3)['menu']
    if option == 1:
        # generate
        knapsacks = generateInstances()
        print('\n  Saving instances to files... ', end='')
        for k in knapsacks:
            k.toFile()
        print('done')
    else:
        # load
        files = listFiles()
        if not files:
            print("\nThere isn't any available file to load.")
            if prompt(askForExit(), style=styles.custom_style_2)['exit']:
                return
            else:
                system('cls')
                return runCLI()
        else:
            # there are available files
            instances = prompt(createFilesCheckbox(files))['files']
            print('  Loading instances... ', end='')
            knapsacks = [Knapsack.fromFile(name) for name in instances]
            print('done')
    
    if knapsacks is None:
        return
    system('cls')
    solveInstances(knapsacks)
