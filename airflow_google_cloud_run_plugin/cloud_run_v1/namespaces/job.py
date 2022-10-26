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
class ExecutionTemplateSpec:
    """https://cloud.google.com/run/docs/reference/rest/v1/namespaces.jobs#ExecutionTemplateSpec"""

    spec: ExecutionSpec


@dataclass
class JobSpec:
    """https://cloud.google.com/run/docs/reference/rest/v1/namespaces.jobs#JobSpec"""

    template: ExecutionTemplateSpec


@dataclass
class ExecutionReference:
    """https://cloud.google.com/run/docs/reference/rest/v1/namespaces.jobs#ExecutionReference"""

    name: Optional[str] = field(default=None)
    creationTimestamp: Optional[str] = field(default=None)
    completionTimestamp: Optional[str] = field(default=None)


@dataclass
class JobStatus(SerializationMixin):
    """https://cloud.google.com/run/docs/reference/rest/v1/namespaces.jobs#jobstatus"""

    observedGeneration: int
    executionCount: int
    conditions: List[Condition] = field(default_factory=list)
    latestCreatedExecution: Optional[ExecutionReference] = field(default=None)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> JobStatus:
        return cls(
            observedGeneration=d.get("observedGeneration"),
            executionCount=d.get("executionCount"),
            conditions=[Condition(**i) for i in d.get("conditions", [])],
            latestCreatedExecution=ExecutionReference(
                name=d.get("latestCreatedExecution", {}).get("name"),
                creationTimestamp=d.get("latestCreatedExecution", {}).get(
                    "creationTimestamp"
                ),
                completionTimestamp=d.get("latestCreatedExecution", {}).get(
                    "completionTimestamp"
                ),
            ),
        )


@dataclass
class Job(SerializationMixin):
    """https://cloud.google.com/run/docs/reference/rest/v1/namespaces.jobs#Job"""

    metadata: ObjectMeta
    spec: JobSpec
    status: JobStatus = field(default=None)
    apiVersion: Optional[str] = field(default=None)
    kind: Optional[str] = field(default=None)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Job:
        return cls(
            metadata=ObjectMeta.from_dict(d["metadata"]),
            spec=JobSpec(
                template=ExecutionTemplateSpec(
                    spec=ExecutionSpec.from_dict(d["spec"]["template"]["spec"])
                )
            ),
            status=JobStatus.from_dict(d.get("status", {})),
            apiVersion=d.get("apiVersion"),
            kind=d.get("kind"),
        )
