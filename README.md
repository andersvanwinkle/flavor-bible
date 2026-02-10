# Flavor Bible (Ingredient Pairings Explorer)

A lightweight web app for exploring **ingredient pairings** and “flavor affinities” from a curated dataset.

This project is designed as a fast, practical way to:
- discover complementary ingredients ("what else goes with X?")
- filter by techniques / cuisine signals
- browse and search a large pairing list without spreadsheets

> Portfolio note: This is intentionally minimal—simple UI + simple backend—so the core value (searching pairings quickly) is obvious.

## What it does
- Serves a small Flask app with a search interface
- Loads a dataset of ingredient pairings
- Returns matching rows and a short set of related suggestions

## Quickstart

### 1) Clone
```bash
git clone https://github.com/andersvanwinkle/flavor-bible.git
cd flavor-bible
```

### 2) Install
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3) Run
```bash
python app.py
```

Then open: http://127.0.0.1:5000

## Example
Search for an ingredient (e.g., `tomato`) to see pairings and adjacent suggestions.

A small sample output is included in [`demo/sample_output.txt`](demo/sample_output.txt).

## Repo metadata
Suggested topics:
- `data-science`
- `flavor`
- `flask`
- `search`
- `python`

## Notes / TODO
- Add a tiny test to validate the dataset loads
- Add a single screenshot/GIF of the search UI

---

Maintained by **Anders Van Winkle** — Data Scientist @ Meta
