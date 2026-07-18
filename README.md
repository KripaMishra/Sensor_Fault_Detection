# Sensor Fault Detection

Educational MLOps portfolio project for binary APS component-failure classification from tabular sensor data.

> **Scope:** this repository provides an offline, reproducible batch workflow. It is not a safety-critical diagnostic system, production fleet service, or maintenance recommendation engine.

## What works

```text
CSV → schema validation → deterministic stratified split → preprocessing → classifier
                                                               ↓
                                              holdout metrics + model artifact
```

The public MVP uses a balanced logistic-regression baseline. It keeps the test split untouched and writes a model, metrics, confusion matrix, and run metadata.

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

## Limitations and roadmap

This release deliberately excludes MongoDB, S3, cloud deployment, authentication, web APIs, monitoring, model registries, scheduled retraining, and real-time inference. Those features should be added only after the local workflow has a documented dataset, stronger validation, and an evidence-backed product need.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Never commit credentials or private data.
