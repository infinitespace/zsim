/** $lic$
 * Copyright (C) 2012-2015 by Massachusetts Institute of Technology
 * Copyright (C) 2010-2013 by The Board of Trustees of Stanford University
 *
 * This file is part of zsim.
 *
 * zsim is free software; you can redistribute it and/or modify it under the
 * terms of the GNU General Public License as published by the Free Software
 * Foundation, version 2.
 *
 * If you use this software in your research, we request that you reference
 * the zsim paper ("ZSim: Fast and Accurate Microarchitectural Simulation of
 * Thousand-Core Systems", Sanchez and Kozyrakis, ISCA-40, June 2013) as the
 * source of the simulator in any publications that use this software, and that
 * you send us a citation of your work.
 *
 * zsim is distributed in the hope that it will be useful, but WITHOUT ANY
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
 * details.
 *
 * You should have received a copy of the GNU General Public License along with
 * this program. If not, see <http://www.gnu.org/licenses/>.
 */

#include "core_name_map.h"
#include "g_std/g_vector.h"
#include "log.h"

struct CoreGroup {
    g_string name;
    uint32_t firstCid;
    uint32_t count;

    CoreGroup(const g_string& name_, const uint32_t firstCid_, const uint32_t count_)
        : name(name_), firstCid(firstCid_), count(count_) {}
};

static g_vector<CoreGroup> coreNameList;

void addCoreName(const g_string& name, const uint32_t count) {
    for (auto it = coreNameList.cbegin(); it != coreNameList.cend(); ++it) {
        if (it->name == name) {
            panic("CoreNameMap: core name %s already exists.", name.c_str());
        }
    }
    uint32_t totalCores = 0;
    if (!coreNameList.empty()) {
        auto& lastCoreGroup = coreNameList.back();
        totalCores = lastCoreGroup.firstCid + lastCoreGroup.count;
    }
    coreNameList.emplace_back(name, totalCores, count);
}

uint32_t getCidFromCoreName(const g_string& name, const uint32_t offset) {
    for (auto it = coreNameList.cbegin(); it != coreNameList.cend(); ++it) {
        if (it->name == name) {
            if (offset >= it->count) {
                panic("CoreNameMap: offset %u exceeds core count.", offset);
            }
            return it->firstCid + offset;
        }
    }
    return -1u;
}

