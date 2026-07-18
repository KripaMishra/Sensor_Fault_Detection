# Data contract

The project targets the public APS component-failure classification task. The real dataset is not included in this repository because redistribution rights and personal-data considerations must be verified independently before publication.

Before using a real dataset:

1. Obtain it from an authoritative source and record the URL, retrieval date, license, and checksum.
2. Confirm that redistribution and model artifacts are permitted by the dataset terms.
3. Keep the raw file outside Git, for example under `data/` (which is ignored).
4. Ensure the target column is `class` with `neg` and `pos` labels.
5. Validate the feature set against `configs/schema.yaml`.

The synthetic fixture under `tests/fixtures/` is safe for CI and is not representative of real-world performance.
