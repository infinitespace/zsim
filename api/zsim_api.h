#ifndef __ZSIM_API_H__
#define __ZSIM_API_H__

#include <cstdint>

#ifdef __cplusplus
extern "C" {
#endif

#define ATTR_HOOK_FUNC __attribute__((externally_visible,noinline))

int zsim_thread_setaffinity(const char* coreName, uint32_t coreIndex) ATTR_HOOK_FUNC;

#undef ATTR_HOOK_FUNC

#ifdef __cplusplus
}
#endif

#endif /*__ZSIM_API_H__*/
