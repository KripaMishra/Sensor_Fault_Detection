# Contributing

1. Create a virtual environment and install `pip install -e ".[dev]"`.
2. Run `ruff check src tests` and `pytest -q` before opening a pull request.
3. Keep changes small and focused; add a regression test for behavior changes.
4. Do not commit credentials, private datasets, generated outputs, or model artifacts.

Pull requests should explain the data/evaluation impact of model changes and avoid unsupported production claims.
