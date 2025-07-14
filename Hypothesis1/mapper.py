#!/usr/bin/env python3
import sys
import csv
import re

# Palabras clave positivas (experiencia inmersiva, técnica positiva)
positive_keywords = {
    "immersive",
    "atmosphere",
    "story",
    "characters",
    "world",
    "explore",
    "deep",
    "engaging",
    "captivating",
    "narrative",
    "optimized",
    "performance",
    "graphics",
    "visuals",
    "sound",
    "audio",
    "smooth",
    "stable",
    "polished",
    "details",
    "fun",
    "enjoyable",
    "excellent",
    "great",
    "wonderful",
    "amazing",
    "impressive",
    "recommend",
    "masterpiece",
    "unforgettable",
    "addictive",
    "fascinating",
    "innovative",
    "incredible",
    "magnificent",
    "solid",
}

# Palabras clave negativas (fallos técnicos, frustraciones)
negative_keywords = {
    "bug",
    "bugs",
    "glitch",
    "glitches",
    "crash",
    "crashes",
    "lag",
    "lags",
    "problems",
    "errors",
    "error",
    "frozen",
    "stutter",
    "stutters",
    "drops",
    "optimization",
    "performance",
    "frustrating",
    "repetitive",
    "monotonous",
    "boring",
    "controls",
    "design",
    "mechanics",
    "difficult",
    "unfair",
    "tedious",
    "bad",
    "terrible",
    "disappointing",
    "not recommend",
    "avoid",
    "unstable",
    "broken",
    "faulty",
    "issues",
    "critical",
    "unplayable",
    "unresponsive",
    "horrible",
    "awful",
}

# Combinamos todas para buscarlas en el texto
all_keywords = positive_keywords.union(negative_keywords)

csv_reader = csv.reader(sys.stdin)
header = next(csv_reader, None)  # Saltamos la cabecera

# Asegúrate de que la cabecera contiene los campos necesarios
for row in csv_reader:
    try:
        if len(row) < 7:
            continue

        review_text = row[2].strip().lower()
        sentiment = row[6].strip().lower()

        if sentiment not in ["positive", "negative"]:
            continue

        label = "pos" if sentiment == "positive" else "neg"
        words = re.findall(r"\b\w+\b", review_text)

        for word in words:
            if word in all_keywords:
                print(f"{label}_{word}\t1")

    except Exception:
        continue
