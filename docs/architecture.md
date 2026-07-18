# Architecture

The public MVP is intentionally a local batch pipeline:

1. `data.py` loads CSV input, applies the schema, rejects malformed columns, maps labels, and creates a deterministic stratified split.
2. `model.py` fits imputation, robust scaling, and a balanced logistic-regression classifier on training rows only.
3. `model.py` evaluates the untouched holdout and writes JSON/CSV reports plus a serialized artifact.
4. `cli.py` exposes `train` and `predict` commands without a server or cloud dependency.

MongoDB, S3, FastAPI, Docker deployment, monitoring, and model registries are intentionally outside this MVP boundary.
