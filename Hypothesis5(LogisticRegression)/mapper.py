#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import csv
import re

# 特殊トークン読み込み
try:
    with open("special_tokens.txt", "r", encoding="utf-8") as f:
        special_tokens = [line.strip().lower() for line in f if line.strip()]
except FileNotFoundError:
    special_tokens = []

def tokenize(text):
    tokens = []
    text = text.lower()
    for special in special_tokens:
        pattern = r'\b' + re.escape(special) + r'\b'
        if re.search(pattern, text):
            tokens.append(special)
            text = re.sub(pattern, ' ', text)
    words = re.findall(r'\b\w+\b', text)
    return tokens + words

reader = csv.reader(sys.stdin, delimiter=',')
header_skipped = False

for row in reader:
    if not header_skipped:
        header_skipped = True
        continue

    try:
        review_text = row[2]
        tokens = tokenize(review_text)
        for token in tokens:
            if token.strip():
                print(f"{token},1")
    except IndexError:
        continue
