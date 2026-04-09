#!/usr/bin/env python3
import sys

current_year = None
count = 0

for line in sys.stdin:
    year, val = line.strip().split('\t')
    if year == current_year:
        count += int(val)
    else:
        if current_year:
            print(f"{current_year}\t{count}")
        current_year = year
        count = int(val)

if current_year:
    print(f"{current_year}\t{count}")