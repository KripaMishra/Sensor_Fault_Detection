import sys
import types

from sensor_fault_detection.cloud import S3ArtifactStore
from sensor_fault_detection.settings import Settings


def test_artifact_store_uses_r2_endpoint_and_versioned_prefix(tmp_path, monkeypatch):
    uploaded: list[tuple[str, str, str]] = []

    class FakeClient:
        def upload_file(self, filename: str, bucket: str, key: str) -> None:
            uploaded.append((filename, bucket, key))

    def client(service: str, **kwargs: object) -> FakeClient:
        assert service == "s3"
        assert kwargs["endpoint_url"] == "https://r2.example.test"
        assert kwargs["aws_access_key_id"] == "access"
        assert kwargs["aws_secret_access_key"] == "secret"
        return FakeClient()

    monkeypatch.setitem(sys.modules, "boto3", types.SimpleNamespace(client=client))
    artifact = tmp_path / "model" / "model.joblib"
    artifact.parent.mkdir()
    artifact.write_bytes(b"model")

    store = S3ArtifactStore(
        Settings(
            s3_bucket="bucket",
            s3_artifact_prefix="sensor-fault-detection",
            s3_endpoint_url="https://r2.example.test",
            r2_access_key_id="access",
            r2_secret_access_key="secret",
        )
    )
    store.upload_directory(tmp_path, prefix="sensor-fault-detection/20260719T120000Z")

    assert uploaded == [
        (
            str(artifact),
            "bucket",
            "sensor-fault-detection/20260719T120000Z/model/model.joblib",
        )
    ]
