# Participant Pack

This folder contains everything teams need to build and submit a hackathon solution.

## Start here (order)

1. Open `starter-app/README.md`
2. Run starter app locally (commands below)
3. Read `challenge-brief.md`
4. Read `data-pack-guide.md`
5. Build according to `judging-rubric-participant-view.md`
6. Submit using `submission-guide.md`

## Starter app quick run

From repo root:

```bash
cd starter-app
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/streamlit run app.py
```

Validation summary is available in `starter-app/VALIDATION.md`.

## Mandatory output

- A **working Streamlit prototype** that improves visibility/usability of gender data resources for advocacy.
- Accepted forms: dashboard, searchable catalog, or hybrid.

## Core baseline files

In this repository:

- sample data: `starter-app/data/sample/`
- full dataset zip: `starter-app/data/full-data.zip`

## Reference docs

- `data-dictionary.md`
- `data-provenance-policy.md`
