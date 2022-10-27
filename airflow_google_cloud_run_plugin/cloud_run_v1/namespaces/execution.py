from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

from airflow_google_cloud_run_plugin.cloud_run_v1.types import (
    Condition,
    ObjectMeta,
    ExecutionSpec,
)
from airflow_google_cloud_run_plugin.cloud_run_v1.utils import SerializationMixin


@dataclass
class ExecutionStatus(SerializationMixin):
    """https://cloud.google.com/run/docs/reference/rest/v1/namespaces.executions#ExecutionStatus"""

    observedGeneration: Optional[int] = field(default=None)
    conditions: List[Condition] = field(default_factory=list)
    startTime: Optional[str] = field(default=None)
    completionTime: Optional[str] = field(default=None)
    runningCount: Optional[int] = field(default=None)
    succeededCount: Optional[int] = field(default=None)
    failedCount: Optional[int] = field(default=None)
    cancelledCount: Optional[int] = field(default=None)
    retriedCount: Optional[int] = field(default=None)
    logUri: Optional[str] = field(default=None)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> ExecutionStatus:
        return cls(
            observedGeneration=d.get("observedGeneration"),
            conditions=[Condition(**i) for i in d.get("conditions", [])],
            startTime=d.get("startTime"),
            completionTime=d.get("completionTime"),
            runningCount=d.get("runningCount"),
            succeededCount=d.get("succeededCount"),
            failedCount=d.get("failedCount"),
            cancelledCount=d.get("cancelledCount"),
            retriedCount=d.get("retriedCount"),
            logUri=d.get("logUri"),
        )


@dataclass
class Execution(SerializationMixin):
    """https://cloud.google.com/run/docs/reference/rest/v1/namespaces.executions"""

    metadata: ObjectMeta
    spec: ExecutionSpec
    status: Optional[ExecutionStatus] = field(default=None)
    apiVersion: Optional[str] = field(default=None)
    kind: Optional[str] = field(default=None)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Execution:
        return cls(
            metadata=ObjectMeta.from_dict(d["metadata"]),
            spec=ExecutionSpec.from_dict(d["spec"]),
            status=ExecutionStatus.from_dict(d.get("status", {})),
        )

    def get_status(self) -> str:
        try:
            cond = next(c for c in self.status.conditions if c.type == "Completed")
            return cond.status
        except StopIteration:
            return "Unknown"
