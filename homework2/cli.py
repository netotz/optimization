"""
Module for the CLI (command line interface).
"""

from typing import List
from os import system
from threading import Thread

# from PyInquirer import prompt
# symbols used by PyInquirer aren't showing in CMD
from questionary import prompt, confirm, select, checkbox, Choice

from validations import isPositiveNumber, isValidPercentage
from knapsack import Knapsack
from file_handling import listFiles
from heuristic import pickItems, sumValues

#! global variables
# last given value in inputs
__last = 0
# thread used for writing to files
__writing = None

def saveLast(string):
    '''Saves the last given value within the prompt.
    '''
    if isPositiveNumber(int, string):
        global __last
        __last = int(string)
        return True
    return 'Please enter a valid positive integer.'

def validateMax(string):
    '''Returns True if the string represents a greater number than LAST, otherwise returns an error string.
    '''
    if isPositiveNumber(int, string):
        integer = int(string)
        if integer > __last:
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

def generateInstances() -> List[Knapsack]:
    '''Generate instances from prompt.
    '''
    knapsacks = list()
    i = 1
    another = True
    while another:
        print('\n  === {}° instance ==='.format(i))
        answers = prompt(createInstanceQuestions())
        print('  Generating instance... ', end='')
        knapsacks.append(Knapsack.random(answers['n'], answers['min w'], answers['max w'], answers['min v'], answers['max v'], answers['p']))
        print('done')

        global __writing
        if __writing is not None:
            __writing.join()
        __writing = Thread(target = knapsacks[-1].toFile)
        __writing.start()

        another = confirm('Do you want to add another instance?').ask()
        i += 1
    return knapsacks

def menu():
    '''Ask to select an option of the menu.
    '''
    return select(
        'What do you want to do?',
        [
            Choice('Generate random instances', 1),
            Choice('Load instances from files', 2)
        ],
        qmark='~'
    ).ask()

def filesCheckbox(files):
    '''Returns a checkbox of the available files.
    '''
    files_listed = [Choice(name) for name in files]
    return checkbox(
        'Which instances do you want to load?',
        files_listed,
        qmark='~'
    )

def heuristicsCheckbox():
    '''Returns a checkbox to select a heuristic.
    '''
    return checkbox(
        'Which heuristic techniques do you want to use?',
        [
            Choice('Pick the most valuable items', 1),
            Choice('Pick the lightest items', 2),
            Choice('Pick the items with the highest value-weight ratio', 3, checked=True)
        ],
        qmark='~'
    )

def validateChoices(checkbox, name):
    '''
    Enters a loop until at least one element of the checkbox is chosen.

    Returns a list of the elements chosen.
    '''
    while True:
        print()
        choices = checkbox.ask()
        if len(choices) > 0:
            return choices
        else:
            print('Please select at least one {}.'.format(name))

def solveInstances(knapsacks: List[Knapsack]):
    '''Solve the generated or loaded instances by the specified heuristics.
    '''
    heuristics = validateChoices(heuristicsCheckbox(), 'heuristic')
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
    option = menu()
    # generate
    if option == 1:
        knapsacks = generateInstances()
    # load
    else:
        files = listFiles()
        if not files:
            print("\nThere isn't any available file to load.")
            if confirm('Do you want to exit?').ask():
                return
            else:
                return runCLI()
        # there are available files
        else:
            instances = validateChoices(filesCheckbox(files), 'file')

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

    if __writing is not None and __writing.is_alive():
        print('  Saving last instance to file... ', end='')
        __writing.join()
        print('done')
