#!/usr/bin/env python3
import sys
import csv
import re

# Define keyword sets for positive and negative review analysis.
# These keywords are associated with immersive gameplay/technical quality (positive)
# and technical failures/gameplay frustrations (negative), as per Hypothesis 1.
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
    "performance",  # Can also be used in negative contexts (e.g., "bad optimization")
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

# Combine both sets of keywords into one for efficient lookup.
# The sentiment label (pos/neg) will be prepended to the word in the output key.
all_keywords = positive_keywords.union(negative_keywords)

# Use csv.reader to handle CSV data, including fields with commas.
# sys.stdin reads input provided by Hadoop.
csv_reader = csv.reader(sys.stdin)

# Iterate over each row (review) from the input.
# Assuming review text is in the 3rd column (index 2) and score in the 4th (index 3).
for row_fields in csv_reader:
    try:
        # Ensure the row has enough columns to avoid IndexError.
        if len(row_fields) < 4:
            continue  # Skip malformed rows

        review_text = (
            row_fields[2].strip().lower()
        )  # Get review text, strip whitespace, convert to lowercase.
        review_score = row_fields[3].strip()  # Get review score.

        # Filter reviews to only include those with score '1' (positive) or '-1' (negative).
        if review_score not in ["1", "-1"]:
            continue  # Skip reviews with irrelevant scores.

        # Determine the sentiment label for the current review.
        sentiment_label = "pos" if review_score == "1" else "neg"

        # Tokenize the review text: find all alphanumeric words.
        words_in_review = re.findall(r"\b\w+\b", review_text)

        # For each word in the review, check if it's in our predefined keywords.
        for word in words_in_review:
            if word in all_keywords:
                # Emit a key-value pair:
                # Key: "sentiment_label_word" (e.g., "pos_gameplay", "neg_bug")
                # Value: "1" (to be summed by the reducer)
                print(f"{sentiment_label}_{word}\t1")

    except Exception:
        # Basic error handling: skip rows that cause unexpected errors.
        # For debugging, you could print the error to sys.stderr.
        continue
