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
    seed: int = 42
    test_size: float = 0.2
    mongo_db_url: str = "mongodb://localhost:27017/sensor_fault_detection"

    @classmethod
    def from_env(cls) -> "Settings":
        settings = cls(
            data_path=Path(os.getenv("SFD_DATA_PATH", cls.data_path)),
            schema_path=Path(os.getenv("SFD_SCHEMA_PATH", cls.schema_path)),
            output_dir=Path(os.getenv("SFD_OUTPUT_DIR", cls.output_dir)),
            seed=int(os.getenv("SFD_SEED", cls.seed)),
            test_size=float(os.getenv("SFD_TEST_SIZE", cls.test_size)),
            mongo_db_url=os.getenv("MONGO_DB_URL", cls.mongo_db_url),
        )
        if not 0 < settings.test_size < 1:
            raise ValueError("SFD_TEST_SIZE must be between 0 and 1")
        return settings
