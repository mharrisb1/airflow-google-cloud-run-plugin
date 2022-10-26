from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union

from airflow_google_cloud_run_plugin.cloud_run_v1.utils import SerializationMixin


@dataclass
class ContainerPort:
    """https://cloud.google.com/run/docs/reference/rest/v1/Container#ContainerPort"""

    name: str
    containerPort: int
    protocol: str


@dataclass
class ResourceRequirements:
    """https://cloud.google.com/run/docs/reference/rest/v1/Container#ResourceRequirements"""

    limits: Dict[str, str]
    # TODO - requests


@dataclass
class SecretKeySelector:
    """https://cloud.google.com/run/docs/reference/rest/v1/Container#SecretKeySelector"""

    name: str
    key: Union[str, int]
    optional: Optional[bool] = field(default=None)


@dataclass
class EnvVarSource:
    """https://cloud.google.com/run/docs/reference/rest/v1/Container#envvarsource"""

    secretKeyRef: SecretKeySelector


@dataclass
class EnvVar(SerializationMixin):
    """https://cloud.google.com/run/docs/reference/rest/v1/Container#EnvVar"""

    name: str
    value: str = field(default=None)
    valueFrom: Optional[EnvVarSource] = field(default=None)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> EnvVar:
        return cls(
            name=d.get("name"),
            value=d.get("value"),
            valueFrom=EnvVarSource(
                secretKeyRef=SecretKeySelector(
                    key=d.get("valueFrom", {}).get("secretKeyRef", {}).get("key"),
                    optional=d.get("valueFrom", {})
                    .get("secretKeyRef", {})
                    .get("optional"),
                    name=d.get("valueFrom", {}).get("secretKeyRef", {}).get("name"),
                )
            ),
        )


@dataclass
class Container(SerializationMixin):
    """https://cloud.google.com/run/docs/reference/rest/v1/Container"""

    image: str
    resources: ResourceRequirements
    name: Optional[str] = field(default=None)
    ports: List[ContainerPort] = field(default_factory=list)
    command: List[str] = field(default_factory=list)
    args: List[str] = field(default_factory=list)
    env: List[EnvVar] = field(default_factory=list)
    workingDir: Optional[str] = field(default=None)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Container:
        return cls(
            image=d["image"],
            resources=ResourceRequirements(limits=d["resources"]["limits"]),
            ports=[ContainerPort(**i) for i in d.get("ports", [])],
            command=d.get("command", []),
            args=d.get("args", []),
            env=[EnvVar.from_dict(i) for i in d.get("env", [])],
            workingDir=d.get("workingDir"),
        )
