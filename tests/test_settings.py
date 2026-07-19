from pathlib import Path

import pytest

from sensor_fault_detection.settings import Settings


def test_settings_load_r2_from_environment(monkeypatch):
    monkeypatch.setenv("SFD_SOURCE", "r2")
    monkeypatch.setenv("SFD_R2_BUCKET", "models")
    monkeypatch.setenv("R2_ENDPOINT_URL", "https://r2.example.test")
    monkeypatch.setenv("R2_ACCESS_KEY_ID", "access")
    monkeypatch.setenv("R2_SECRET_ACCESS_KEY", "secret")

    settings = Settings.from_env()

    assert settings.source == "r2"
    assert settings.s3_bucket == "models"
    assert settings.s3_endpoint_url == "https://r2.example.test"


def test_settings_rejects_incomplete_r2_configuration(monkeypatch):
    monkeypatch.setenv("SFD_SOURCE", "r2")
    monkeypatch.setenv("SFD_R2_BUCKET", "models")
    monkeypatch.setenv("R2_ENDPOINT_URL", "https://r2.example.test")
    monkeypatch.delenv("R2_ACCESS_KEY_ID", raising=False)
    monkeypatch.delenv("R2_SECRET_ACCESS_KEY", raising=False)

    with pytest.raises(ValueError, match="R2 configuration requires"):
        Settings.from_env()


def test_settings_rejects_s3_source(monkeypatch):
    monkeypatch.setenv("SFD_SOURCE", "s3")

    with pytest.raises(ValueError, match="local, mongo, or r2"):
        Settings.from_env()


def test_settings_load_from_environment(monkeypatch):
    monkeypatch.setenv("SFD_DATA_PATH", "fixtures/data.csv")
    monkeypatch.setenv("SFD_SEED", "7")
    monkeypatch.setenv("SFD_TEST_SIZE", "0.25")

    settings = Settings.from_env()

    assert settings.data_path == Path("fixtures/data.csv")
    assert settings.seed == 7
    assert settings.test_size == 0.25
