from pathlib import Path

from sensor_fault_detection.settings import Settings


def test_settings_load_from_environment(monkeypatch):
    monkeypatch.setenv("SFD_DATA_PATH", "fixtures/data.csv")
    monkeypatch.setenv("SFD_SEED", "7")
    monkeypatch.setenv("SFD_TEST_SIZE", "0.25")

    settings = Settings.from_env()

    assert settings.data_path == Path("fixtures/data.csv")
    assert settings.seed == 7
    assert settings.test_size == 0.25
