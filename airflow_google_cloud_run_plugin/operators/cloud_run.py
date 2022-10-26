import time
from typing import Any, Dict, List, Optional, Union, Sequence

from airflow.models import BaseOperator

from airflow_google_cloud_run_plugin.hooks.cloud_run import CloudRunJobHook
from airflow_google_cloud_run_plugin.exceptions import CloudRunJobExecutionError


class CloudRunJobCreateOperator(BaseOperator):
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
        project_id: str,
        location: str,
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
        labels: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> None:
        super().__init__(task_id=task_id, **kwargs)
        self.project_id = project_id
        self.location = location
        self.name = name
        self.image = image
        self.cpu = cpu
        self.memory = memory
        self.command = command
        self.args = args
        self.env_vars = env_vars
        self.parallelism = parallelism
        self.task_count = task_count
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.labels = labels

    def execute(self, context: Any) -> Dict[str, Any]:
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


class CloudRunJobDeleteOperator(BaseOperator):
    template_fields: Sequence[str] = (
        "project_id",
        "location",
        "name",
    )

    def __init__(
        self, task_id: str, project_id: str, location: str, name: str, **kwargs
    ) -> None:
        super().__init__(task_id=task_id, **kwargs)
        self.project_id = project_id
        self.location = location
        self.name = name

    def execute(self, context: Any) -> None:
        hook = CloudRunJobHook(project_id=self.project_id, region=self.location)
        hook.delete_job(self.name)


class CloudRunJobRunOperator(BaseOperator):
    template_fields: Sequence[str] = (
        "project_id",
        "location",
        "name",
    )

    def __init__(
        self,
        task_id: str,
        project_id: str,
        location: str,
        name: str,
        wait_for_execution: bool = True,
        **kwargs
    ) -> None:
        super().__init__(task_id, **kwargs)
        self.project_id = project_id
        self.location = location
        self.name = name

        # TODO - once sensor is added this needs to be adhered to
        self.wait_for_execution = wait_for_execution

    def execute(self, context: Any) -> Dict[str, Any]:
        hook = CloudRunJobHook(project_id=self.project_id, region=self.location)
        if not self.wait_for_execution:
            raise NotImplementedError
        execution = hook.run_job(self.name)
        execution_name = execution.metadata.name
        status = "Unknown"
        while status == "Unknown":
            execution = hook.get_execution(execution_name)
            self.log.info("Checking execution status")
            self.log.info(execution.to_dict())
            try:
                condition = next(
                    c for c in execution.status.conditions if c.type == "Completed"
                )
                status = condition.status
            except StopIteration:
                status = "Unknown"
            time.sleep(3)

        if status == "True":
            return execution.to_dict()
        elif status == "False":
            raise CloudRunJobExecutionError(
                "Job execution did not complete successfully. Please check logs."
            )
