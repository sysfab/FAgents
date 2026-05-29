import inspect
import json
from agents import TResponseInputItem
from agents.tool import FunctionTool
from agents.tool_context import ToolContext
from openai.types.responses import EasyInputMessageParam
from openai.types.responses.response_input_param import ResponseInputParam
from openai.types.responses.response_input_text_param import ResponseInputTextParam
from openai.types.responses.response_input_image_param import ResponseInputImageParam
from openai.types.responses.response_input_file_param import ResponseInputFileParam

from FAgents.conversations import Text, Image, File

from typing import TYPE_CHECKING, Union, Any

if TYPE_CHECKING:
    from FAgents.agents import Tool
    from FAgents.conversations import Conversation, Message


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


def _text_to_openai(text: Text) -> ResponseInputTextParam:
    return {"type": "input_text", "text": text.text}


def _image_to_openai(image: Image) -> ResponseInputImageParam:
    return {
        "type": "input_image",
        "detail": image.detail or "auto",
        "image_url": image.url,
    }


def _file_to_openai(file: File) -> ResponseInputFileParam:
    result: ResponseInputFileParam = {"type": "input_file"}
    if file.id is not None:
        result["file_id"] = file.id
    if file.url is not None:
        result["file_url"] = file.url
    if file.data is not None:
        result["file_data"] = file.data
    if file.filename is not None:
        result["filename"] = file.filename
    if file.detail is not None:
        result["detail"] = file.detail
    return result


def to_openai_message(message: Message) -> EasyInputMessageParam:
    content = [
        _text_to_openai(item)
        if isinstance(item, Text)
        else _file_to_openai(item)
        if isinstance(item, File)
        else _image_to_openai(item)
        for item in message.content
    ]
    return {"role": message.role, "content": content, "type": "message"}


def to_openai_input(conversation: Conversation) -> ResponseInputParam:
    return [to_openai_message(message) for message in conversation]


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
