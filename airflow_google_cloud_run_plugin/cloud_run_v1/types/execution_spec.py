from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Dict, Any

from airflow_google_cloud_run_plugin.cloud_run_v1.types.task_spec import TaskSpec
from airflow_google_cloud_run_plugin.cloud_run_v1.utils import SerializationMixin


@dataclass
class TaskTemplateSpec:
    """https://cloud.google.com/run/docs/reference/rest/v1/ExecutionSpec#TaskTemplateSpec"""

    spec: TaskSpec


@dataclass
class ExecutionSpec(SerializationMixin):
    """https://cloud.google.com/run/docs/reference/rest/v1/ExecutionSpec"""

    template: TaskTemplateSpec
    parallelism: Optional[int] = field(default=None)
    taskCount: Optional[int] = field(default=None)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> ExecutionSpec:
        return cls(
            template=TaskTemplateSpec(spec=TaskSpec.from_dict(d["template"]["spec"])),
            parallelism=d.get("parallelism"),
            taskCount=d.get("taskCount"),
        )
