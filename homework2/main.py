from sys import exit

from cli import runCLI

try:
    runCLI()
except Exception:
    exit()
