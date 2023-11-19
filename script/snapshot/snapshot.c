#define _GNU_SOURCE
#include <sys/types.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/uio.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>
#include <math.h>
#include <stdint.h>

#define MAX_ARRAY_SIZE 4096
int num_region;
intptr_t maps_offsets[MAX_ARRAY_SIZE]; // increments in index 2s see implementation later
intptr_t buf_offsets[MAX_ARRAY_SIZE];
int rdwr_offsets[MAX_ARRAY_SIZE]; // increments in index 2s see implementation later

// responsible for creating a snapshot
// finds memory regions related to binary and copies them to malloc'd memory
unsigned char* create_snapshot(pid_t pwntools_process_pid) {
    //printf("creaint snapshot");
    errno = 0;
    int counter = 1;



    // malloc giga memory to store snapshot of memory
    unsigned char* snapshot_buffer = (unsigned char*)malloc(0x2C000);


    // get memory map of the process
    char proc_map[0x50] = {};

    //popen cant use format string so workaround:
    sprintf(proc_map, "cat /proc/%d/maps | grep rw | awk '{split($1,a,\"-\"); print a[1]; print a[2]}'", pwntools_process_pid);

    FILE *addr_fp = popen(proc_map, "r");
    
    if (addr_fp == NULL) {fprintf(stderr, "open map"); exit(errno);}
    
    char *end;
    char line[0x50] = {};
    while (fgets(line, sizeof(line), addr_fp)) {
        // grab map addrs for rw that could change on every fuzz iteration
        if (counter % 2 == 0) {
            maps_offsets[counter] = strtol(line, &end, 16);
        } else {
            rdwr_offsets[counter - 1] = maps_offsets[counter - 1] - strtol(line, &end, 16);
        }
        counter++;
    }

    // should be an even number
    num_region = counter / 2;
    fclose(addr_fp);



    counter = 1;
    // assign regions for malloc'd memory
    intptr_t offset = 0xFFF;
    for (int i = 1; i <= counter; i += 2) {
        buf_offsets[i] = (intptr_t)snapshot_buffer + (offset * i);
    }



    // now grab memory regions /proc/mem
    // BINARY MUST BE PAUSED BEFORE READING MEMORY
    char proc_mem[0x50] = {};

    //popen cant use format string so workaround:
    sprintf(proc_mem, "/proc/%d/mem", pwntools_process_pid);
    int mem_fp = open(proc_mem, O_RDONLY);
    if (mem_fp == -1) {fprintf(stderr, "open mem"); exit(errno);}

    int err;

    for (int i = 1; i <= counter; i += 2) {
        // set lseek to mem region in /proc/mem we want to read from
        err = lseek(mem_fp, maps_offsets[i], SEEK_SET);
        if (err == -1) {fprintf(stderr, "lseek failed on mem"); exit(errno);}

        err = read(mem_fp,(unsigned char*)snapshot_buffer + buf_offsets[i],rdwr_offsets[i]);
        if (err == -1) {fprintf(stderr, "read on mem failed"); exit(errno);}
    }

    close(mem_fp);
    return snapshot_buffer;
}


// responsible for bringing a snapshot back into memory
void restore_snapshot(unsigned char* snapshot_buffer, pid_t pwntools_process_pid) {
    errno = 0;
    // set this up as iovecs's so that we can used process_vm_writev
    // lets up avoid going through a syscall meaning each iteration of fuzz is faster

    struct iovec local[num_region];
    struct iovec remote[num_region];

    // "local" iovec which is what we gonna overwrite the "remote / binary"
    // this overwrites the memory for the binary
    local[0].iov_base = snapshot_buffer;
    local[0].iov_len = rdwr_offsets[0];
    remote[0].iov_base = (void *)maps_offsets[0];
    remote[0].iov_len = rdwr_offsets[0];

    for (int i = 1; i <= num_region * 2; i += 2) {
        // for local:
        // base is the offset into the malloc'd memory region given by snapshot_buffer
        // len is the read/write length
        local[i].iov_base = (unsigned char*)buf_offsets[i];
        local[i].iov_len = rdwr_offsets[i];



        // for remote:
        // base is the offsets in proc/map we found earlier
        // len is the read/write length
        remote[i].iov_base = (void *)maps_offsets[i];
        remote[i].iov_len = rdwr_offsets[i];
    }


    process_vm_writev(pwntools_process_pid, local, num_region, remote, num_region, 0);
}