FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
COPY configs ./configs

RUN pip install --no-cache-dir ".[full]"

ENV SFD_API_HOST=0.0.0.0 SFD_API_PORT=8080
VOLUME ["/app/models", "/app/artifacts"]
EXPOSE 8080
CMD ["sh", "-c", "exec uvicorn sensor_fault_detection.api:create_app --factory --host \"$SFD_API_HOST\" --port \"$SFD_API_PORT\""]
