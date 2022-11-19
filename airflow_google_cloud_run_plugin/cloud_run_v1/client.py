from typing import List

import requests
from requests.adapters import HTTPAdapter, Retry

import google.auth
import google.auth.transport.requests

from airflow_google_cloud_run_plugin.cloud_run_v1.namespaces import Job, Execution


class CloudRunJobClient:
    def __init__(self, project_id: str, region: str) -> None:
        regional_endpoint = f"https://{region}-run.googleapis.com"
        self.endpoint = f"{regional_endpoint}/apis/run.googleapis.com/v1/namespaces/{project_id}/jobs"
        self.executions_endpoint = f"{regional_endpoint}/apis/run.googleapis.com/v1/namespaces/{project_id}/executions"
        credentials, project = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        auth_req = google.auth.transport.requests.Request()
        credentials.refresh(auth_req)
        self._session = requests.Session()
        self._session.mount("https://", HTTPAdapter(max_retries=Retry(total=5, backoff_factor=2)))
        self._session.headers.update({"Content-Type": "application/json"})
        self._session.headers.update({"Authorization": f"Bearer {credentials.token}"})

    def close(self) -> None:
        self._session.close()

    def list_jobs(self) -> List[Job]:
        res = self._session.get(url=self.endpoint)
        res.raise_for_status()
        return [Job.from_dict(d) for d in res.json()["items"]]

    def create_job(self, job: Job) -> Job:
        res = self._session.post(url=self.endpoint, json=job.to_dict())
        res.raise_for_status()
        return Job.from_dict(res.json())

    def delete_job(self, name: str) -> None:
        res = self._session.delete(url=self.endpoint + "/" + name)
        res.raise_for_status()

    def get_job(self, name: str) -> Job:
        res = self._session.get(url=self.endpoint + "/" + name)
        res.raise_for_status()
        return Job.from_dict(res.json())

    # TODO - replace job

    def run_job(self, name: str) -> Execution:
        res = self._session.post(url=self.endpoint + "/" + name + ":run")
        res.raise_for_status()
        return Execution.from_dict(res.json())

    # TODO - list executions

    def get_execution(self, name: str) -> Execution:
        res = self._session.get(url=self.executions_endpoint + "/" + name)
        res.raise_for_status()
        return Execution.from_dict(res.json())

    # TODO - delete executions
