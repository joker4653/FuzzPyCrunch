#!/usr/bin/env python3
# Joseph Fabrello
# Main Func sets up environment, process, etc



import re
import multiprocessing
import sys
import signal
import os
from pwn import *
from helpers.utils import *


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
        print("Correct Usage: ./fuzzer <binary> <valid_input>")
        exit(1)

    print("\nInfiltrating...\n\n")


    context.terminal = ['gnome-terminal', '-x']
    context.timeout = 60
    context.log_level = "warning"

    prog = sys.argv[1]

    with open(sys.argv[2], "r") as fp:
        ValidInputs = fp.read()

    print(ValidInputs)
    mut = factory(checkfileFormat(ValidInputs),ValidInputs)
    p = process(prog)
    p.recvline(timeout=0.0000001)
    p.sendline("".encode())
    p.proc.stdin.close()
    if p.poll(True) == -11:
            segfault_handler(payload)
            p.close()

    while True:
        p = process(prog)
    
        p.recvline(timeout=0.0000001)

        payload = randMutations(ValidInputs, random.randint(1,3), mut).rstrip("\n")
        print(payload)
        
        p.sendline(str(payload).encode())
        p.proc.stdin.close()

        if p.poll(True) == -11:
            segfault_handler(payload)
            p.close()




def forkNAttach(proc):
    pass


if __name__ == "__main__":
    main()

