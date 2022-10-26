from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import Any, Dict


class SerializationMixin(ABC):
    @classmethod
    @abstractmethod
    def from_dict(cls, d: Dict[str, Any]) -> SerializationMixin:
        raise NotImplementedError

    def to_dict(self: Any) -> Dict[str, Any]:
        return asdict(
            self,
            dict_factory=lambda x: {
                k: v for (k, v) in x if v is not None and v != [] and v != {}
            },
        )
