from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, Any

from airflow_google_cloud_run_plugin.cloud_run_v1.utils import SerializationMixin


@dataclass
class ObjectMeta(SerializationMixin):
    """
    https://cloud.google.com/run/docs/reference/rest/v1/ObjectMeta

    NOTE: Annotations need to adhere to https://cloud.google.com/run/docs/troubleshooting#launch-stage-validation
    """

    name: str
    namespace: str
    selfLink: Optional[str] = field(default=None)
    uid: Optional[str] = field(default=None)
    resourceVersion: Optional[str] = field(default=None)
    generation: Optional[int] = field(default=None)
    creationTimestamp: Optional[str] = field(default=None)
    labels: Optional[Dict[str, str]] = field(default=None)
    annotations: Optional[Dict[str, str]] = field(default=None)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> ObjectMeta:
        return cls(
            name=d["name"],
            namespace=d["namespace"],
            selfLink=d.get("selfLink"),
            uid=d.get("uid"),
            resourceVersion=d.get("resourceVersion"),
            generation=d.get("generation"),
            creationTimestamp=d.get("creationTimestamp"),
            labels=d.get("labels", {}),
            annotations=d.get("annotations", {}),
        )
