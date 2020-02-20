from sys import exit
from os import system

from file_handling import listFiles
from cli import menu
from instance import generateInstances, loadInstances

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

try:
    runCLI()
except Exception:
    exit()
