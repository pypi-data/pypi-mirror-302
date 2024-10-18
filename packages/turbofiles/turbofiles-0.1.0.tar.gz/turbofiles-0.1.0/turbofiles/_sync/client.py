import http.client
import json
import time
import os
from urllib.parse import urlparse
import ssl
from typing import Dict, Any, Optional, Union, BinaryIO
import mimetypes
import logging
from contextlib import contextmanager
import urllib.parse

from ..version import __version__
from ..exceptions import (
    ClientException,
    CompressionFailedException,
    MaxRetriesExceededException,
)


class SyncClient:
    BASE_URL = "https://api.turbofiles.io/v1"
    MAX_RETRIES = 3
    RETRY_DELAY = 1

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("TURBOFILES_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided or set in TURBOFILES_API_KEY environment variable"
            )

        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/vnd.api+json",
            "User-Agent": f"TurboFilesSyncClient/{__version__}",
        }
        self.logger = logging.getLogger(__name__)
        self.http_client = http.client.HTTPSConnection

    @contextmanager
    def _http_connection(self, url: str, timeout: int = 10):
        parsed_url = urlparse(url)
        context = ssl.create_default_context()
        conn = self.http_client(parsed_url.netloc, context=context, timeout=timeout)
        try:
            yield conn
        finally:
            conn.close()

    def _req(
        self, method: str, endpoint: str, body: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        url = f"{self.BASE_URL}{endpoint}"
        for attempt in range(self.MAX_RETRIES):
            try:
                with self._http_connection(url) as conn:
                    conn.request(
                        method,
                        urlparse(url).path,
                        body=json.dumps(body) if body else None,
                        headers=self.headers,
                    )
                    response = conn.getresponse()
                    if response.status >= 400:
                        raise ClientException(
                            f"HTTP Error {response.status}: {response.reason}"
                        )
                    return json.loads(response.read().decode())
            except (http.client.HTTPException, ssl.SSLError) as e:
                self.logger.warning(
                    f"Request failed (attempt {attempt + 1}/{self.MAX_RETRIES}): {str(e)}"
                )
                if attempt == self.MAX_RETRIES - 1:
                    raise
                time.sleep(self.RETRY_DELAY * (2**attempt))  # exponential backoff

    def get_upload_url(self, mime: str, size: int) -> Dict[str, Any]:
        data = {
            "data": {"type": "files", "attributes": {"mime_type": mime, "size": size}}
        }
        return self._req("POST", "/files", body=data)

    def upload(self, url: str, file: Union[str, BinaryIO], mime: str = None):
        if isinstance(file, str):
            file_path = file
            size = os.path.getsize(file_path)
            if mime is None:
                mime, _ = mimetypes.guess_type(file_path)
            with open(file_path, "rb") as f:
                return self._upload(url, f, size, mime)
        else:
            file.seek(0, os.SEEK_END)
            size = file.tell()
            file.seek(0)
            return self._upload(url, file, size, mime)

    def _upload(self, url: str, file: BinaryIO, size: int, mime: str):
        parsed_url = urllib.parse.urlparse(url)
        headers = {
            "Content-Type": mime,
            "Content-Length": str(size),
        }
        with self._http_connection(url, timeout=30) as conn:
            conn.request(
                "PUT",
                f"{parsed_url.path}?{parsed_url.query}",
                body=file,
                headers=headers,
            )
            response = conn.getresponse()
            if response.status >= 400:
                raise ClientException(
                    f"Upload failed: HTTP Error {response.status}: {response.reason}"
                )
            return response.read().decode()

    def create_task(
        self, file_id: str, action: str = "compress", parameters: Dict[str, Any] = {}
    ) -> Dict[str, Any]:
        data = {
            "data": {
                "type": "tasks",
                "attributes": {"action": action, "parameters": parameters},
                "relationships": {"source": {"data": {"type": "files", "id": file_id}}},
            }
        }
        return self._req("POST", "/tasks", body=data)

    def get_status(self, task_id: str) -> Dict[str, Any]:
        return self._req("GET", f"/tasks/{task_id}")

    def compress(
        self,
        file: Union[str, BinaryIO],
        parameters: Dict[str, Any] = {},
        mime: str = None,
        max_tries: int = 10,
        delay: int = 2,
    ) -> str:
        if isinstance(file, str):
            size = os.path.getsize(file)
            if mime is None:
                mime, _ = mimetypes.guess_type(file)
        else:
            file.seek(0, os.SEEK_END)
            size = file.tell()
            file.seek(0)

        if mime is None:
            raise ValueError("Mime type could not be determined and was not provided")

        upload_resp = self.get_upload_url(mime, size)
        file_id = upload_resp["data"]["id"]
        upload_url = upload_resp["data"]["links"]["upload"]

        self.upload(upload_url, file, mime)

        task_resp = self.create_task(file_id, "compress", parameters)
        task_id = task_resp["data"]["id"]

        for _ in range(max_tries):
            status_resp = self.get_status(task_id)
            status = status_resp["data"]["attributes"]["status"]
            if status == "COMPLETED":
                return status_resp["data"]["links"]["download"]
            elif status == "FAILED":
                raise CompressionFailedException("Compression task failed")
            time.sleep(delay)

        raise MaxRetriesExceededException(
            "Max retries reached while waiting for task completion"
        )
