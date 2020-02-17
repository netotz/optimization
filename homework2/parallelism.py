'''
Module to handle parallelism functions.
'''

from threading import Thread
from queue import Queue as ThreadQueue
from multiprocessing import Process, Queue as ProcQueue

