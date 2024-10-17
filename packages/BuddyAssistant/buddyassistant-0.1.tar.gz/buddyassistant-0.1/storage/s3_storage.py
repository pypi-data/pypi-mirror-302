import json
from typing import Any, Dict

import boto3

from storage.base_storage import BaseStorage


class S3Storage(BaseStorage):
    def __init__(self, bucket_name: str):
        self.s3 = boto3.client("s3")
        self.bucket_name = bucket_name

    def save_assistant(self, assistant_id: str, data: Dict[str, Any]) -> None:
        s3_key = f"assistants/{assistant_id}.json"
        self.s3.put_object(Bucket=self.bucket_name, Key=s3_key, Body=json.dumps(data))

    def load_assistant(self, assistant_id: str) -> Dict[str, Any]:
        s3_key = f"assistants/{assistant_id}.json"
        response = self.s3.get_object(Bucket=self.bucket_name, Key=s3_key)
        return json.loads(response["Body"].read())

    def save_thread(self, thread_id: str, data: Dict[str, Any]) -> None:
        s3_key = f"threads/{thread_id}.json"
        self.s3.put_object(Bucket=self.bucket_name, Key=s3_key, Body=json.dumps(data))

    def load_thread(self, thread_id: str) -> Dict[str, Any]:
        s3_key = f"threads/{thread_id}.json"
        response = self.s3.get_object(Bucket=self.bucket_name, Key=s3_key)
        return json.loads(response["Body"].read())
