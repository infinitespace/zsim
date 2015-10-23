#include "zsim_api.h"
#include <cstdio>

int zsim_thread_setaffinity(const char* coreName, uint32_t coreIndex) {
    printf("zsim_thread_setaffinity: ignored when not running in zsim!\n");
    return 0;
}

