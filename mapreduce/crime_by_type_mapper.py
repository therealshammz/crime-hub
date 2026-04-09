#!/usr/bin/env python3
import sys, csv, io
for line in sys.stdin:
    try:
        row = next(csv.reader(io.StringIO(line.strip())))
        if row[0] == 'ID':
            continue
        t = row[5].strip()
        if t:
            print(f"{t}\t1")
    except:
        pass
