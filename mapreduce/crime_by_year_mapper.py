#!/usr/bin/env python3
import sys
import csv
import io

for line in sys.stdin:
    try:
        row = next(csv.reader(io.StringIO(line.strip())))
        if row[0] == 'ID':
            continue
        year = row[17].strip()
        if year.isdigit():
            print(f"{year}\t1")
    except:
        pass