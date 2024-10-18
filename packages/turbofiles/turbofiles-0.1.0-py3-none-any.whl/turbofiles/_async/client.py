import aiohttp
import asyncio
import os
import mimetypes
from typing import Dict, Any, Optional, Union, BinaryIO
import logging
from aiohttp import ClientError

from ..version import __version__
from ..exceptions import (
    ClientException,
    CompressionFailedException,
    MaxRetriesExceededException,
)


class AsyncClient:
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
            "User-Agent": f"TurboFilesAsyncClient/{__version__}",
        }
        self.logger = logging.getLogger(__name__)

    async def _req(
        self, method: str, endpoint: str, json: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        url = f"{self.BASE_URL}{endpoint}"
        for attempt in range(self.MAX_RETRIES):
            try:
                async with aiohttp.ClientSession(headers=self.headers) as session:
                    async with session.request(method, url, json=json) as resp:
                        resp.raise_for_status()
                        return await resp.json()
            except ClientError as e:
                self.logger.warning(
                    f"Request failed (attempt {attempt + 1}/{self.MAX_RETRIES}): {str(e)}"
                )
                if attempt == self.MAX_RETRIES - 1:
                    raise ClientException(
                        f"Request failed after {self.MAX_RETRIES} attempts: {str(e)}"
                    )
                await asyncio.sleep(
                    self.RETRY_DELAY * (2**attempt)
                )  # exponential backoff

    async def get_upload_url(self, mime: str, size: int) -> Dict[str, Any]:
        data = {
            "data": {"type": "files", "attributes": {"mime_type": mime, "size": size}}
        }
        return await self._req("POST", "/files", json=data)

    async def upload(self, url: str, file: Union[str, BinaryIO], mime: str = None):
        if isinstance(file, str):
            file_path = file
            file_size = os.path.getsize(file_path)
            if mime is None:
                mime, _ = mimetypes.guess_type(file_path)
            with open(file_path, "rb") as f:
                return await self._upload(url, f, file_size, mime)
        else:
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
            return await self._upload(url, file, file_size, mime)

    async def _upload(self, url: str, file: BinaryIO, file_size: int, mime: str):
        headers = {"Content-Type": mime}
        async with aiohttp.ClientSession() as session:
            async with session.put(url, data=file, headers=headers) as resp:
                resp.raise_for_status()
                return await resp.text()

    async def create_task(
        self, file_id: str, action: str = "compress", parameters: Dict[str, Any] = {}
    ) -> Dict[str, Any]:
        data = {
            "data": {
                "type": "tasks",
                "attributes": {"action": action, "parameters": parameters},
                "relationships": {"source": {"data": {"type": "files", "id": file_id}}},
            }
        }
        return await self._req("POST", "/tasks", json=data)

    async def get_status(self, task_id: str) -> Dict[str, Any]:
        return await self._req("GET", f"/tasks/{task_id}")

    async def compress(
        self,
        file: Union[str, BinaryIO],
        parameters: Dict[str, Any] = {},
        mime: str = None,
        max_tries: int = 10,
        delay: float = 2.0,
    ) -> str:
        if isinstance(file, str):
            file_size = os.path.getsize(file)
            if mime is None:
                mime, _ = mimetypes.guess_type(file)
        else:
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)

        if mime is None:
            raise ValueError("Mime type could not be determined and was not provided")

        # Step 1: Get upload URL
        upload_resp = await self.get_upload_url(mime, file_size)
        file_id = upload_resp["data"]["id"]
        upload_url = upload_resp["data"]["links"]["upload"]

        # Step 2: Upload file
        await self.upload(upload_url, file, mime)

        # Step 3: Create compression task
        task_resp = await self.create_task(file_id, "compress", parameters)
        task_id = task_resp["data"]["id"]

        # Step 4: Check task status
        for _ in range(max_tries):
            status_resp = await self.get_status(task_id)
            status = status_resp["data"]["attributes"]["status"]
            if status == "COMPLETED":
                return status_resp["data"]["links"]["download"]
            elif status == "FAILED":
                raise CompressionFailedException("Compression task failed")
            await asyncio.sleep(delay)

        raise MaxRetriesExceededException(
            "Max retries reached while waiting for task completion"
        )
