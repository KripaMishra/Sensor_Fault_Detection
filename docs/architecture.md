# Architecture

The public MVP is intentionally a local batch pipeline:

1. `data.py` loads CSV input, applies the schema, rejects malformed columns, maps labels, and creates a deterministic stratified split.
2. `model.py` fits imputation, robust scaling, and a balanced logistic-regression classifier on training rows only.
3. `model.py` evaluates the untouched holdout and writes JSON/CSV reports plus a serialized artifact.
4. `cli.py` exposes `train`, `predict`, `pipeline-train`, and `serve` commands.
5. `sources.py` provides local CSV, MongoDB, and S3 input adapters; `cloud.py` uploads artifacts through boto3's credential chain.
6. `api.py` provides bounded stateless prediction uploads and guarded training requests.

MongoDB, S3, FastAPI, and Docker are optional integrations. Authentication, model registries, scheduled retraining, and production observability remain outside this portfolio release.
