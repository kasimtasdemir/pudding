"""Component registry for tracking and discovery."""

# src/pudding/core/registry.py
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class ComponentRegistry:
    """Simple registry for component tracking."""

    def __init__(self) -> None:
        self._components: dict[str, dict[str, Any]] = {}

    def register(
        self, name: str, version: str, input_schema: str, output_schema: str
    ) -> None:
        """Register a component."""
        self._components[name] = {
            "version": version,
            "input_schema": input_schema,
            "output_schema": output_schema,
        }
        logger.info(f"Registered component: {name} v{version}")

    def can_connect(
        self, from_component: str, to_component: str
    ) -> tuple[bool, Optional[str]]:
        """Check if two components can be connected."""
        if from_component not in self._components:
            return False, f"Component '{from_component}' not registered"

        if to_component not in self._components:
            return False, f"Component '{to_component}' not registered"

        from_info = self._components[from_component]
        to_info = self._components[to_component]

        if from_info["output_schema"] == to_info["input_schema"]:
            return True, None

        return (
            False,
            f"Schema mismatch: {from_component} outputs {from_info['output_schema']}, {to_component} expects {to_info['input_schema']}",
        )

    def list_components(self) -> list[str]:
        """List all registered components."""
        return list(self._components.keys())


# Global registry instance
registry = ComponentRegistry()
