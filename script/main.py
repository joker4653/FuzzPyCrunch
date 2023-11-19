#!/usr/bin/env python3
# Joseph Fabrello
# Main Func sets up environment, process, etc



import re
import multiprocessing
import sys
import signal
import ctypes
import time
import os
from pwn import *
from helpers.utils import *
import cDefinitions


prog = None
ValidInputs = None
payload = None
regsStruct = cDefinitions.user_regs_struct()
snapshotBuffer = cDefinitions.unsigned_char_p
snapshotRegs = None
iterations = 0
startTime = time.perf_counter()
#ptraceLib, snapshotLib = cDefinitions.setupSharedObjects()

def stats(iterationsIn100Thousands,currTimeTaken, codeCoverage, pid):
    print(f"\n\033[96mFuzzCrunch Stats\033[0m -> Target: \033[96m{sys.argv[1]}\033[0m\n")
    print(f"\033[92mIterations: \033[0m{iterationsIn100Thousands}\n")
    print(f"\033[92mCode Coverage: \033[0m{codeCoverage}\n")
    print(f"\033[92mTime: \033[0m{currTimeTaken}s\n")


def segfaultHandler(payload):
    with open("bad.txt", "w") as fp:
        fp.write(payload)
    
    print(f"Nice One bro its a Seg Fault, take my word im a good programmer.\nPayload that crashed program in bad.txt")
    exit(1)


def fuzzBro(ValidInputs):
    mut = factory(checkfileFormat(ValidInputs),ValidInputs)
    with process(prog) as p:
        p.recvline(timeout=0.0000001)
        pwntoolsPid = pidof(p)[0]
        # pause prog to read memory
        
        #ptraceLib.pause_prog(pwntoolsPid)
        #snapshot memory
        #snapshotBuffer = snapshotLib.create_snapshot(pwntoolsPid)
        
        #snapshotRegs = ptraceLib.get_registers(pwntoolsPid, ctypes.byref(regsStruct))

        #ptraceLib.continue_prog(pwntoolsPid)

        p.sendline("".encode())
        p.proc.stdin.close()
        if p.poll(True) == -11:
                segfaultHandler(payload)
        p.close()
    #print("at setting snapshot")
    #snapshotLib.restore_snapshot(snapshotBuffer, pwntoolsPid)
    #print("past setting snapshot")
    #ptraceLib.set_registers(pwntoolsPid, ctypes.byref(snapshotRegs))
    iterations = 0
    while True:   
        with process(prog) as p:
            
            os.system("clear")

            stats(iterations,time.perf_counter() - startTime, "N/A", None)
            p.recvline(timeout=0.0000001)

            payload = randMutations(ValidInputs, random.randint(1,3), mut)

            if isinstance(payload, str):
                payload.rstrip("\n")
                p.sendline(str(payload).encode())
            else:
                p.sendline(payload)
            p.proc.stdin.close()

            if p.poll(True) == -11:
                segfaultHandler(payload)
                p.close()


        iterations = iterations + 1
        #snapshotLib.restore_snapshot(snapshotBuffer, pwntoolsPid)
        #ptraceLib.set_registers(pwntoolsPid, ctypes.byref(snapshotRegs))



def main():
    if len(sys.argv) < 2:
        print("Correct Usage: ./fuzzer <binary> <valid_input>")
        exit(1)

    print("\nInfiltrating...\n\n")


    context.timeout = 60
    context.log_level = "warning"
    context.binary = sys.argv[1]

    try:
        with open(sys.argv[2], "r") as fp:
            ValidInputs = fp.read()
    except:
        with open(sys.argv[2], "rb") as fp:
            ValidInputs = fp.read()
            

    
    fuzzBro(ValidInputs)


def forkNAttach(proc):
    pass


if __name__ == "__main__":
    main()

