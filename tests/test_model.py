from pathlib import Path

from sensor_fault_detection.data import DatasetSchema, load_training_data
from sensor_fault_detection.model import build_model, train


ROOT = Path(__file__).parent
SCHEMA = ROOT / "fixtures/schema.yaml"
DATA = ROOT / "fixtures/aps_synthetic.csv"


def test_model_fits_only_training_data():
    schema = DatasetSchema.from_yaml(SCHEMA)
    features, target = load_training_data(DATA, schema)
    model = build_model(seed=42)
    model.fit(features.iloc[:16], target.iloc[:16])
    assert model.named_steps["imputer"].statistics_[0] < 2


def test_train_writes_reproducible_artifacts(tmp_path):
    result = train(DATA, SCHEMA, tmp_path / "run", seed=42)
    output = Path(result["output_dir"])
    assert (output / "model.joblib").exists()
    assert (output / "metrics.json").exists()
    assert (output / "confusion_matrix.csv").exists()
    assert result["metadata"]["test_rows"] == 4
