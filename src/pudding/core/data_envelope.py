"""Core data structures for self-describing data."""

# src/pudding/core/data_envelope.py
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field


class DataType(str, Enum):
    """Types of data that can be wrapped in DataEnvelope"""

    COMPONENT_INPUT = "component_input"
    COMPONENT_OUTPUT = "component_output"
    RAW_DATA = "raw_data"


class DataEnvelope(BaseModel):
    """Universal wrapper for all data with rich metadata"""

    envelope_version: str = "1.0"
    data_type: DataType

    # Component context
    component_name: Optional[str] = None
    component_version: Optional[str] = None

    # Data classification
    data_tags: list[str] = Field(default_factory=list)
    schema_name: Optional[str] = None
    schema_version: Optional[str] = None

    # Execution context
    execution_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source_info: Optional[dict[str, Any]] = None

    # Lineage tracking
    lineage: list[dict[str, str]] = Field(default_factory=list)

    # The actual data
    data: dict[str, Any]

    class Config:
        arbitrary_types_allowed = True


class ComponentMetadata(BaseModel):
    """Metadata tracked for each component execution"""

    component_name: str
    component_version: str
    executed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    execution_id: Optional[str] = None
    debug_mode: bool = False
    input_source_type: Optional[str] = None
    is_replay: bool = False
    data_lineage: list[dict[str, str]] = Field(default_factory=list)


TOutput = TypeVar("TOutput", bound=BaseModel)


class ComponentResult(BaseModel, Generic[TOutput]):
    """Wrapper for component results with metadata and error handling."""

    data: Optional[TOutput] = None
    metadata: ComponentMetadata
    error: Optional[str] = None
    warnings: list[str] = Field(default_factory=list)
    envelope: Optional[DataEnvelope] = None

    class Config:
        arbitrary_types_allowed = True
