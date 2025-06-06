#!/usr/bin/env python3
import sys
import csv
import re

keywords = {"fun", "awesome", "boring", "love", "hate", "recommend", "bad"}

reader = csv.reader(sys.stdin)

for fields in reader:
    try:
        review_text = fields[2].strip().lower()
        score = fields[3].strip()

        if score not in ["1", "-1"]:
            continue

        label = "pos" if score == "1" else "neg"
        words = re.findall(r"\b\w+\b", review_text)

        for word in words:
            if word in keywords:
                print(f"{label}_{word}\t1")
    except Exception:
        continue
