#!/usr/bin/env python3
import sys

current_key = None
count = 0

for line in sys.stdin:
    try:
        key, value = line.strip().split("\t")
        value = int(value)

        if key == current_key:
            count += value
        else:
            if current_key is not None:
                print(f"{current_key}\t{count}")
            current_key = key
            count = value
    except:
        continue

if current_key is not None:
    print(f"{current_key}\t{count}")
