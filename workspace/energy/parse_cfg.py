import sys
import os

def parse(filename):
    with open(filename) as f: lines = f.readlines()
    lennum = len(lines)
    idx = 0
    while idx < lennum:
        lines[idx] = lines[idx].strip()
        lines[idx] = lines[idx].strip('\t\n')
        if len(lines[idx]) == 0: 
            del lines[idx]
            lennum -= 1
        else:
            idx += 1
    # return lines
    return loadtoDict(lines, lennum)

def loadtoDict(lines, lennum):
    idx = 0
    while idx < lennum:
        if len(lines) >= 3 and lines[idx][:3] == 'sys':
            break
        else:
            idx += 1
    d = {}
    cur = d
    stack = []
    stack.append(d)
    while idx < lennum:
        if lines[idx][-1] == '{':
            key = lines[idx].split('=')[0].strip()
            val = {}
            stack.append(cur)
            cur[key] = val
            cur = cur[key]
        elif lines[idx] == '};':
            cur = stack.pop()
        else:
            key = lines[idx].split('=')[0].strip().strip('\";')
            # print lines[idx].split('=')
            val = lines[idx].split('=')[1].strip().strip('\";')
            cur[key] = val
        idx += 1
        # print idx, d
    return d
