#!/usr/bin/env python3
# Joseph Fabrello
# Main Func sets up environment, process, etc



import re
import multiprocessing
import sys
import signal
from pwn import *
from helpers.utils import *
from mutations import *
prog = None
ValidInputs = None
payload = None
def segfault_handler(signum, frame):
    with open("bad.txt", "w") as fp:
        fp.write(payload)
    
    print(f"Ladies and Gentlemen, We got him.\n Payload that crashed program in bad.txt .")
    exit(1)


def main():
    if len(sys.argv) < 2:
        print("Correct Usage: <executable> <binary> <valid_input>")
        exit(1)


    signal.signal(signal.SIGSEGV, segfault_handler)
    prog = "./" + sys.argv[0]
    
    ValidInputs = [line for line in open(sys.argv[1], "r")]

    ParentProc = runProg()

    gdb.attach(ParentProc)

def forkNattach(ParentProc):
    pass



def runProg(prog=None):
    return process(prog)


if __name__ == "__main__":
    main()

