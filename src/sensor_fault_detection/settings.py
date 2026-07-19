from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """Central runtime configuration loaded from environment variables."""

    data_path: Path = Path("data/aps.csv")
    schema_path: Path = Path("configs/schema.yaml")
    output_dir: Path = Path("outputs/latest")
    artifact_root: Path = Path("artifacts")
    model_root: Path = Path("models")
    seed: int = 42
    test_size: float = 0.2
    source: str = "local"
    mongo_db_url: str = "mongodb://localhost:27017/sensor_fault_detection"
    mongo_database: str = "sensor_data"
    mongo_collection: str = "sensor_collection"
    s3_bucket: str = ""
    s3_artifact_prefix: str = "sensor-fault-detection"
    s3_data_key: str = ""
    s3_endpoint_url: str = ""
    r2_access_key_id: str = ""
    r2_secret_access_key: str = ""
    aws_region: str = "auto"
    s3_sync_enabled: bool = False
    drift_threshold: float = 0.05
    api_host: str = "127.0.0.1"
    api_port: int = 8080
    max_upload_bytes: int = 10 * 1024 * 1024
    cors_origins: tuple[str, ...] = ("http://localhost:3000",)

    @classmethod
    def from_env(cls) -> "Settings":
        settings = cls(
            data_path=Path(os.getenv("SFD_DATA_PATH", cls.data_path)),
            schema_path=Path(os.getenv("SFD_SCHEMA_PATH", cls.schema_path)),
            output_dir=Path(os.getenv("SFD_OUTPUT_DIR", cls.output_dir)),
            artifact_root=Path(os.getenv("SFD_ARTIFACT_ROOT", cls.artifact_root)),
            model_root=Path(os.getenv("SFD_MODEL_ROOT", cls.model_root)),
            seed=int(os.getenv("SFD_SEED", cls.seed)),
            test_size=float(os.getenv("SFD_TEST_SIZE", cls.test_size)),
            source=os.getenv("SFD_SOURCE", cls.source),
            mongo_db_url=os.getenv("MONGO_DB_URL", cls.mongo_db_url),
            mongo_database=os.getenv("MONGO_DATABASE", cls.mongo_database),
            mongo_collection=os.getenv("MONGO_COLLECTION", cls.mongo_collection),
            s3_bucket=os.getenv("SFD_R2_BUCKET", cls.s3_bucket),
            s3_artifact_prefix=os.getenv("SFD_R2_ARTIFACT_PREFIX", cls.s3_artifact_prefix),
            s3_data_key=os.getenv("SFD_R2_DATA_KEY", cls.s3_data_key),
            s3_endpoint_url=os.getenv("R2_ENDPOINT_URL", cls.s3_endpoint_url),
            r2_access_key_id=os.getenv("R2_ACCESS_KEY_ID", cls.r2_access_key_id),
            r2_secret_access_key=os.getenv("R2_SECRET_ACCESS_KEY", cls.r2_secret_access_key),
            aws_region=cls.aws_region,
            s3_sync_enabled=os.getenv("SFD_R2_SYNC_ENABLED", "false").lower() == "true",
            drift_threshold=float(os.getenv("SFD_DRIFT_THRESHOLD", cls.drift_threshold)),
            api_host=os.getenv("SFD_API_HOST", cls.api_host),
            api_port=int(os.getenv("SFD_API_PORT", cls.api_port)),
            max_upload_bytes=int(os.getenv("SFD_MAX_UPLOAD_BYTES", cls.max_upload_bytes)),
            cors_origins=tuple(
                origin.strip()
                for origin in os.getenv("SFD_CORS_ORIGINS", ",".join(cls.cors_origins)).split(",")
                if origin.strip()
            ),
        )
        if settings.source not in {"local", "mongo", "r2"}:
            raise ValueError("SFD_SOURCE must be local, mongo, or r2")
        if settings.source == "r2" or settings.s3_sync_enabled:
            settings.validate_r2()
        if not 0 < settings.test_size < 1:
            raise ValueError("SFD_TEST_SIZE must be between 0 and 1")
        if not 0 < settings.drift_threshold < 1:
            raise ValueError("SFD_DRIFT_THRESHOLD must be between 0 and 1")
        return settings

    def validate_r2(self) -> None:
        missing = [
            name
            for name, value in (
                ("SFD_R2_BUCKET", self.s3_bucket),
                ("R2_ENDPOINT_URL", self.s3_endpoint_url),
                ("R2_ACCESS_KEY_ID", self.r2_access_key_id),
                ("R2_SECRET_ACCESS_KEY", self.r2_secret_access_key),
            )
            if not value
        ]
        if missing:
            raise ValueError(f"R2 configuration requires: {', '.join(missing)}")
        if not self.s3_endpoint_url.startswith("https://"):
            raise ValueError("R2_ENDPOINT_URL must use https://")
