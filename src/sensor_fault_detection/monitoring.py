from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import yaml
from scipy.stats import ks_2samp


def detect_dataset_drift(
    baseline: pd.DataFrame,
    current: pd.DataFrame,
    *,
    threshold: float = 0.05,
) -> dict[str, Any]:
    columns: dict[str, dict[str, float | bool]] = {}
    drifted = False
    for column in baseline.columns:
        left = pd.to_numeric(baseline[column], errors="coerce").dropna()
        right = pd.to_numeric(current[column], errors="coerce").dropna()
        if left.empty or right.empty:
            p_value = 1.0
        else:
            p_value = float(ks_2samp(left, right).pvalue)
        is_drifted = p_value < threshold
        drifted = drifted or is_drifted
        columns[column] = {"p_value": p_value, "drifted": is_drifted}
    return {"threshold": threshold, "drifted": drifted, "columns": columns}


def write_drift_report(path: str | Path, report: dict[str, Any]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(yaml.safe_dump(report, sort_keys=False))
