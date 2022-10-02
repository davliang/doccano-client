from __future__ import annotations

import pathlib
from typing import List

from requests_toolbelt import MultipartEncoder

from doccano_client.client import DoccanoClient
from doccano_client.models.data_import import AvailableTask, Option


class DataImportClient:
    """Client for interacting with the Doccano data import API"""

    def __init__(self, client: DoccanoClient):
        self._client = client

    def list_options(self, project_id: int) -> List[Option]:
        """Return all upload options

        Args:
            project_id (int): The id of the project

        Returns:
            List[Option]: The list of the upload options.
        """
        resource = f"projects/{project_id}/catalog"
        response = self._client.get(resource)
        options = [Option.parse_obj(label) for label in response.json()]
        return options

    def upload(self, file_path: str) -> str:
        """Upload a file to the server

        Args:
            file_path (str): The path to the file to upload

        Returns:
            str: The id of the uploaded file
        """
        resource = "fp/process/"
        path = pathlib.Path(file_path)
        with path.open("rb") as f:
            m = MultipartEncoder(fields={"filepond": (path.name, f)})
            headers = {"Content-Type": m.content_type, "Accept": "*/*"}
            response = self._client.post(resource, data=m, headers=headers)
            return response.content.decode()

    def delete(self, upload_id: str):
        """Delete the uploaded file from the server

        Args:
            upload_id (str): The id of the uploaded file
        """
        resource = "fp/revert/"
        headers = {"Content-Type": "text/plain", "Accept": "*/*"}
        self._client.delete(resource, data=upload_id, headers=headers)

    def ingest(self, project_id: int, upload_ids: List[str], task: AvailableTask, format: str) -> int:
        """Ingest the uploaded files into the project

        Args:
            project_id (int): The id of the project
            upload_ids (List[str]): The ids of the uploaded files
            task (AvailableTask): The project's task name
            format (str): The format of the uploaded files

        Returns:
            int: The celery task id
        """
        resource = f"projects/{project_id}/upload"
        data = {"uploadIds": upload_ids, "task": task, "format": format}
        response = self._client.post(resource, json=data)
        return response.json()["task_id"]
