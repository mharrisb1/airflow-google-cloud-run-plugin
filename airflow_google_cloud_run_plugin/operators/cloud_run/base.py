from typing import Any, Dict

from airflow.models import BaseOperator
from airflow.utils.context import Context


class BaseCloudRunJobOperator(BaseOperator):
    def __init__(
        self, task_id: str, name: str, project_id: str, location: str, **kwargs: Any
    ) -> None:
        """
        :param task_id: Task ID
        :param name: Job name
        :param project_id: Google Cloud project ID or project number
        :param location: Google Cloud region
        """
        super().__init__(task_id=task_id, **kwargs)
        self.name = name
        self.project_id = project_id
        self.location = location

    def execute(self, context: Context) -> Dict[str, Any]:
        raise NotImplementedError
