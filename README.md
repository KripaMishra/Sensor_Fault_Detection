# Sensor Fault Detection

Educational MLOps portfolio project for binary APS component-failure classification from tabular sensor data.

> **Scope:** this repository provides an offline, reproducible batch workflow. It is not a safety-critical diagnostic system, production fleet service, or maintenance recommendation engine.

## What works

```text
CSV → schema validation → deterministic stratified split → preprocessing → classifier
                                                               ↓
                                              holdout metrics + model artifact
```

The public MVP uses a balanced logistic-regression baseline. It keeps the test split untouched and writes a model, metrics, confusion matrix, and run metadata. The full pipeline adds local/MongoDB/S3 ingestion, validation and drift reporting, model promotion, and an optional FastAPI service without putting credentials in source.

## Quickstart

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python -m pip install -e ".[dev]"
python -m sensor_fault_detection train \
  --data tests/fixtures/aps_synthetic.csv \
  --schema tests/fixtures/schema.yaml \
  --output-dir outputs/example
python -m sensor_fault_detection predict \
  --data tests/fixtures/aps_synthetic.csv \
  --model outputs/example/model.joblib \
  --schema tests/fixtures/schema.yaml \
  --output outputs/example/predictions.csv
```

Run quality checks with `ruff check src tests` and `pytest -q`.

## Configuration

Runtime defaults are centralized in `sensor_fault_detection.settings.Settings`. Copy `.env.example` to `.env` when local overrides are needed; real credentials belong in a secret manager and must never be committed. The offline MVP does not connect to MongoDB, but a safe localhost placeholder is included for future adapters.

## Data contract

The real APS dataset is intentionally not committed. See [docs/data.md](docs/data.md) for provenance, licensing, and acquisition requirements. The checked-in fixture is synthetic and exists only to exercise the pipeline without network access.

For a real run, provide a CSV containing the `class` target (`neg` or `pos`) and the numerical columns listed in `configs/schema.yaml`. Missing numeric values are imputed by the training pipeline; unknown columns and non-numeric values are rejected.

## Outputs and evaluation

A training run writes to an ignored output directory:

- `model.joblib` — serialized preprocessing and classifier pipeline;
- `metrics.json` — accuracy, precision, recall, F1, and confusion-matrix counts;
- `confusion_matrix.csv` — readable holdout matrix;
- `metadata.json` — seed, split, data path, schema path, and model details.

Metrics are measured once on a deterministic held-out split. False positives and false negatives have different operational costs in real fleet workflows; this educational baseline does not claim a cost-optimized threshold. See [docs/reproducibility.md](docs/reproducibility.md).

## Full pipeline and API

Install optional integrations with `python -m pip install -e ".[full]"`. Run the orchestrated pipeline with:

```bash
sensor-fault-detection pipeline-train --source local --data /path/to/aps.csv
# or use SFD_SOURCE=mongo / SFD_SOURCE=s3 in a private environment
sensor-fault-detection serve
```

The run performs ingestion, schema validation, deterministic splitting, drift reporting, training, artifact storage, and model promotion to `models/latest/model.joblib`. The API exposes `/health`, `POST /train`, and `POST /predict`; uploads are bounded and processed without shared global state. Docker starts the API with `docker build -f dockerfile -t sensor-fault-detection .` followed by `docker run --env-file .env -p 8080:8080 sensor-fault-detection`.

## Limitations and roadmap

MongoDB, S3, and the API are optional integrations, not proof of production readiness. Authentication, scheduled retraining, model registries, observability, and deployment hardening remain follow-up work. The local `PENDENCIES.md` handoff checklist records the configuration and external prerequisites for each integration; it is intentionally not committed.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Never commit credentials or private data.
