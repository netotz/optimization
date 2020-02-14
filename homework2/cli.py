"""Module for the CLI (command line interface).
"""
from typing import List
from os import system

# ! symbols used by PyInquirer don't show in CMD
# from PyInquirer import prompt
from questionary import prompt
# import examples as styles

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
        'qmark': '>',
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
        answers = prompt(createInstanceQuestions())
        print('  Generating instance... ', end='')
        knapsacks.append(Knapsack.random(answers['n'], answers['min w'], answers['max w'], answers['min v'], answers['max v'], answers['p']))
        print('done')
        answers = prompt(askAnotherInstance())
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
            'qmark': '~',
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
                'qmark': '~',
                'name': 'files',
                'message': 'Which instances do you want to load?',
                'choices': files_listed
        }
    )

def createHeuristicsCheckbox():
    '''Returns a checkbox to select a heuristic.
    '''
    return (
        {
            'type': 'checkbox',
            'qmark': '~',
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
            )
        }
    )

def validateCheckbox(checkbox, name):
    '''
    Enters a loop until at least one element of the checkbox is chosen.

    Returns a list of the elements chosen.
    '''
    while True:
        print()
        answers = prompt(checkbox)[name]
        if len(answers) > 0:
            return answers
        else:
            print('Please select at least one {}.'.format(name[:-1]))

def solveInstances(knapsacks: List[Knapsack]):
    '''Solve the generated or loaded instances by the specified heuristics.
    '''
    heuristics = validateCheckbox(createHeuristicsCheckbox(), 'heuristics')
    for i, k in enumerate(knapsacks):
        print('\n{}° instance:\n   {} items\n   {} of capacity'.format(i + 1, k.total_items, k.capacity))
        for h in heuristics:
            items = pickItems(k, h)
            value = sumValues(items)
            print('\tTotal value by heuristic {}: {}\n\tPercentage of items picked: {:.2f}%'.format(h, value, (len(items) / k.total_items) * 100))
            print()

def runCLI():
    '''Runs the options selector.
    '''
    print()

    knapsacks = list()
    option = prompt(createMenu())['menu']
    # generate
    if option == 1:
        knapsacks = generateInstances()
        
        # formatting strings to print
        instances_str = 'instance'
        files_str = 'file'
        if len(knapsacks) > 1:
            instances_str += 's'
            files_str += 's'
        print('  Saving {} to {}...'.format(instances_str, files_str))
        for k in knapsacks:
            k.toFile()
        print('  ...done')
    # load
    else:
        files = listFiles()
        if not files:
            print("\nThere isn't any available file to load.")
            if prompt(askForExit())['exit']:
                return
            else:
                return runCLI()
        # there are available files
        else:
            instances = validateCheckbox(createFilesCheckbox(files), 'files')

            # formatting strings to print
            instances_str = 'instance'
            if len(instances) > 1:
                instances_str += 's'
            print('  Loading {}...'.format(instances_str))

            knapsacks = list()
            for name in instances:
                k = Knapsack.fromFile(name)
                if k is not None:
                    knapsacks.append(k)
            
            # check if knapsacks' list is empty
            if not knapsacks:
                print('  ...failed :(')
                return runCLI()
            else:
                print('  ...done')
    solveInstances(knapsacks)
