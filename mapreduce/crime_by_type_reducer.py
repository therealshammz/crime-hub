#!/usr/bin/env python3
import sys
current, count = None, 0
for line in sys.stdin:
    k, v = line.strip().split('\t')
    if k == current:
        count += int(v)
    else:
        if current:
            print(f"{current}\t{count}")
        current, count = k, int(v)
if current:
    print(f"{current}\t{count}")
