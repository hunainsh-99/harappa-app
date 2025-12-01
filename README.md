<<<<<<< HEAD
# Harappa World Distance Calculator

A complete tool for calculating Euclidean genetic distances between a user's HarappaWorld profile and 1,985 individual HarappaWorld samples collected across South and Central Asia.

This project includes:

- A Python backend (with virtual environment support)
- An interactive frontend (HTML/JS)
- A dataset containing nearly two thousand HarappaWorld individual samples
- Optional filtering (e.g., by population labels such as "Punjabi")

The tool lets you input your HarappaWorld percentages and returns the closest matching individuals from the dataset.

---

## 🧬 Dataset Summary

This project includes a cleaned dataset extracted from 41 pages of the *South & Central Asia HarappaWorld* report.

- **Total individual samples:** 1,985  
- **Columns:**  
  - `label` (sample identifier)  
  - 16 HarappaWorld admixture components

### HarappaWorld components used:

- S-Indian  
- Baloch  
- Caucasian  
- NE-Euro  
- SE-Asian  
- Siberian  
- NE-Asian  
- Papuan  
- American  
- Beringian  
- Mediterranean  
- SW-Asian  
- San  
- E-African  
- Pygmy  
- W-African  

All profiles (yours + samples) may optionally be normalized to sum to 100%.

---



=======
# Harappa App – HarappaWorld Distance Explorer

This project lets you compare your own HarappaWorld admixture profile to a large set of **individual samples** using **Euclidean distance** on the 16 HarappaWorld components.

You run a simple Python script (and optionally a small Flask web app) that:
- reads your profile from a text file,
- reads the `harappaworld_samples.csv` dataset,
- computes Euclidean distances between your profile and every sample,
- prints or displays the closest matches.

The dataset currently includes **1,845 individual HarappaWorld samples** (before any filtering or removal of "AVERAGE" rows).

---

## Project structure

```text
harappa-app/
├── app.py                  # Optional Flask front end
├── my_profile.txt          # Your HarappaWorld percentages
├── README.md
├── requirements.txt        # Python dependencies (Flask, pandas, etc.)
├── data/
│   └── harappaworld_samples.csv   # Individual samples dataset
└── scripts/
    └── harappa_samples.py  # CLI distance tool for individual samples
# harappa-app
>>>>>>> 8ce2081 (Update README and app entrypoint for deployment)
