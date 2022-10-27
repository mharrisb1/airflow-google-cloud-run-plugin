from typing import Any, Dict, List, Optional, Union, Sequence

from airflow.utils.context import Context

from airflow_google_cloud_run_plugin.hooks.cloud_run import CloudRunJobHook
from airflow_google_cloud_run_plugin.operators.cloud_run.base import (
    BaseCloudRunJobOperator,
)


class CloudRunCreateJobOperator(BaseCloudRunJobOperator):
    template_fields: Sequence[str] = (
        "project_id",
        "location",
        "name",
        "image",
        "command",
        "args",
        "labels",
    )

    def __init__(
        self,
        task_id: str,
        name: str,
        project_id: str,
        location: str,
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
        labels: Optional[Dict[str, str]] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(
            task_id=task_id,
            name=name,
            project_id=project_id,
            location=location,
            **kwargs
        )
        self.image = image
        self.cpu = cpu
        self.memory = memory
        self.command = command
        self.args = args
        self.env_vars = env_vars
        self.parallelism = parallelism
        self.task_count = task_count
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries or 0
        self.labels = labels

    def execute(self, context: Context) -> Dict[str, Any]:
        hook = CloudRunJobHook(project_id=self.project_id, region=self.location)
        job = hook.create_job(
            name=self.name,
            image=self.image,
            cpu=self.cpu,
            memory=self.memory,
            command=self.command,
            args=self.args,
            env_vars=self.env_vars,
            parallelism=self.parallelism,
            task_count=self.task_count,
            timeout_seconds=self.timeout_seconds,
            max_retries=self.max_retries,
            labels=self.labels,
        )
        return job.to_dict()


class CloudRunDeleteJobOperator(BaseCloudRunJobOperator):
    template_fields: Sequence[str] = (
        "project_id",
        "location",
        "name",
    )

    def __init__(
        self, task_id: str, name: str, project_id: str, location: str, **kwargs: Any
    ) -> None:
        super().__init__(
            task_id=task_id,
            name=name,
            project_id=project_id,
            location=location,
            **kwargs
        )

    def execute(self, context: Context) -> None:
        hook = CloudRunJobHook(project_id=self.project_id, region=self.location)
        hook.delete_job(self.name)
