# Architecture

The public MVP is intentionally a local batch pipeline:

1. `data.py` loads CSV input, applies the schema, rejects malformed columns, maps labels, and creates a deterministic stratified split.
2. `model.py` fits imputation, robust scaling, and a balanced logistic-regression classifier on training rows only.
3. `model.py` evaluates the untouched holdout and writes JSON/CSV reports plus a serialized artifact.
4. `cli.py` exposes `train`, `predict`, `pipeline-train`, and `serve` commands.
5. `sources.py` provides local CSV, MongoDB, and Cloudflare R2-compatible input adapters; `cloud.py` uploads versioned artifacts through boto3's S3-compatible API.
6. `api.py` provides bounded stateless prediction uploads and guarded training requests.

MongoDB, Cloudflare R2, FastAPI, and Docker are optional integrations. R2 stores versioned run artifacts but is not a full model registry; authentication, registry migration, scheduled retraining, and production observability remain outside this portfolio release.
