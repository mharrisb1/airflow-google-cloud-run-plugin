from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Condition:
    """https://cloud.google.com/run/docs/reference/rest/v1/Condition"""

    type: str
    status: str
    reason: Optional[str] = field(default=None)
    message: Optional[str] = field(default=None)
    lastTransitionTime: Optional[str] = field(default=None)
    severity: Optional[str] = field(default=None)
