
from unittest.mock import patch
import runpy, sys


def run_with_args():
    print('Choose configuration:')
    print('1. Default (full featured simulation)')
    print('2. MultiClamp 700B')
    print('3. Minimal simulation')
    print('4. Exit')
    inp = input('Select option: ')
    if inp == '1':
        testargs = ["acq4", "-c", "./config/example/default.cfg"]
    elif inp == '2':
        testargs = ["acq4", "-c", "./config/JhouLabConfigs/700B.cfg"]
    elif inp == '3':
        testargs = ["acq4", "-c", "./config/JhouLabConfigs/simulated, minimal.cfg"]
    elif inp == '4':
        return
    else:
        print('Invalid option')
        return
    with patch.object(sys, 'argv', testargs):
        runpy.run_module("acq4", run_name="__main__")


USE_CUSTOM_ARGS = True

if __name__ == "__main__":
    if USE_CUSTOM_ARGS:
        run_with_args()
    else:
        from acq4.__main__ import *

