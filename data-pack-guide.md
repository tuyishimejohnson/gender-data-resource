# Data Pack Guide (Participants)

## Baseline data

Use these files from `app/crawler-output-full/`:

- `studies.csv` (main index)
- `study_resources.csv` (linked resources)
- `quality_report.csv` (quality overlays)

Read field definitions in `../shared/data-dictionary.md`.

## Recommended workflow

1. Load `studies.csv` as your primary table.
2. Join `study_resources.csv` on `study_id`.
3. Join `quality_report.csv` on `study_id`.
4. Expose filters for year, geography, resource type, and quality flags.
5. Show source URLs and access status clearly.

## Direct NISR retrieval flow

Use this for high-value resources in demo scenarios:

1. Identify candidate in your app.
2. Open `url` or `get_microdata_url`.
3. Confirm availability status.
4. Record provenance fields (see shared policy).

## Practical tips

- If files feel large, start with a subset for iteration.
- Keep null-safe logic for missing metadata fields.
- Surface uncertainty in UI rather than hiding it.
