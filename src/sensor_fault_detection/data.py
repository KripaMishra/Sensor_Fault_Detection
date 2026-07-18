from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import yaml
from sklearn.model_selection import train_test_split


@dataclass(frozen=True)
class DatasetSchema:
    target_column: str
    feature_columns: tuple[str, ...]
    drop_columns: tuple[str, ...] = ()

    @classmethod
    def from_yaml(cls, path: str | Path) -> "DatasetSchema":
        raw: dict[str, Any] = yaml.safe_load(Path(path).read_text()) or {}
        target = raw.get("target_column", "class")
        features = raw.get("feature_columns") or raw.get("numerical_columns")
        if not features:
            features = [name for item in raw.get("columns", []) for name in item if name != target]
        if not features:
            raise ValueError(f"Schema {path} does not define feature columns")
        return cls(target, tuple(features), tuple(raw.get("drop_columns", [])))


def read_csv(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path, na_values=["?", "NA", "N/A", "null"])


def validate_dataframe(
    dataframe: pd.DataFrame,
    schema: DatasetSchema,
    *,
    require_target: bool,
) -> pd.DataFrame:
    required = set(schema.feature_columns)
    if require_target:
        required.add(schema.target_column)
    missing = sorted(required - set(dataframe.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    allowed = required | set(schema.drop_columns)
    unexpected = sorted(set(dataframe.columns) - allowed)
    if unexpected:
        raise ValueError(f"Unexpected columns: {', '.join(unexpected)}")

    cleaned = dataframe.drop(columns=list(schema.drop_columns), errors="ignore").copy()
    for column in schema.feature_columns:
        original = cleaned[column]
        converted = pd.to_numeric(original, errors="coerce")
        invalid = original.notna() & converted.isna()
        if invalid.any():
            raise ValueError(f"Feature '{column}' contains non-numeric values")
        cleaned[column] = converted
    return cleaned


def load_training_data(path: str | Path, schema: DatasetSchema) -> tuple[pd.DataFrame, pd.Series]:
    dataframe = validate_dataframe(read_csv(path), schema, require_target=True)
    labels = dataframe.pop(schema.target_column).astype(str).str.strip().str.lower()
    mapping = {"neg": 0, "0": 0, "pos": 1, "1": 1}
    unknown = sorted(set(labels) - set(mapping))
    if unknown:
        raise ValueError(f"Unsupported labels in {schema.target_column}: {', '.join(unknown)}")
    target = labels.map(mapping).astype("int64")
    if target.nunique() != 2:
        raise ValueError("Training data must contain both neg and pos classes")
    return dataframe[list(schema.feature_columns)], target


def load_prediction_data(path: str | Path, schema: DatasetSchema) -> pd.DataFrame:
    dataframe = validate_dataframe(read_csv(path), schema, require_target=False)
    return dataframe[list(schema.feature_columns)]


def split_data(
    features: pd.DataFrame,
    target: pd.Series,
    *,
    test_size: float,
    seed: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    return train_test_split(
        features,
        target,
        test_size=test_size,
        random_state=seed,
        stratify=target,
    )
