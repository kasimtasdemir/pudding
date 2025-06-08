"""Core components of the pudding pipeline framework."""

# src/pudding/core/__init__.py
from .base_component import BaseComponent
from .config import RunConfig, SampleSaveMode
from .data_envelope import ComponentMetadata, ComponentResult, DataEnvelope, DataType
from .registry import registry

__all__ = [
    "BaseComponent",
    "RunConfig",
    "SampleSaveMode",
    "DataEnvelope",
    "DataType",
    "ComponentResult",
    "ComponentMetadata",
    "registry",
]
