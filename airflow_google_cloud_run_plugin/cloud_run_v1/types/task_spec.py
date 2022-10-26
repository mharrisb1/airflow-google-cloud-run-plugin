from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

from airflow_google_cloud_run_plugin.cloud_run_v1.types.container import Container
from airflow_google_cloud_run_plugin.cloud_run_v1.utils import SerializationMixin


@dataclass
class TaskSpec(SerializationMixin):
    """https://cloud.google.com/run/docs/reference/rest/v1/TaskSpec"""

    # TODO - volumes
    containers: List[Container]
    timeoutSeconds: Optional[str] = field(default=None)
    serviceAccountName: Optional[str] = field(default=None)
    maxRetries: Optional[int] = field(default=None)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> TaskSpec:
        return cls(
            containers=[Container.from_dict(i) for i in d["containers"]],
            timeoutSeconds=d.get("timeoutSeconds"),
            serviceAccountName=d.get("serviceAccountName"),
            maxRetries=d.get("maxRetries"),
        )
