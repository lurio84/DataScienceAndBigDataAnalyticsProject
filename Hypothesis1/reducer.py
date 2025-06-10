#!/usr/bin/env python3
import sys

current_key = None  # Stores the key currently being processed.
current_count = 0  # Accumulates the count for the current key.

# Iterate over each line from the input (which comes from the Mapper, sorted by key).
for line in sys.stdin:
    try:
        # Strip leading/trailing whitespace and split the line by tab to get key and value.
        # Example line: "pos_gameplay\t1"
        key, value_str = line.strip().split("\t")
        value = int(value_str)  # Convert the value string to an integer.

        # If the current key is the same as the one we're accumulating, add the value.
        if key == current_key:
            current_count += value
        else:
            # If the key has changed, it means we've finished processing the previous key's group.
            # Print the accumulated count for the previous key.
            if current_key is not None:
                print(f"{current_key}\t{current_count}")

            # Start accumulating for the new key.
            current_key = key
            current_count = value
    except ValueError:
        # Handles cases where the value cannot be converted to an integer (malformed input line).
        # sys.stderr.write(f"Skipping malformed line (ValueError): {line}\n")
        continue
    except Exception:
        # Catches any other unexpected errors during line processing.
        # sys.stderr.write(f"Error processing line: {line}, Error: {e}\n")
        continue

# After the loop finishes, there will be one last key-count pair that hasn't been printed yet.
# This ensures that the final accumulated count is also outputted.
if current_key is not None:
    print(f"{current_key}\t{current_count}")
