import inspect
import json
from agents.tool import FunctionTool
from agents.tool_context import ToolContext


from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from typing import Any
    from FAgents.agents import Tool


def to_openai_tool(tool: Tool[Any, Any]) -> FunctionTool:
    params = tool.Signature.parameters
    properties: dict[str, object] = {}
    required: list[str] = []

    for name, param in params.items():
        json_type = _python_type_to_json(param.annotation)
        properties[name] = {"type": json_type}
        if param.default is inspect.Parameter.empty:
            required.append(name)

    async def on_invoke(ctx: ToolContext[Any], args_json: str) -> Any:
        args = json.loads(args_json)
        return tool(**args)

    return FunctionTool(
        name=tool.Name,
        description=tool.Description,
        params_json_schema={
            "type": "object",
            "properties": properties,
            "required": required,
        },
        on_invoke_tool=on_invoke,
    )


def _python_type_to_json(ann: Any) -> str:
    import types

    if ann is inspect.Parameter.empty:
        return "string"
    origin = getattr(ann, "__origin__", None)
    if origin is types.UnionType or origin is Union:
        args = [a for a in ann.__args__ if a is not type(None)]
        return _python_type_to_json(args[0]) if args else "string"
    return {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
    }.get(ann, "string")
