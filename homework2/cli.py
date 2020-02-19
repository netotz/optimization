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

from validation import isPositiveNumber, isValidPercentage, messages
from knapsack import Knapsack
from file_handling import listFiles
from heuristic import solveInstance

#! global variables
# last given value in inputs
__last = 0

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

def validateChoices(checkbox, name)  -> List[str]:
    '''
    Enters a loop until at least one element of the checkbox is chosen.

    Returns a list of the chosen elements.
    '''
    while True:
        print()
        choices = checkbox.ask()
        if len(choices) > 0:
            return choices
        else:
            print('Please select at least one %s.' % name)

def generateInstances():
    '''
    Generate instances from prompt.
    '''
    knapsacks = list()
    # list of threads for writing to files
    writing = list()

    index = 1
    another = True
    while another:
        print('\n  === {}° instance ==='.format(index))
        answers = prompt(createInstanceQuestions())

        k = Knapsack.random(answers['n'], answers['min w'], answers['max w'], answers['min v'], answers['max v'], answers['p'])
        knapsacks.append(k)

        # new thread's name
        name = 'w%d' % index
        # new thread to write last instance and start it
        write = Thread(target=knapsacks[-1].toFile, name=name)
        write.start()
        writing.append(write)
        
        another = confirm('Do you want to add another instance?').ask()
        index += 1

    heuristics = validateChoices(heuristicsCheckbox(), 'heuristic')
    
    save_str = '  Saving instances to files...'
    size = len(writing)
    while size:
        # loop over threads list
        for write, k in zip(writing, knapsacks):
            index = int(write.name[-1])
            # if a thread is still running
            if write.is_alive():
                print('%s\r' % save_str , end='')
                continue
            else:
                # wait until the thread finishes
                write.join()
                print('%s\r' % (' ' * len(save_str)), end='')
                solveInstance(k, index, heuristics)
                size -= 1
    print('\n All instances have been saved to files.')

def loadInstances(files):
    '''
    Load instances from files.
    '''
    # list for file names
    instances = validateChoices(filesCheckbox(files), 'file')

    # queue for threads
    thread_queue = Queue(len(instances))
    # list of threads for reading files
    reading = list()
    for index, file_name in enumerate(instances):
        name = 'r%d' % index
        # new thread to read a file
        read = Thread(target=lambda q, arg: q.put(Knapsack.fromFile(arg)), args=(thread_queue, file_name), name=name, daemon=True)
        # start new thread and add it to list
        read.start()
        reading.append(read)

    heuristics = validateChoices(heuristicsCheckbox(), 'heuristic')

    # number of instances to solve
    size = len(instances)
    index = 1
    load_str = '  Loading instance...'
    # while there exist unsolved instances
    while size:
        # loop over list of threads
        for read in reading:
            # if thread is still running
            if read.is_alive():
                print('%s\r' % load_str, end='')
                # check next thread
                continue
            read.join()
            # get Knapsack object
            knapsack = thread_queue.get()
            if knapsack is not None:
                print('%s\r' % (' ' * len(load_str)), end='')
                solveInstance(knapsack, index, heuristics)
            size -= 1
            index += 1
            # if all instances have been solved
            if size <= 0:
                # break for
                break

def runCLI():
    '''
    Runs the options selector.
    '''
    print()

    # list of files that contains instances, if any
    files = listFiles()

    option = menu(files)
    # generate
    if option == 1:
        generateInstances()
    # load if available
    elif option == 2:
        loadInstances(files)
    # exit
    elif option == 0:
        return

    print()
    system('pause')
    system('cls')
    return runCLI()
