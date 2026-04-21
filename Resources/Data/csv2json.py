#!/usr/bin/env python3

import csv
import json
import sys


def make_json(csvPath, jsonPath):
    with open(csvPath, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    with open(jsonPath, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=4)

    print(f"Wrote {len(rows)} records to {jsonPath}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: csv2json.py <input.csv> <output.json>")
        sys.exit(1)

    make_json(sys.argv[1], sys.argv[2])
