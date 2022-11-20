import time
from typing import Any, Dict, List, Optional, Union, Sequence

import requests
from airflow.utils.context import Context

from airflow_google_cloud_run_plugin.hooks.cloud_run import CloudRunJobHook
from airflow_google_cloud_run_plugin.exceptions import CloudRunJobExecutionError
from airflow_google_cloud_run_plugin.cloud_run_v1.namespaces import Execution
from airflow_google_cloud_run_plugin.operators.cloud_run.base import (
    BaseCloudRunJobOperator,
)


class CloudRunJobOperator(BaseCloudRunJobOperator):
    template_fields: Sequence[str] = (
        "project_id",
        "location",
        "name",
        "image",
        "command",
        "args",
        "labels",
    )
    template_ext: Sequence[str] = (".sql", ".json")

    def __init__(
        self,
        task_id: str,
        name: str,
        project_id: str,
        location: str,
        image: Optional[str] = None,
        create_if_not_exists: bool = True,
        delete_on_exit: bool = True,
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
        self.create_if_not_exists = create_if_not_exists
        self.delete_on_exit = delete_on_exit
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

    def _wait_for_execution_completion(
        self, hook: CloudRunJobHook, execution: Execution
    ) -> Execution:
        execution_name = execution.metadata.name
        status = "Unknown"
        while status == "Unknown":
            execution = hook.get_execution(execution_name)
            self.log.info("Checking execution status")
            self.log.info(execution.to_dict())
            status = execution.get_status()
            # Avoid too many calls error
            time.sleep(18)

        return execution

    def execute(self, context: Context) -> Dict[str, Any]:
        hook = CloudRunJobHook(project_id=self.project_id, region=self.location)
        if self.create_if_not_exists and not self.image:
            raise CloudRunJobExecutionError("Image must be set if creating new job.")
        # Handle in case job already exists. Expect exception.
        try:
            job = hook.get_job(self.name)
        except requests.HTTPError:
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

        # Even though the job exists, sometimes the run will fail with "JOB NOT FOUND ERROR".
        # Add padding to help prevent that.
        time.sleep(5)

        execution = hook.run_job(job.metadata.name)
        execution = self._wait_for_execution_completion(hook, execution)

        if self.delete_on_exit:
            hook.delete_job(job.metadata.name)

        if execution.get_status() == "True":
            return execution.to_dict()

        raise CloudRunJobExecutionError("Job execution did not complete successfully.")
