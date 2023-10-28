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



def segfault_handler(payload):
    with open("bad.txt", "w") as fp:
        fp.write(payload)
    
    print(f"Ladies and Gentlemen, We got him.\nPayload that crashed program in bad.txt")
    exit(1)


def main():
    if len(sys.argv) < 2:
        print("Correct Usage: <executable> <binary> <valid_input>")
        exit(1)

    print("\nInfiltrating...\n\n")


    context.terminal = ['gnome-terminal', '-x']
    context.timeout = 60
    context.log_level = "warning"

    prog = './' + sys.argv[1]

    with open(sys.argv[2], "r") as fp:
        ValidInputs = fp.read()


    mut = factory(checkfileFormat(ValidInputs),ValidInputs)



    while True:
        p = process(prog)

        payload = mut.chooseMutation(ValidInputs)
    
        p.recvline(timeout=0.0000001)

        p.sendline(payload.encode())

        p.proc.stdin.close()

        if p.poll(True) == -11:
            segfault_handler(payload)

        p.close()
        
    
    #gdbInstance = gdb.attach(ParentProc, """checkpoint
    #                                        continue""")


    
def forkNattach(ParentProc):
    pass




if __name__ == "__main__":
    main()

