"""Module for the CLI (command line interface).
"""
from PyInquirer import prompt
from examples import custom_style_1

from validations import isPositiveNumber, isValidPercentage
from knapsack import Knapsack

# last given value
_last_ = 0

def saveLast(string):
    '''Saves the last given value within the prompt.
    '''
    if isPositiveNumber('int', string):
        global _last_
        _last_ = int(string)
        return True
    return 'Please enter a valid positive integer.'

def validateMax(string):
    '''Returns True if the string represents a greater number than LAST, otherwise returns an error string.
    '''
    if isPositiveNumber('int', string):
        integer = int(string)
        global _last_
        if integer > _last_:
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

def runCLI():
    '''Runs the options selector.
    '''
    questions = (
        { # ask to generate or load an instance
            'type': 'list',
            'name': 'menu',
            'message': 'What do you want to do?',
            'choices': (
                {
                    'name': 'Generate a random instance',
                    'value': 1
                },
                {
                    'name': 'Load an instance from a file',
                    'value': 2
                }
            )
        }
    )

    option = prompt(questions, style=custom_style_1)['menu']
    if option == 1:
        # generate
        knapsacks = list()
        i = 1
        while True:
            print('  === {}° instance ==='.format(i))
            questions = createInstanceQuestions()
            answers = prompt(questions, style=custom_style_1)
            knapsacks.append(Knapsack.random(answers['n'], answers['min w'], answers['max w'], answers['min v'], answers['max v'], answers['p']))

            i += 1
    else:
        # TODO: load
        pass
