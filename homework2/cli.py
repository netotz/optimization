"""
Module for the CLI (command line interface).
"""

from typing import List
from os import system
from sys import maxsize
from threading import Thread
from queue import Queue

# from PyInquirer import prompt
# symbols used by PyInquirer aren't showing in CMD
from questionary import prompt, confirm, select, checkbox, Choice

from validations import isPositiveNumber, isValidPercentage, messages
from knapsack import Knapsack
from file_handling import listFiles
from heuristic import pickItems, sumValues

#! global variables
# last given value in inputs
__last = 0
# list of threads for writing to files
__writing = [Thread()]

def delimitItems(string):
    '''
    Set a maximum value for the input of number of items.
    '''
    if isPositiveNumber(int, string):
        integer = int(string)
        if integer > 5000000:
            return messages['lower'].format(5000000)
        return True
    return messages['valid']

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

def generateInstances() -> List[Knapsack]:
    '''
    Generate instances from prompt.
    '''
    knapsacks = list()
    index = 1
    another = True
    while another:
        print('\n  === {}° instance ==='.format(index))
        answers = prompt(createInstanceQuestions())
        print('  Generating instance... ', end='')
        knapsacks.append(Knapsack.random(answers['n'], answers['min w'], answers['max w'], answers['min v'], answers['max v'], answers['p']))
        print('done')

        # new thread to write last instance and start it
        name = 'w' + str(index)
        write = Thread(target=knapsacks[-1].toFile, name=name, daemon=True)
        write.start()
        global __writing
        # if last thread in list is still running
        if __writing[-1].is_alive():
            # append new thread to list
            __writing.append(write)
        # if last thread in list is finished
        else:
            # use new thread to overwrite last in list
            __writing[-1] = write

        another = confirm('Do you want to add another instance?').ask()
        index += 1
    return knapsacks

def menu():
    '''
    Ask to select an option of the menu.
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
            Choice('Pick the items with the highest value-weight ratio', 3, checked=True)
        ],
        qmark='~'
    )

def validateChoices(checkbox, name)  -> List[str]:
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

def solveInstance(knapsack: Knapsack, index, heuristics):
    '''
    Solve the generated or loaded instance by the specified heuristics.
    '''
    print(' {}° instance:\n   {} items\n   {} of capacity'.format(index, knapsack.total_items, knapsack.capacity))
    for h in heuristics:
        items = pickItems(knapsack, h)
        value = sumValues(items)
        print('\tTotal value by heuristic {}: {}\n\tPercentage of items picked: {:.2f}%'.format(h, value, (len(items) / knapsack.total_items) * 100))
        print()

def runCLI():
    '''
    Runs the options selector.
    '''
    print()

    option = menu()
    # generate
    if option == 1:
        knapsacks = generateInstances()
        heuristics = validateChoices(heuristicsCheckbox(), 'heuristic')
        for i, k in enumerate(knapsacks):
            solveInstance(k, i + 1, heuristics)
        # loop over threads list
        for write in __writing:
            # if a thread is still running
            if write.is_alive():
                index = write.name[-1]
                print('  Saving {}° instance to file... '.format(index), end='')
                # wait until the thread finishes
                write.join()
                print('done')
        print('  All instances have been saved to files.')
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
            # list for file names
            instances = validateChoices(filesCheckbox(files), 'file')

            # queue for threads
            queue = Queue(len(instances))
            # list of threads for reading files
            reading = list()
            for index, file_name in enumerate(instances):
                name = 'r' + str(index + 1)
                read = Thread(target=lambda q, arg: q.put(Knapsack.fromFile(arg)), args=(queue, file_name), name=name, daemon=True)
                read.start()
                reading.append(read)
    
            heuristics = validateChoices(heuristicsCheckbox(), 'heuristic')

            size = len(instances)
            index = 1
            load_str = '  Loading instance...'
            while size:
                for i, read in enumerate(reading):
                    if read.is_alive():
                        print('{}\r'.format(load_str), end='')
                        continue
                    else:
                        del reading[i]

                    knapsack = queue.get()
                    if knapsack is not None:
                        print('{}\r'.format(' ' * len(load_str)), end='')
                        solveInstance(knapsack, index, heuristics)
                    size -= 1
                    index += 1
                    if size <= 0:
                        break
