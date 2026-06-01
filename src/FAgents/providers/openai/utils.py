import inspect
import json
from agents.tool import FunctionTool
from agents.tool_context import ToolContext

from FAgents import Messages, Message, ToolCall, ToolCallOutput, Text, Image, File

from typing import TYPE_CHECKING, Union, Literal, LiteralString, Any, cast

if TYPE_CHECKING:
    from FAgents import tool


#
# HELPERS
#
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


#
# TO
#
def to_openai_tool(tool: tool[Any, Any]) -> FunctionTool:
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

        if tool.IsAwaitable:
            return await tool(**args)
        else:
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


def to_openai_input(messages: Messages) -> list:
    return [
        to_openai_message(message)
        if isinstance(message, Message)
        else to_openai_tool_call(message)
        if isinstance(message, ToolCall)
        else to_openai_tool_call_output(message)
        for message in messages
    ]


def to_openai_message(message: Message) -> dict:
    item_type = "output" if message.role == "assistant" else "input"
    content = [
        to_openai_text(item, item_type=item_type)
        if isinstance(item, Text)
        else to_openai_file(item, item_type=item_type)
        if isinstance(item, File)
        else to_openai_image(item, item_type=item_type)
        for item in message.content
    ]
    return {"role": message.role, "content": content, "type": "message"}


def to_openai_tool_call(tool_call: ToolCall) -> dict:
    return {
        "arguments": tool_call.arguments,
        "name": tool_call.name,
        "id": tool_call.id,
        "call_id": tool_call.call_id,
        "status": tool_call.status,
        "type": "function_call",
    }


def to_openai_tool_call_output(
    tool_call_output: ToolCallOutput,
) -> dict:
    return {
        "output": tool_call_output.output,
        "call_id": tool_call_output.call_id,
        "type": "function_call_output",
    }


def to_openai_text(text: Text, item_type: Literal["input", "output"]):
    return {"type": f"{item_type}_text", "text": text.text}


def to_openai_image(image: Image, item_type: Literal["input", "output"]):
    return {
        "type": f"{item_type}_image",
        "detail": image.detail,
        "image_url": image.url,
    }


def to_openai_file(file: File, item_type: Literal["input", "output"]):
    result = {"type": f"{item_type}_file"}
    if file.id is not None:
        result["file_id"] = cast(LiteralString, file.id)
    if file.url is not None:
        result["file_url"] = cast(LiteralString, file.url)
    if file.data is not None:
        result["file_data"] = cast(LiteralString, file.data)
    if file.filename is not None:
        result["filename"] = cast(LiteralString, file.filename)
    if file.detail is not None:
        result["detail"] = cast(LiteralString, file.detail)
    return result


#
# FROM
#
def from_openai_input(messages) -> Messages:
    return Messages(
        *[
            msg
            for message in messages
            if (
                msg := (
                    from_openai_message(message)
                    if message["type"] == "message"
                    else from_openai_tool_call(message)
                    if message["type"] == "function_call"
                    else from_openai_tool_call_output(message)
                    if message["type"] == "function_call_output"
                    else None
                )
            )
            is not None
        ]
    )


def from_openai_message(message: dict) -> Message:
    content = []
    for content_item in message["content"]:
        if "text" in content_item["type"]:
            content.append(from_openai_text(content_item))
        elif "image" in content_item["type"]:
            content.append(from_openai_image(content_item))
        elif "file" in content_item["type"]:
            content.append(from_openai_file(content_item))

    return Message(role=message["role"], content=content)


def from_openai_tool_call(tool_call: dict) -> ToolCall:
    return ToolCall(
        arguments=tool_call["arguments"],
        name=tool_call["name"],
        id=tool_call["id"],
        call_id=tool_call["call_id"],
        status=tool_call["status"],
    )


def from_openai_tool_call_output(
    tool_call_output: dict,
) -> ToolCallOutput:
    return ToolCallOutput(
        output=tool_call_output["output"],
        call_id=tool_call_output["call_id"],
    )


def from_openai_text(text: dict) -> Text:
    return Text(text=text["text"])


def from_openai_image(image: dict) -> Image:
    return Image(
        detail=image["detail"],
        url=image["image_url"],
        format=image["format"],
    )


def from_openai_file(file: dict) -> File:
    return File(
        id=file.get("file_id"),
        url=file.get("file_url"),
        data=file.get("file_data"),
        filename=file.get("filename"),
        detail=file.get("detail") or "low",
    )
