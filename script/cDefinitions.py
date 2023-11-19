import ctypes



# key = address, value = old_value before overwritting with 0xCC
bpAddrValues = {}




class user_regs_struct(ctypes.Structure): # MUST ALSO USE ctype.byref(), c always expects a pointer
    _fields_ = [
        ("r15", ctypes.c_ulonglong),
        ("r14", ctypes.c_ulonglong),
        ("r13", ctypes.c_ulonglong),
        ("r12", ctypes.c_ulonglong),
        ("rbp", ctypes.c_ulonglong),
        ("rbx", ctypes.c_ulonglong),
        ("r11", ctypes.c_ulonglong),
        ("r10", ctypes.c_ulonglong),
        ("r9", ctypes.c_ulonglong),
        ("r8", ctypes.c_ulonglong),
        ("rax", ctypes.c_ulonglong),
        ("rcx", ctypes.c_ulonglong),
        ("rdx", ctypes.c_ulonglong),
        ("rsi", ctypes.c_ulonglong),
        ("rdi", ctypes.c_ulonglong),
        ("orig_rax", ctypes.c_ulonglong),
        ("rip", ctypes.c_ulonglong),
        ("cs", ctypes.c_ulonglong),
        ("eflags", ctypes.c_ulonglong),
        ("rsp", ctypes.c_ulonglong),
        ("ss", ctypes.c_ulonglong),
        ("fs_base", ctypes.c_ulonglong),
        ("gs_base", ctypes.c_ulonglong),
        ("ds", ctypes.c_ulonglong),
        ("es", ctypes.c_ulonglong),
        ("fs", ctypes.c_ulonglong),
        ("gs", ctypes.c_ulonglong),
    ]

unsigned_char_p = ctypes.POINTER(ctypes.c_ubyte) # MUST ALSO USE ctype.byref(), c always expects a pointer
long_long_unsigned = ctypes.c_ulonglong
pid_t = ctypes.c_int



def setupSharedObjects():
    ptraceLib = ctypes.CDLL("script/codeCoverage/ptraceDebugger.so")
    if ptraceLib is None:
        raise Exception("Failed to load ptrace")
    snapshotLib = ctypes.CDLL("script/snapshot/snapshot.so")
    if snapshotLib is None:
        raise Exception("Failed to load snapshot")


    # snapshot shared object
    snapshotLib.create_snapshot.restype = unsigned_char_p;
    snapshotLib.create_snapshot.argtypes = [pid_t]

    snapshotLib.restore_snapshot.argtypes = [unsigned_char_p, pid_t]
    snapshotLib.restore_snapshot.restype = None

    # PTRACE shared object
    ptraceLib.get_registers.argtypes = [pid_t, user_regs_struct]
    ptraceLib.get_registers.restype = user_regs_struct

    ptraceLib.set_registers.argtypes = [pid_t, user_regs_struct]
    ptraceLib.set_registers.restype = None

    ptraceLib.get_old_value.argtypes = [pid_t, long_long_unsigned]
    ptraceLib.get_old_value.restype = long_long_unsigned

    ptraceLib.set_bp.argtypes = [long_long_unsigned, long_long_unsigned, pid_t]
    ptraceLib.set_bp.restype = None

    ptraceLib.remove_bp.argtypes = [long_long_unsigned, long_long_unsigned, pid_t]
    ptraceLib.remove_bp.restype = None

    ptraceLib.pause_prog.argtypes = [pid_t]
    ptraceLib.pause_prog.restype = None

    ptraceLib.continue_prog.argtypes = [pid_t]
    ptraceLib.continue_prog.restype = None


    return ptraceLib, snapshotLib

