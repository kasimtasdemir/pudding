"""Pudding - A novel pipeline framework for debuggable data processing."""

from .core import (
    BaseComponent,
    ComponentMetadata,
    ComponentResult,
    DataEnvelope,
    DataType,
    RunConfig,
    SampleSaveMode,
    registry,
)

__version__ = "0.1.0"

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
