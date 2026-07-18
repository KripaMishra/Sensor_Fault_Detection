from __future__ import annotations

import pandas as pd

from .settings import Settings


class MongoDataSource:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def read(self) -> pd.DataFrame:
        try:
            from pymongo import MongoClient
        except ImportError as exc:
            raise RuntimeError("Install the 'mongo' extra to use the MongoDB source") from exc

        with MongoClient(self.settings.mongo_db_url, serverSelectionTimeoutMS=5000) as client:
            client.admin.command("ping")
            records = list(
                client[self.settings.mongo_database][self.settings.mongo_collection].find({})
            )
        frame = pd.DataFrame(records)
        return frame.drop(columns=["_id"], errors="ignore").replace({"na": pd.NA})


class S3CsvDataSource:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def read(self) -> pd.DataFrame:
        if not self.settings.s3_bucket or not self.settings.s3_data_key:
            raise ValueError("SFD_S3_BUCKET and SFD_S3_DATA_KEY are required for the S3 source")
        try:
            import boto3
        except ImportError as exc:
            raise RuntimeError("Install the 'cloud' extra to use the S3 source") from exc

        body = boto3.client("s3", region_name=self.settings.aws_region).get_object(
            Bucket=self.settings.s3_bucket, Key=self.settings.s3_data_key
        )["Body"]
        return pd.read_csv(body, na_values=["?", "NA", "N/A", "null"])


def load_source(settings: Settings) -> pd.DataFrame:
    if settings.source == "local":
        return pd.read_csv(settings.data_path, na_values=["?", "NA", "N/A", "null"])
    if settings.source == "mongo":
        return MongoDataSource(settings).read()
    if settings.source == "s3":
        return S3CsvDataSource(settings).read()
    raise ValueError(f"Unsupported SFD_SOURCE: {settings.source}")
