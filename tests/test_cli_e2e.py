from pathlib import Path

import pandas as pd

from sensor_fault_detection.model import predict, train


ROOT = Path(__file__).parent
SCHEMA = ROOT / "fixtures/schema.yaml"
DATA = ROOT / "fixtures/aps_synthetic.csv"


def test_train_predict_workflow(tmp_path):
    run_dir = tmp_path / "run"
    train(DATA, SCHEMA, run_dir, seed=42)
    prediction_input = tmp_path / "prediction.csv"
    pd.read_csv(DATA).drop(columns=["class"]).head(4).to_csv(prediction_input, index=False)

    output = tmp_path / "predictions.csv"
    result = predict(prediction_input, run_dir / "model.joblib", SCHEMA, output)

    assert len(result) == 4
    assert set(result["prediction"]) <= {"neg", "pos"}
    assert len(pd.read_csv(output)) == 4
