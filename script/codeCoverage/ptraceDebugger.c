#include <sys/types.h>
#include <unistd.h>
#include <sys/ptrace.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/user.h>
#include <sys/wait.h>

// Naive Debugger implemented through manipulation of ptrace
// uses ptrace to insert breakpoints at instructions as code coverage


// get registers of a pid. For use when setting breakpoints
struct user_regs_struct get_registers(pid_t pwntools_process_pid, struct user_regs_struct regs) {
    errno = 0;
    int err = ptrace(PT_GETREGS, pwntools_process_pid, 0,&regs);

    if (err == -1) {fprintf(stderr, "Error getting registers <ptrace>"); exit(errno);}

    return regs;
}

// set registers of a pid. For use when setting breakpoints
void set_registers(pid_t pwntools_process_pid, struct user_regs_struct regs) {
    errno = 0;
    int err = ptrace(PT_SETREGS, pwntools_process_pid, 0, &regs);

    if (err == -1) {fprintf(stderr, "Error setting registers <ptrace>"); exit(errno);}
}

// long long data type irrelevant on 32 bit systems.
// provide process id and the address of the value to retrieve
long long unsigned get_old_value(pid_t pwntools_process_pid, long long unsigned addr) {
    errno = 0;
    long long unsigned val = ptrace(PTRACE_PEEKTEXT, pwntools_process_pid, (void*)addr, 0);

    if (val == -1 && errno != 0) {fprintf(stderr, "Error getting old value <ptrace>"); exit(errno);}

    return val;
}

void set_bp(long long unsigned bp_addr, long long unsigned literal_val, pid_t pwntools_process_pid) {
    errno = 0;

    // & with 00s to overwrite last byte then or to bring the sig trap bytes into the address.
    long long unsigned bp = ((literal_val & 0xFFFFFFFFFFFFFF00) | 0xCC);

    int err = ptrace(PTRACE_POKETEXT, pwntools_process_pid, (void*)bp_addr, (void*)bp);

    if (err == -1 && errno != 0) {fprintf(stderr, "error setting a breakpoint <ptrace>"); exit(errno);}

}

void remove_bp(long long unsigned bp_addr, long long unsigned literal_val, pid_t pwntools_process_pid) {
    errno = 0;

    // we can just put the value back in like nothing happened
    int err = ptrace(PTRACE_POKETEXT, pwntools_process_pid, (void*)bp_addr, (void*)literal_val);

    if (err == -1 && errno != 0) {fprintf(stderr, "error removing a bp <ptrace>"); exit(errno);}


}


void pause_prog(pid_t pwntools_process_pid) {
    errno = 0;
    int status;

    // pause prog for looking at memory
    int err = ptrace(PTRACE_ATTACH, pwntools_process_pid, NULL, NULL);
    if (err == -1 && errno != 0 ) {fprintf(stderr, "error attaching to prog <ptrace>"); exit(errno);}

    waitpid(pwntools_process_pid, &status, 0);
}


void continue_prog(pid_t prwntools_process_pid) {
    errno = 0;

    int err = ptrace(PTRACE_CONT, prwntools_process_pid, 0,0);
    if (err == -1 && errno != 0) {fprintf(stderr, "error continuing prog <ptrace>"); exit(errno);}
}