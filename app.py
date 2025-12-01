#!/usr/bin/env python3
from flask import Flask, render_template, request
from pathlib import Path
import csv
import math

app = Flask(__name__)

# -----------------------------
# CONFIG
# -----------------------------
COMPONENTS = [
    "S-Indian", "Baloch", "Caucasian", "NE-Euro",
    "SE-Asian", "Siberian", "NE-Asian", "Papuan",
    "American", "Beringian", "Mediterranean", "SW-Asian",
    "San", "E-African", "Pygmy", "W-African",
]

DATA_PATH = Path(__file__).parent / "data" / "harappaworld_samples.csv"


# -----------------------------
# CORE LOGIC (same idea as CLI script)
# -----------------------------
def load_samples(csv_path: Path):
    rows = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            label = (r.get("label") or "").strip()
            if not label:
                continue
            if "AVERAGE" in label.upper():
                continue
            if not label:
                continue
            row = {"label": label}
            for c in COMPONENTS:
                val = r.get(c, "")
                try:
                    row[c] = float(val) if val != "" else 0.0
                except ValueError:
                    row[c] = 0.0
            rows.append(row)
    return rows


def normalize(profile: dict) -> dict:
    total = sum(profile.get(c, 0.0) for c in COMPONENTS)
    if total == 0:
        return profile
    factor = 100.0 / total
    return {c: profile.get(c, 0.0) * factor for c in COMPONENTS}


def euclid(a: dict, b: dict) -> float:
    return math.sqrt(sum((a[c] - b[c]) ** 2 for c in COMPONENTS))


def compute_distances(profile: dict, contains: str | None, top: int = 20):
    samples = load_samples(DATA_PATH)

    # filter by substring if requested
    if contains:
        sub = contains.lower()
        samples = [s for s in samples if sub in s["label"].lower()]

    prof_norm = normalize(profile)

    results = []
    for row in samples:
        samp_prof = {c: row[c] for c in COMPONENTS}
        samp_norm = normalize(samp_prof)
        d = euclid(prof_norm, samp_norm)
        results.append({
            "label": row["label"],
            "distance": d,
        })

    results.sort(key=lambda x: x["distance"])
    # add rank
    for i, r in enumerate(results, start=1):
        r["rank"] = i
    return results[:top], prof_norm


# -----------------------------
# ROUTES
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    # default empty profile for the form
    profile_vals = {c: "" for c in COMPONENTS}
    filter_contains = ""
    top_n = 20
    results = None
    normalized_profile = None

    if request.method == "POST":
        # build profile from form fields
        profile = {}
        for c in COMPONENTS:
            raw = request.form.get(c, "").strip()
            try:
                profile[c] = float(raw) if raw else 0.0
            except ValueError:
                profile[c] = 0.0

        filter_contains = request.form.get("contains", "").strip()
        try:
            top_n = int(request.form.get("top", "20"))
        except ValueError:
            top_n = 20

        results, normalized_profile = compute_distances(
            profile=profile,
            contains=filter_contains or None,
            top=top_n,
        )

        # keep what user typed so it stays in the form
        profile_vals = {c: request.form.get(c, "") for c in COMPONENTS}

    return render_template(
        "index.html",
        components=COMPONENTS,
        profile_vals=profile_vals,
        results=results,
        normalized_profile=normalized_profile,
        filter_contains=filter_contains,
        top_n=top_n,
    )


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5555))
    debug = True
    app.run(host="0.0.0.0", port=port, debug=debug)



