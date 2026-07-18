FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
COPY configs ./configs

RUN pip install --no-cache-dir ".[api]"

EXPOSE 8080
CMD ["uvicorn", "sensor_fault_detection.api:create_app", "--factory", "--host", "0.0.0.0", "--port", "8080"]
