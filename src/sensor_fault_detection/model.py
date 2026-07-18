from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler

from .data import DatasetSchema, load_prediction_data, load_training_data, split_data


def build_model(seed: int) -> Pipeline:
    return Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", RobustScaler()),
            ("classifier", LogisticRegression(max_iter=2000, class_weight="balanced", random_state=seed)),
        ]
    )


def _metrics(y_true: pd.Series, y_pred: Any) -> dict[str, float | int]:
    matrix = confusion_matrix(y_true, y_pred, labels=[0, 1])
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "true_negatives": int(matrix[0, 0]),
        "false_positives": int(matrix[0, 1]),
        "false_negatives": int(matrix[1, 0]),
        "true_positives": int(matrix[1, 1]),
    }


def train(
    data_path: str | Path,
    schema_path: str | Path,
    output_dir: str | Path,
    *,
    seed: int = 42,
    test_size: float = 0.2,
) -> dict[str, Any]:
    schema = DatasetSchema.from_yaml(schema_path)
    features, target = load_training_data(data_path, schema)
    x_train, x_test, y_train, y_test = split_data(features, target, test_size=test_size, seed=seed)

    model = build_model(seed)
    model.fit(x_train, y_train)
    metrics = _metrics(y_test, model.predict(x_test))

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {"model": model, "feature_columns": list(schema.feature_columns), "labels": {"0": "neg", "1": "pos"}},
        output / "model.joblib",
    )
    (output / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
    with (output / "confusion_matrix.csv").open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerows([["", "pred_neg", "pred_pos"], ["actual_neg", metrics["true_negatives"], metrics["false_positives"]], ["actual_pos", metrics["false_negatives"], metrics["true_positives"]]])
    metadata = {
        "seed": seed,
        "test_size": test_size,
        "train_rows": len(x_train),
        "test_rows": len(x_test),
        "feature_count": len(schema.feature_columns),
        "data_path": str(data_path),
        "schema_path": str(schema_path),
        "model": "balanced logistic regression",
    }
    (output / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    return {"metrics": metrics, "output_dir": str(output), "metadata": metadata}


def predict(
    data_path: str | Path,
    model_path: str | Path,
    schema_path: str | Path,
    output_path: str | Path,
) -> pd.DataFrame:
    schema = DatasetSchema.from_yaml(schema_path)
    features = load_prediction_data(data_path, schema)
    artifact = joblib.load(model_path)
    expected = artifact.get("feature_columns", list(schema.feature_columns))
    if list(features.columns) != list(expected):
        raise ValueError("Prediction schema does not match the trained model")
    predictions = artifact["model"].predict(features)
    result = pd.read_csv(data_path)
    result["prediction"] = pd.Series(predictions, index=result.index).map({0: "neg", 1: "pos"})
    result.to_csv(output_path, index=False)
    return result
