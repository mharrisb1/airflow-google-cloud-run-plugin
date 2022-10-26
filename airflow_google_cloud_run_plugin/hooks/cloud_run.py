from typing import Any, Dict, List, Optional, Union

from airflow.hooks.base import BaseHook

from airflow_google_cloud_run_plugin.cloud_run_v1.client import CloudRunJobClient
from airflow_google_cloud_run_plugin.cloud_run_v1.namespaces import Job, Execution

__all__ = ["CloudRunJobHook"]


class CloudRunJobHook(BaseHook):
    def __init__(self, project_id: str, region: str, context: Any = None) -> None:
        super().__init__(context)
        self.project_id = project_id
        self.region = region
        self._client: Optional[CloudRunJobClient] = None

    def get_conn(self) -> CloudRunJobClient:
        self._client = CloudRunJobClient(project_id=self.project_id, region=self.region)
        return self._client

    def create_job(
        self,
        *,
        name: str,
        image: str,
        cpu: Union[str, int, float] = "1000m",
        memory: str = "512Mi",
        command: Optional[List[str]] = None,
        args: Optional[List[str]] = None,
        env_vars: Optional[List[Dict[str, str]]] = None,
        parallelism: Optional[int] = None,
        task_count: Optional[int] = None,
        timeout_seconds: Optional[str] = None,
        max_retries: Optional[int] = None,
        labels: Optional[Dict[str, str]] = None
    ) -> Job:
        job = Job.from_dict(
            {
                "metadata": {
                    "name": name,
                    "namespace": self.project_id,
                    "annotations": {"run.googleapis.com/launch-stage": "BETA"},
                    "labels": labels,
                },
                "spec": {
                    "template": {
                        "spec": {
                            "template": {
                                "spec": {
                                    "containers": [
                                        {
                                            "image": image,
                                            "resources": {
                                                "limits": {"cpu": cpu, "memory": memory}
                                            },
                                            "command": command or [],
                                            "args": args or [],
                                            "env": env_vars or [],
                                        }
                                    ],
                                    "timeoutSeconds": timeout_seconds,
                                    "maxRetries": max_retries,
                                }
                            }
                        },
                        "parallelism": parallelism,
                        "taskCount": task_count,
                    }
                },
                "kind": "Job",
                "apiVersion": "run.googleapis.com/v1",
            }
        )
        client = self.get_conn()
        job = client.create_job(job)
        client.close()
        return job

    def delete_job(self, name: str) -> None:
        client = self.get_conn()
        client.delete_job(name)
        client.close()

    def get_job(self, name: str) -> Job:
        client = self.get_conn()
        job = client.get_job(name)
        client.close()
        return job

    def run_job(self, name: str) -> Execution:
        client = self.get_conn()
        execution = client.run_job(name)
        client.close()
        return execution

    def get_execution(self, name: str) -> Execution:
        client = self.get_conn()
        execution = client.get_execution(name)
        client.close()
        return execution
