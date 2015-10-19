#include <cstdio>
#include <vector>
#include <thread>
#include "zsim_api.h"

static inline uint32_t get_cpuid() {
#ifdef __x86_64__
    uint32_t ebx;
    __asm__ __volatile__("" ::: "memory");
    __asm__ __volatile__("cpuid" : "=b"(ebx) : "a"(1) : "%ecx", "%edx");
    __asm__ __volatile__("" ::: "memory");
    return ebx >> 24;
#else
    return -1u;
#endif
}

static uint64_t dummy_compute(uint64_t amount) {
    uint64_t ret = 0;
    const uint64_t amplify = 1uL << 23;
    for (uint64_t i = 0; i < amount * amplify; i++)
        ret += i;
    return ret;
}

uint64_t thread_function(int tid) {
    printf("Thread %d: start on core %u\n", tid, get_cpuid());

    zsim_thread_setaffinity("c", tid + 4);

    printf("Thread %d: pin on core %u\n", tid, get_cpuid());

    // Thread excutes different numbers of instructions based on its thread id.
    // Check zsim.out for instruction counts on the pinning cores.
    return dummy_compute(tid);
}

int main() {
    printf("zsim API test\n");

    std::vector<std::thread> threadPool(4);
    for (uint32_t tid = 0; tid < 4; tid++) {
        threadPool[tid] = std::thread(thread_function, tid);
    }
    for (uint32_t tid = 0; tid < 4; tid++) {
        threadPool[tid].join();
    }

    printf("zsim API test done\n");

    return 0;
}


