from __future__ import annotations

from pathlib import Path

from .settings import Settings


class S3ArtifactStore:
    """Optional S3 artifact storage using boto3's credential chain."""

    def __init__(self, settings: Settings) -> None:
        if not settings.s3_bucket:
            raise ValueError("SFD_S3_BUCKET is required for S3 artifact storage")
        try:
            import boto3
        except ImportError as exc:
            raise RuntimeError("Install the 'cloud' extra to use S3 artifact storage") from exc
        self.settings = settings
        self.client = boto3.client("s3", region_name=settings.aws_region)

    def upload_directory(self, directory: str | Path, prefix: str | None = None) -> None:
        root = Path(directory)
        base = prefix or self.settings.s3_artifact_prefix
        for path in root.rglob("*"):
            if path.is_file():
                key = "/".join(part for part in [base, path.relative_to(root).as_posix()] if part)
                self.client.upload_file(str(path), self.settings.s3_bucket, key)
