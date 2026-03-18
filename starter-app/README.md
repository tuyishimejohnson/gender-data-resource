# Starter App (Runnable Baseline)

This is a ready-to-run Streamlit baseline for hackathon participants.

## What is included

- Multi-page Streamlit app (`Discovery`, `Dashboard`, `Data Quality`)
- Data loaders and filter utilities
- Basic quality parsing and status logic
- Basic test suite
- Sample data in `data/sample/`
- Full source data packaged as `data/full-data.zip`

## Quick start

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/streamlit run app.py
```

## Quick test check

```bash
.venv/Scripts/python -m unittest discover -s tests -v
```

## Data mode

- Default: app reads from `data/sample/`
- Optional full mode:
  1. unzip `data/full-data.zip` into `data/full/`
  2. set env var `HACKATHON_DATA_DIR=data/full`
  3. run app again

## Minimum demo flow

1. Use Discovery page to search/filter studies
2. Open Dashboard page to show trends/resource mix
3. Open Data Quality page to show caveats
4. Explain one policy/advocacy use case

## Optional advanced work

- Add link validation UI
- Add district/time comparisons
- Add export/report generator
- Add optional crawler refresh script
