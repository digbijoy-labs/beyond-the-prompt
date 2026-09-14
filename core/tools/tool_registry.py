"""
Grammar-Constrained Tool Registry & Coercion Engine (Chapter 4 Reference Blueprint)
Forces model tool calls to conform strictly to Pydantic schemas before execution.
"""

from __future__ import annotations

from typing import Any, Callable, Type
from pydantic import BaseModel, ValidationError


class RegisteredTool(BaseModel):
    name: str
    description: str
    schema_model: Type[BaseModel]

    class Config:
        arbitrary_types_allowed = True


class GrammarToolRegistry:
    """
    Central tool repository exposing JSON schemas and validating raw arguments.
    Prevents hallucinated parameter injection.
    """

    def __init__(self):
        self._tools: dict[str, tuple[RegisteredTool, Callable]] = {}

    def register(self, name: str, description: str, schema_model: Type[BaseModel]):
        def decorator(fn: Callable):
            tool = RegisteredTool(name=name, description=description, schema_model=schema_model)
            self._tools[name] = (tool, fn)
            return fn
        return decorator

    def get_tool_schemas(self) -> list[dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.schema_model.model_json_schema(),
                },
            }
            for t, _ in self._tools.values()
        ]

    def coerce_and_execute(self, tool_name: str, raw_params: dict[str, Any]) -> Any:
        if tool_name not in self._tools:
            raise KeyError(f"Tool '{tool_name}' not found in registry")
        tool_meta, fn = self._tools[tool_name]
        try:
            validated_model = tool_meta.schema_model.model_validate(raw_params)
        except ValidationError as err:
            raise ValueError(f"Schema violation for '{tool_name}': {err}") from err

        return fn(**validated_model.model_dump())
