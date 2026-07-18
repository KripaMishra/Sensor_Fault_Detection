from __future__ import annotations

import tempfile
from pathlib import Path
from threading import Lock

from .full_pipeline import run_training
from .model import predict
from .settings import Settings


_training_lock = Lock()


def create_app(settings: Settings | None = None):
    try:
        from fastapi import FastAPI, File, HTTPException, UploadFile
        from fastapi.middleware.cors import CORSMiddleware
        from fastapi.responses import Response
    except ImportError as exc:
        raise RuntimeError("Install the 'api' extra to run the HTTP service") from exc

    settings = settings or Settings.from_env()
    app = FastAPI(title="Sensor Fault Detection", version="1.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_origins),
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health() -> dict[str, object]:
        return {"status": "ok", "source": settings.source}

    @app.post("/train")
    def train_route() -> dict[str, str]:
        if not _training_lock.acquire(blocking=False):
            raise HTTPException(status_code=409, detail="Training is already running")
        try:
            result = run_training(settings)
            return {"status": "completed", "run_dir": str(result.run_dir)}
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc
        finally:
            _training_lock.release()

    @app.post("/predict")
    async def predict_route(file: UploadFile = File(...)):
        if file.content_type not in {"text/csv", "application/csv", "application/octet-stream"}:
            raise HTTPException(status_code=415, detail="Upload a CSV file")
        contents = await file.read(settings.max_upload_bytes + 1)
        if len(contents) > settings.max_upload_bytes:
            raise HTTPException(status_code=413, detail="CSV exceeds upload size limit")
        model_path = settings.model_root / "latest" / "model.joblib"
        if not model_path.exists():
            raise HTTPException(status_code=404, detail="No promoted model is available")

        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "input.csv"
            output_path = Path(directory) / "predictions.csv"
            input_path.write_bytes(contents)
            try:
                predict(input_path, model_path, settings.schema_path, output_path)
            except Exception as exc:
                raise HTTPException(status_code=400, detail=str(exc)) from exc
            return Response(
                content=output_path.read_bytes(),
                media_type="text/csv",
                headers={"Content-Disposition": 'attachment; filename="predictions.csv"'},
            )

    return app
