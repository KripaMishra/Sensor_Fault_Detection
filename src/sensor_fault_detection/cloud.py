from __future__ import annotations

from pathlib import Path

from .settings import Settings


class S3ArtifactStore:
    """Optional S3-compatible artifact storage, including Cloudflare R2."""

    def __init__(self, settings: Settings) -> None:
        settings.validate_r2()
        try:
            import boto3
        except ImportError as exc:
            raise RuntimeError("Install the 'cloud' extra to use R2 artifact storage") from exc
        self.settings = settings
        client_kwargs = {
            "region_name": settings.aws_region,
            "endpoint_url": settings.s3_endpoint_url,
            "aws_access_key_id": settings.r2_access_key_id,
            "aws_secret_access_key": settings.r2_secret_access_key,
        }
        self.client = boto3.client("s3", **client_kwargs)

    def upload_directory(self, directory: str | Path, prefix: str | None = None) -> None:
        root = Path(directory)
        base = prefix or self.settings.s3_artifact_prefix
        for path in root.rglob("*"):
            if path.is_file():
                key = "/".join(part for part in [base, path.relative_to(root).as_posix()] if part)
                self.client.upload_file(str(path), self.settings.s3_bucket, key)
