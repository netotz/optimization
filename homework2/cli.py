"""Module for the CLI (command line interface).
"""
from PyInquirer import prompt
from examples import custom_style_1

def runCLI():
    '''Runs the options selector.
    '''
    answers = dict()
    which_menu = (
        { # ask to generate or load an instance
            'type': 'list',
            'name': 'option',
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

    menu = prompt(which_menu, style=custom_style_1)
    if menu == 1:
        # TODO: generate
    else:
        # TODO: load
