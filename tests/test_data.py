from pathlib import Path

import pandas as pd
import pytest

from sensor_fault_detection.data import DatasetSchema, load_training_data, split_data, validate_dataframe


ROOT = Path(__file__).parent
SCHEMA = DatasetSchema.from_yaml(ROOT / "fixtures/schema.yaml")
DATA = ROOT / "fixtures/aps_synthetic.csv"


def test_schema_rejects_missing_feature():
    frame = pd.read_csv(DATA).drop(columns=["sensor_d"])
    with pytest.raises(ValueError, match="Missing required columns"):
        validate_dataframe(frame, SCHEMA, require_target=True)


def test_split_is_deterministic_and_stratified():
    features, target = load_training_data(DATA, SCHEMA)
    first = split_data(features, target, test_size=0.2, seed=42)
    second = split_data(features, target, test_size=0.2, seed=42)
    pd.testing.assert_frame_equal(first[0], second[0])
    assert first[2].value_counts().to_dict() == {0: 8, 1: 8}
    assert first[3].value_counts().to_dict() == {0: 2, 1: 2}
