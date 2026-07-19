from dataclasses import replace
from pathlib import Path

from sensor_fault_detection.full_pipeline import run_training
from sensor_fault_detection.settings import Settings


ROOT = Path(__file__).parent


def test_full_local_pipeline_syncs_under_versioned_prefix(tmp_path, monkeypatch):
    uploaded: list[tuple[Path, str]] = []

    class FakeArtifactStore:
        def __init__(self, settings):
            pass

        def upload_directory(self, directory, prefix=None):
            uploaded.append((directory, prefix))

    monkeypatch.setattr(
        "sensor_fault_detection.cloud.S3ArtifactStore", FakeArtifactStore
    )
    settings = replace(
        Settings.from_env(),
        source="local",
        data_path=ROOT / "fixtures/aps_synthetic.csv",
        schema_path=ROOT / "fixtures/schema.yaml",
        artifact_root=tmp_path / "artifacts",
        model_root=tmp_path / "models",
        s3_sync_enabled=True,
        s3_artifact_prefix="sensor-fault-detection",
    )

    result = run_training(settings)

    assert uploaded == [
        (
            result.run_dir / "model",
            f"sensor-fault-detection/{result.run_dir.name}/model",
        ),
        (
            result.run_dir / "data_validation",
            f"sensor-fault-detection/{result.run_dir.name}/data_validation",
        ),
    ]
    assert all("data_ingestion" not in str(directory) for directory, _ in uploaded)


def test_full_local_pipeline_promotes_model(tmp_path):
    settings = replace(
        Settings.from_env(),
        source="local",
        data_path=ROOT / "fixtures/aps_synthetic.csv",
        schema_path=ROOT / "fixtures/schema.yaml",
        artifact_root=tmp_path / "artifacts",
        model_root=tmp_path / "models",
    )

    result = run_training(settings)

    assert result.model_path.exists()
    assert result.promoted_model_path == tmp_path / "models/latest/model.joblib"
    assert result.promoted_model_path.exists()
    assert result.metrics_path.exists()
    assert result.drift_report_path.exists()
