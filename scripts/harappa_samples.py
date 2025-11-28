#!/usr/bin/env python3

import csv
import math
import argparse
from pathlib import Path

# HarappaWorld components
COMPONENTS = [
    "S-Indian", "Baloch", "Caucasian", "NE-Euro",
    "SE-Asian", "Siberian", "NE-Asian", "Papuan",
    "American", "Beringian", "Mediterranean", "SW-Asian",
    "San", "E-African", "Pygmy", "W-African",
]

# Path to the samples CSV (relative to project root)
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "harappaworld_samples.csv"


def load_samples(csv_path: Path, contains: str | None = None, exclude_average: bool = True):
    """Load individual samples from the CSV, with optional label filtering."""
    rows = []
    contains_lower = contains.lower() if contains else None

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            label = (r.get("label") or "").strip()
            if not label:
                continue

            if exclude_average and label.upper().startswith("AVERAGE"):
                continue

            if contains_lower and contains_lower not in label.lower():
                continue

            row = {"id": label}
            for c in COMPONENTS:
                val = r.get(c, "")
                try:
                    row[c] = float(val) if val != "" else 0.0
                except ValueError:
                    row[c] = 0.0
            rows.append(row)
    return rows


def normalize(profile: dict) -> dict:
    """Normalize profile so components sum to ~100."""
    total = sum(profile.get(c, 0.0) for c in COMPONENTS)
    if total == 0:
        return profile
    factor = 100.0 / total
    return {c: profile.get(c, 0.0) * factor for c in COMPONENTS}


def euclid(a: dict, b: dict) -> float:
    """Euclidean distance between two profiles."""
    return math.sqrt(sum((a[c] - b[c]) ** 2 for c in COMPONENTS))


def load_profile(path: Path) -> dict:
    """Load your profile from a simple key: value text file."""
    profile = {}
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip()
            try:
                profile[k] = float(v)
            except ValueError:
                profile[k] = 0.0

    # ensure all components exist
    for c in COMPONENTS:
        profile.setdefault(c, 0.0)

    return profile


def main():
    parser = argparse.ArgumentParser(
        description="Compute Euclidean distance to HarappaWorld INDIVIDUAL samples."
    )
    parser.add_argument(
        "--profile",
        required=True,
        help="Path to your profile text file (key: value per line).",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=20,
        help="Number of closest samples to show.",
    )
    parser.add_argument(
        "--no-normalize",
        action="store_true",
        help="Disable normalization of profiles to 100%.",
    )
    parser.add_argument(
        "--contains",
        help="Only include samples whose label contains this text (case-insensitive).",
    )
    parser.add_argument(
        "--include-average",
        action="store_true",
        help="Include rows whose label starts with 'AVERAGE'.",
    )

    args = parser.parse_args()

    profile_path = Path(args.profile)
    prof = load_profile(profile_path)

    print("Raw profile as read from file:")
    for c in COMPONENTS:
        print(f"  {c:12s}: {prof[c]:6.2f}")

    if not args.no_normalize:
        prof = normalize(prof)
        print("\nNormalized profile (sums to ~100):")
        for c in COMPONENTS:
            print(f"  {c:12s}: {prof[c]:6.2f}")

    samples = load_samples(
        DATA_PATH,
        contains=args.contains,
        exclude_average=not args.include_average,
    )

    if not samples:
        print("\nNo samples loaded. Check:")
        print(f"  CSV path: {DATA_PATH}")
        if args.contains:
            print(f"  Filter: label contains '{args.contains}'")
        return

    print(f"\nLoaded {len(samples)} samples from: {DATA_PATH}")

    results = []
    for row in samples:
        samp_prof = {c: row[c] for c in COMPONENTS}
        if not args.no_normalize:
            samp_prof = normalize(samp_prof)
        d = euclid(prof, samp_prof)
        results.append((row["id"], d))

    results.sort(key=lambda x: x[1])

    print(f"\nTop {args.top} closest individual samples:\n")
    for label, dist in results[: args.top]:
        print(f"{label:45s}  distance = {dist:7.4f}")


if __name__ == "__main__":
    main()
