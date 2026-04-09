#!/usr/bin/env python3
import sys
current, total, arrests = None, 0, 0
for line in sys.stdin:
    k, v = line.strip().split('\t')
    count, arrest = map(int, v.split(','))
    if k == current:
        total += count
        arrests += arrest
    else:
        if current:
            rate = round((arrests / total) * 100, 2) if total > 0 else 0
            print(f"{current}\t{total}\t{arrests}\t{rate}%")
        current, total, arrests = k, count, arrest
if current:
    rate = round((arrests / total) * 100, 2) if total > 0 else 0
    print(f"{current}\t{total}\t{arrests}\t{rate}%")
