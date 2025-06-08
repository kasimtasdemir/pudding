"""Base component framework for all pipeline components."""

# src/pudding/core/base_component.py
import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel

from .config import RunConfig, SampleSaveMode
from .data_envelope import ComponentMetadata, ComponentResult, DataEnvelope, DataType

# Set up module logger
logger = logging.getLogger(__name__)

# Generic type variables
TInput = TypeVar("TInput", bound=BaseModel)
TOutput = TypeVar("TOutput", bound=BaseModel)


class BaseComponent(ABC, Generic[TInput, TOutput]):
    """Abstract base class for all pipeline components."""

    def __init__(
        self,
        name: str,
        version: str,
        input_schema: type[TInput],
        output_schema: type[TOutput],
        sample_data_dir: Optional[Path] = None,
    ):
        self.name = name
        self.version = version
        self.input_schema = input_schema
        self.output_schema = output_schema

        # Set up sample data directory
        if sample_data_dir:
            self.sample_data_dir = Path(sample_data_dir)
        else:
            self.sample_data_dir = Path.cwd() / "sample_data" / name
        self.sample_data_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Initialized {name} v{version}")

    @abstractmethod
    async def process(self, input_data: TInput) -> TOutput:
        """Core processing logic. Must be implemented by each component."""
        pass

    def prepare_input(self, input_dict: dict[str, Any]) -> dict[str, Any]:
        """Transform input from previous component to expected format."""
        return input_dict

    async def run(
        self,
        input_source: Any = None,
        config: Optional[RunConfig] = None,
        **process_kwargs: Any,
    ) -> ComponentResult[TOutput]:
        """
        Universal run method accepting multiple input types.

        Args:
            input_source: Can be:
                - None: Use latest saved input (replay mode)
                - dict: Direct data
                - BaseModel: Pydantic model instance
                - ComponentResult: Output from another component
                - BaseComponent: Use latest output from that component
                - str/Path: Load from file
            config: Execution configuration
            **process_kwargs: Additional arguments passed to process()
        """
        if config is None:
            config = RunConfig()

        # Initialize metadata
        metadata = ComponentMetadata(
            component_name=self.name,
            component_version=self.version,
            debug_mode=config.debug_mode,
            execution_id=config.execution_id or "local_run",
        )

        try:
            # Handle empty argument - use latest input
            if input_source is None:
                logger.info(f"🔄 REPLAY MODE: Using latest saved input for {self.name}")
                envelope = self._get_latest_envelope(DataType.COMPONENT_INPUT)
                if not envelope:
                    raise ValueError(f"No saved inputs found for {self.name}")
                metadata.is_replay = True
                metadata.input_source_type = "latest_saved_input"
            else:
                # Normalize to DataEnvelope
                envelope = await self._normalize_to_envelope(input_source)
                metadata.input_source_type = self._get_source_type_name(input_source)

            # Update metadata with lineage
            metadata.data_lineage = envelope.lineage.copy()

            # Check compatibility
            if not config.skip_compatibility_check:
                can_process, reason = self.can_process(envelope)
                if not can_process:
                    raise ValueError(
                        f"Component {self.name} cannot process this data: {reason}"
                    )

            # Log data source
            if config.debug_mode:
                self._log_data_source(envelope, metadata.is_replay)

            # Extract and prepare data
            input_dict = envelope.data
            transformed_input = self.prepare_input(input_dict)

            # Validate input
            validated_input = self.input_schema(**transformed_input)

            # Save input sample if requested
            if config.save_samples & SampleSaveMode.INPUT:
                self._save_sample(
                    DataType.COMPONENT_INPUT,
                    transformed_input,
                    metadata,
                    prefix=config.sample_name_prefix,
                )

            # Execute core processing
            raw_output = await self.process(validated_input, **process_kwargs)

            # Validate output
            if isinstance(raw_output, self.output_schema):
                validated_output = raw_output
            else:
                validated_output = self.output_schema.model_validate(
                    raw_output.model_dump()
                )

            # Create output envelope
            output_envelope = self._create_output_envelope(
                validated_output, metadata, envelope
            )

            # Create successful result
            result: ComponentResult[TOutput] = ComponentResult(
                data=validated_output, metadata=metadata, envelope=output_envelope
            )

            # Save output sample if requested
            if config.save_samples & SampleSaveMode.OUTPUT:
                self._save_sample(
                    DataType.COMPONENT_OUTPUT,
                    validated_output.model_dump(),
                    metadata,
                    prefix=config.sample_name_prefix,
                )

            if config.debug_mode:
                logger.info(f"✅ {self.name}: Completed successfully")

            return result

        except Exception as e:
            error_msg = f"Component {self.name} failed: {str(e)}"
            logger.error(error_msg, exc_info=config.debug_mode)

            return ComponentResult(data=None, metadata=metadata, error=error_msg)

    def can_process(self, envelope: DataEnvelope) -> tuple[bool, Optional[str]]:
        """Check if this component can process the given data."""
        # Basic implementation - can be overridden
        if envelope.schema_name and envelope.schema_name != self.input_schema.__name__:
            # Check if we have prepare_input that might handle it
            if self.prepare_input.__name__ != BaseComponent.prepare_input.__name__:
                return True, "Will transform using prepare_input()"
            return (
                False,
                f"Schema mismatch: expects {self.input_schema.__name__}, got {envelope.schema_name}",
            )
        return True, None

    async def _normalize_to_envelope(self, input_source: Any) -> DataEnvelope:
        """Convert various input types to DataEnvelope."""
        # String could be a path or sample name
        if isinstance(input_source, str):
            return self.load_sample(input_source)

        # Path object
        elif isinstance(input_source, Path):
            return self.load_sample(str(input_source))

        # DataEnvelope - already normalized
        elif isinstance(input_source, DataEnvelope):
            return input_source

        # ComponentResult - extract envelope or create from data
        elif isinstance(input_source, ComponentResult):
            if input_source.envelope:
                return input_source.envelope
            else:
                return DataEnvelope(
                    data_type=DataType.COMPONENT_OUTPUT,
                    component_name=input_source.metadata.component_name,
                    component_version=input_source.metadata.component_version,
                    data=input_source.data.model_dump() if input_source.data else {},
                    execution_id=input_source.metadata.execution_id,
                    timestamp=input_source.metadata.executed_at,
                    lineage=input_source.metadata.data_lineage,
                )

        # Another component - load its latest output
        elif isinstance(input_source, BaseComponent):
            envelope = input_source._get_latest_envelope(DataType.COMPONENT_OUTPUT)
            if not envelope:
                raise ValueError(f"No output samples found for {input_source.name}")
            logger.info(f"Loading latest output from {input_source.name}")
            return envelope

        # BaseModel - wrap in envelope
        elif isinstance(input_source, BaseModel):
            return DataEnvelope(
                data_type=DataType.RAW_DATA,
                data=input_source.model_dump(),
                schema_name=input_source.__class__.__name__,
            )

        # Dict - wrap in envelope
        elif isinstance(input_source, dict):
            return DataEnvelope(data_type=DataType.RAW_DATA, data=input_source)

        # Tuple of (component, sample_name)
        elif isinstance(input_source, tuple) and len(input_source) == 2:
            component, sample_name = input_source
            if isinstance(component, BaseComponent):
                return component.load_sample(sample_name)
            else:
                raise ValueError(
                    f"First element of tuple must be a BaseComponent, got {type(component)}"
                )

        else:
            raise ValueError(f"Unsupported input source type: {type(input_source)}")

    def _save_sample(
        self,
        sample_type: DataType,
        data: dict[str, Any],
        metadata: ComponentMetadata,
        prefix: Optional[str] = None,
    ) -> None:
        """Save sample data as DataEnvelope."""
        envelope = DataEnvelope(
            data_type=sample_type,
            component_name=self.name,
            component_version=self.version,
            schema_name=self.input_schema.__name__
            if sample_type == DataType.COMPONENT_INPUT
            else self.output_schema.__name__,
            execution_id=metadata.execution_id,
            timestamp=metadata.executed_at,
            data=data,
            lineage=metadata.data_lineage,
        )

        # Create filename with microseconds and counter to prevent collisions
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[
            :-3
        ]  # Include milliseconds
        type_prefix = "input" if sample_type == DataType.COMPONENT_INPUT else "output"

        if prefix:
            base_filename = f"{prefix}_{type_prefix}_{timestamp}"
        else:
            base_filename = f"{type_prefix}_{timestamp}"

        # Add counter if file exists
        counter = 0
        while True:
            if counter == 0:
                filename = f"{base_filename}.json"
            else:
                filename = f"{base_filename}_{counter:03d}.json"

            filepath = self.sample_data_dir / filename
            if not filepath.exists():
                break
            counter += 1

        # Save envelope
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(
                envelope.model_dump(), f, indent=2, default=str, ensure_ascii=False
            )

        logger.info(f"💾 {self.name}: Saved {sample_type.value} to {filepath}")

    def load_sample(self, filename: str) -> DataEnvelope:
        """Load sample data and return as DataEnvelope."""
        if Path(filename).is_absolute():
            filepath = Path(filename)
        else:
            filepath = self.sample_data_dir / filename

        if not filepath.exists():
            raise FileNotFoundError(f"Sample file not found: {filename}")

        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)

        return DataEnvelope(**data)

    def _get_latest_envelope(self, data_type: DataType) -> Optional[DataEnvelope]:
        """Get the most recent DataEnvelope of specified type."""
        prefix = "input_" if data_type == DataType.COMPONENT_INPUT else "output_"
        pattern = f"{prefix}*.json"
        files = list(self.sample_data_dir.glob(pattern))

        if not files:
            return None

        latest = max(files, key=lambda f: f.stat().st_mtime)
        return self.load_sample(latest.name)

    def _log_data_source(self, envelope: DataEnvelope, is_replay: bool = False) -> None:
        """Log human-readable description of data source."""
        parts = []

        if is_replay:
            parts.append("🔄 REPLAY")

        if envelope.component_name:
            parts.append(f"From: {envelope.component_name}")

        if envelope.schema_name:
            parts.append(f"Schema: {envelope.schema_name}")

        if envelope.data_tags:
            parts.append(f"Tags: {envelope.data_tags}")

        logger.info(" | ".join(parts))

    def _create_output_envelope(
        self,
        output_data: TOutput,
        metadata: ComponentMetadata,
        input_envelope: DataEnvelope,
    ) -> DataEnvelope:
        """Create output envelope with updated lineage."""
        lineage = input_envelope.lineage.copy()
        lineage.append(
            {
                "component": self.name,
                "version": self.version,
                "timestamp": metadata.executed_at.isoformat(),
                "execution_id": metadata.execution_id or "",
            }
        )

        return DataEnvelope(
            data_type=DataType.COMPONENT_OUTPUT,
            component_name=self.name,
            component_version=self.version,
            schema_name=self.output_schema.__name__,
            execution_id=metadata.execution_id,
            timestamp=metadata.executed_at,
            data=output_data.model_dump(),
            lineage=lineage,
        )

    def _get_source_type_name(self, input_source: Any) -> str:
        """Get human-readable name for input source type."""
        if isinstance(input_source, dict):
            return "dict"
        elif isinstance(input_source, BaseModel):
            return f"model:{input_source.__class__.__name__}"
        elif isinstance(input_source, ComponentResult):
            return "component_result"
        elif isinstance(input_source, DataEnvelope):
            return "data_envelope"
        elif isinstance(input_source, BaseComponent):
            return f"component:{input_source.name}"
        elif isinstance(input_source, (str, Path)):
            return "file"
        else:
            return "unknown"

    def list_samples(self, sample_type: Optional[str] = None) -> list[str]:
        """List available sample files."""
        if sample_type:
            pattern = f"{sample_type}_*.json"
        else:
            pattern = "*.json"

        files = sorted(self.sample_data_dir.glob(pattern))
        return [f.name for f in files]
