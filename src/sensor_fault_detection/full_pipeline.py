from __future__ import annotations

import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .data import DatasetSchema, load_training_data, split_data, validate_dataframe
from .model import train
from .monitoring import detect_dataset_drift, write_drift_report
from .settings import Settings
from .sources import load_source


@dataclass(frozen=True)
class PipelineResult:
    run_dir: Path
    model_path: Path
    promoted_model_path: Path
    metrics_path: Path
    drift_report_path: Path


def _promote_model(model_path: Path, model_root: Path) -> Path:
    destination = model_root / "latest" / "model.joblib"
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(model_path, destination)
    return destination


def run_training(settings: Settings) -> PipelineResult:
    schema = DatasetSchema.from_yaml(settings.schema_path)
    frame = validate_dataframe(load_source(settings), schema, require_target=True)

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = settings.artifact_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    feature_store = run_dir / "data_ingestion" / "feature_store" / "sensor.csv"
    feature_store.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(feature_store, index=False)

    features, target = load_training_data(feature_store, schema)
    train_features, test_features, _, _ = split_data(
        features, target, test_size=settings.test_size, seed=settings.seed
    )
    ingested_dir = run_dir / "data_ingestion" / "ingested"
    ingested_dir.mkdir(parents=True, exist_ok=True)
    frame.loc[train_features.index].to_csv(ingested_dir / "train.csv", index=False)
    frame.loc[test_features.index].to_csv(ingested_dir / "test.csv", index=False)

    training_dir = run_dir / "model"
    train(
        feature_store,
        settings.schema_path,
        training_dir,
        seed=settings.seed,
        test_size=settings.test_size,
    )
    drift_report_path = run_dir / "data_validation" / "drift_report.yaml"
    write_drift_report(
        drift_report_path,
        detect_dataset_drift(train_features, test_features, threshold=settings.drift_threshold),
    )
    promoted = _promote_model(training_dir / "model.joblib", settings.model_root)

    if settings.s3_sync_enabled:
        from .cloud import S3ArtifactStore

        S3ArtifactStore(settings).upload_directory(run_dir)

    return PipelineResult(
        run_dir=run_dir,
        model_path=training_dir / "model.joblib",
        promoted_model_path=promoted,
        metrics_path=training_dir / "metrics.json",
        drift_report_path=drift_report_path,
    )
