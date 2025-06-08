"""Configuration classes for component execution."""

# src/pudding/core/config.py
from enum import Flag, auto
from typing import Any, Optional

from pydantic import BaseModel


class SampleSaveMode(Flag):
    """Flags for controlling what samples to save"""

    NONE = 0
    INPUT = auto()
    OUTPUT = auto()
    BOTH = INPUT | OUTPUT


class RunConfig(BaseModel):
    """Configuration for component execution"""

    # Debugging options
    debug_mode: bool = False
    save_samples: SampleSaveMode = SampleSaveMode.NONE

    # Execution context
    execution_id: Optional[str] = None
    source_info: Optional[dict[str, Any]] = None

    # Performance options
    skip_compatibility_check: bool = False
    timeout: Optional[float] = None
    max_retries: int = 0

    # Sample storage options
    sample_name_prefix: Optional[str] = None
    compress_samples: bool = False

    class Config:
        arbitrary_types_allowed = True

    # Convenience factory methods
    @classmethod
    def debug(cls, save_all: bool = True) -> "RunConfig":
        """Create debug configuration"""
        return cls(
            debug_mode=True,
            save_samples=SampleSaveMode.BOTH if save_all else SampleSaveMode.NONE,
        )

    @classmethod
    def production(cls, execution_id: str) -> "RunConfig":
        """Create production configuration"""
        return cls(
            debug_mode=False,
            save_samples=SampleSaveMode.NONE,
            execution_id=execution_id,
            skip_compatibility_check=False,
        )

    @classmethod
    def testing(cls, save_output_only: bool = False) -> "RunConfig":
        """Create testing configuration"""
        return cls(
            debug_mode=True,
            save_samples=SampleSaveMode.OUTPUT
            if save_output_only
            else SampleSaveMode.BOTH,
        )
