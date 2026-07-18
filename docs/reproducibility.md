# Reproducibility

The baseline is deterministic when the same Python/dependency versions, input CSV, schema, seed, and test size are used.

```bash
python -m sensor_fault_detection train \
  --data /path/to/aps.csv \
  --schema configs/schema.yaml \
  --seed 42 \
  --test-size 0.2 \
  --output-dir outputs/aps-baseline
```

The command records the resolved paths and split settings in `metadata.json`. The preprocessor is fitted only on training rows; the holdout rows are transformed but never resampled or used for fitting.

For public claims, preserve the input checksum, Python version, package lock/update date, and generated metrics together with the release notes. Do not treat the archived artifacts from the abandoned implementation as validated benchmark results.
