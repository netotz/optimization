'''
Module that contains functions to generate or load instances.
'''

from threading import Thread
from queue import Queue

from questionary import prompt, confirm

from cli import createInstanceQuestions, validateChoices
from knapsack import Knapsack
from heuristic import solveInstance

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

    heuristics = validateChoices('heuristic')
    
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
    # if there are more than 1 available files
    if len(files) > 1:
        instances = validateChoices('file', files)
    # if there is only 1 available file
    else:
        instances = files

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

    heuristics = validateChoices('heuristic')

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
