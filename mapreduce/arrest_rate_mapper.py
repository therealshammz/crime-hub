#!/usr/bin/env python3
import sys, csv, io
for line in sys.stdin:
    try:
        row = next(csv.reader(io.StringIO(line.strip())))
        if row[0] == 'ID':
            continue
        t = row[5].strip()
        arrest = 1 if row[8].strip().lower() == 'true' else 0
        if t:
            print(f"{t}\t1,{arrest}")
    except:
        pass
