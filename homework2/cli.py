"""Module for the CLI (command line interface).
"""
from PyInquirer import prompt
from examples import custom_style_1

from validations import isPositiveInteger

def inputDict(name, message):
    '''Returns a dictionary of type input.
    '''
    return {
        'type': 'input',
        'name': name,
        'message':  message,
        'validate': lambda n: True if isPositiveInteger(n) else 'Please enter a valid positive integer.',
        'filter': lambda n: int(n)
    }

def askForInstance():
    '''Prompt for data to generate an instance.
    '''
    return ((
        inputDict('n', 'How many items?'),
        inputDict('p', 'What percentage of the items can fit in the knapsack?'),
        inputDict('min v', 'How low can the value of an item be?'),
        inputDict('max v', 'And how high?'),
        inputDict('min w', 'How low can the weight of an item be?'),
        inputDict('max w', 'And how high?')
    ))

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
        questions = (
            {
                'type': 'input',
                'name': 'instances',
                'message': 'How many instances?',
                'validate': lambda n: True if isPositiveInteger(n) else 'Please enter a valid positive integer.',
                'filter': lambda n: int(n)
            }
        )
        instances = prompt(questions, style=custom_style_1)['instances']
        for i in range(instances):
            print('=== {}° instance ==='.format(i + 1))
            questions = askForInstance()
            answers = prompt(questions, style=custom_style_1)
            
    else:
        # TODO: load
        pass

runCLI()