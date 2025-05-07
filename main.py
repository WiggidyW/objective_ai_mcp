from dataclasses import dataclass
import json
from typing import Any, AsyncIterator, TypedDict, cast
import objective_ai_pb2 as proto
import objective_ai_pb2_grpc as grpc_proto
import grpc
import grpc.aio
import os
from contextlib import asynccontextmanager
from google.protobuf.wrappers_pb2 import StringValue
from google.protobuf.struct_pb2 import Value
from mcp.server.models import InitializationOptions
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.sse import SseServerTransport
import mcp.types

from dotenv import load_dotenv

load_dotenv()

OBJECTIVE_AI_SERVER_ADDRESS = os.environ.get("OBJECTIVE_AI_SERVER_ADDRESS")
OBJECTIVE_AI_SERVER_INSECURE = os.environ.get("OBJECTIVE_AI_SERVER_INSECURE", "").strip().lower() == "true"
PORT = int(os.environ.get("PORT", "8000"))

@dataclass
class AppContext:
    client: grpc_proto.ObjectiveAIStub

@asynccontextmanager
async def app_lifespan(app: Server) -> AsyncIterator[AppContext]:
    if OBJECTIVE_AI_SERVER_INSECURE:
        channel = grpc.aio.insecure_channel(
            OBJECTIVE_AI_SERVER_ADDRESS,
        )
    else:
        channel = grpc.aio.secure_channel(
            OBJECTIVE_AI_SERVER_ADDRESS,
            grpc.ssl_channel_credentials(),
        )
    client = grpc_proto.ObjectiveAIStub(channel)
    try:
        yield AppContext(client)
    finally:
        await channel.close()

class InvalidArgumentsError(Exception):
    def __init__(self, property: str):
        self.property = property

    def __str__(self) -> str:
        return json.dumps(
            {
                "code": 400,
                "error": f"invalid property: {self.property}",
            },
            indent=2
        )

class GrpcError(Exception):
    def __init__(self, error: grpc.aio.AioRpcError):
        self.error = error

    def __str__(self) -> str:
        return json.dumps(
            {
                "code": int(self.error.code()),
                "error": self.error.details(),
            },
            indent=2
        )
    
class GenericError(Exception):
    def __init__(self, error: Exception):
        self.error = error

    def __str__(self) -> str:
        return json.dumps(
            {
                "code": 500,
                "error": str(self.error),
            },
            indent=2
        )
    
class ObjectiveAI:
    @staticmethod
    def convert_input_schema(input_schema: Any | None) -> proto.JsonSchema:
        if input_schema is None:
            raise InvalidArgumentsError(
                f"schema required"
            )
        if not isinstance(input_schema, dict):
            raise InvalidArgumentsError(
                f"schema must be a dictionary"
            )
        schema = input_schema
        input_description = schema.get("description")
        if input_description is not None and not \
            isinstance(input_description, str):
            raise InvalidArgumentsError(
                f"schema.description must be a string"
            )
        description = StringValue(value=input_description)
        match schema.get("type"):
            case "boolean":
                return proto.JsonSchema(
                    boolean=proto.BooleanJsonSchema(
                        description=description,
                    )
                )
            case "integer":
                return proto.JsonSchema(
                    integer=proto.IntegerJsonSchema(
                        description=description,
                    )
                )
            case "number":
                return proto.JsonSchema(
                    number=proto.NumberJsonSchema(
                        description=description,
                    )
                )
            case "string":
                input_enum = schema.get("enum")
                if input_enum is not None and \
                    (not isinstance(input_enum, list) or \
                    not all(isinstance(e, str) for e in input_enum)):
                    raise InvalidArgumentsError(
                        f"schema.enum must be a list of strings"
                    )
                enum = input_enum
                return proto.JsonSchema(
                    string=proto.StringJsonSchema(
                        description=description,
                        enum=enum,
                    )
                )
            case "array":
                input_items = schema.get("items")
                if input_items is not None and \
                    not isinstance(input_items, dict):
                    raise InvalidArgumentsError(
                        f"schema.items must be a dictionary"
                    )
                items = ObjectiveAI.convert_input_schema(input_items) if input_items else None
                return proto.JsonSchema(
                    array=proto.ArrayJsonSchema(
                        description=description,
                        items=items,
                    )
                )
            case "object":
                input_properties = schema.get("properties")
                if input_properties is not None and \
                    not isinstance(input_properties, list):
                    raise InvalidArgumentsError(
                        f"schema.properties must be a list"
                    )
                properties = []
                for input_property in input_properties:
                    input_property_name = input_property.get("name")
                    if input_property_name is None:
                        raise InvalidArgumentsError(
                            f"schema.properties.name required"
                        )
                    if not isinstance(input_property_name, str):
                        raise InvalidArgumentsError(
                            f"schema.properties.name must be a string"
                        )
                    property_name = input_property_name
                    if not isinstance(input_property, dict):
                        raise InvalidArgumentsError(
                            f"schema.properties must be a dictionary"
                        )
                    property_schema = ObjectiveAI.convert_input_schema(
                        input_property
                    )
                    properties.append(proto.ObjectJsonSchemaProperty(
                        key=property_name,
                        value=property_schema,
                    ))
                return proto.JsonSchema(
                    object=proto.ObjectJsonSchema(
                        description=description,
                        properties=properties,
                    )
                )

    @staticmethod
    def convert_input_messages(input_messages: Any | None) -> list[proto.Message]:
        if input_messages is None:
            raise InvalidArgumentsError(
                f"messages required"
            )
        if not isinstance(input_messages, list):
            raise InvalidArgumentsError(
                f"messages must be a list"
            )
        if len(input_messages) == 0:
            raise InvalidArgumentsError(
                f"messages must not be empty"
            )
        messages = []
        for input_message in input_messages:
            if not isinstance(input_message, dict):
                raise InvalidArgumentsError(
                    f"messages must be a list of dictionaries"
                )
            content = input_message.get("content")
            if content is None:
                raise InvalidArgumentsError(
                    f"message.content required"
                )
            if not isinstance(content, str):
                raise InvalidArgumentsError(
                    f"message.content must be a string"
                )
            role = input_message.get("role")
            match role:
                case "user":
                    messages.append(proto.Message(
                        user=proto.UserMessage(
                            content=proto.MessageContent(
                                text=content,
                            )
                        )
                    ))
                case "assistant":
                    messages.append(proto.Message(
                        assistant=proto.AssistantMessage(
                            content=proto.MessageContent(
                                text=content,
                            ),
                            tool_calls=None,
                        )
                    ))
                case "system":
                    messages.append(proto.Message(
                        system=proto.SystemMessage(
                            content=proto.MessageContent(
                                text=content,
                            )
                        )
                    ))
                case _:
                    raise InvalidArgumentsError(
                        f"message.role must be one of user, assistant, system"
                    )
        return messages
    
    @staticmethod
    def convert_input_meta_model(input_meta_model: Any | None) -> str:
        if input_meta_model is None:
            raise InvalidArgumentsError(
                f"meta_model required"
            )
        if not isinstance(input_meta_model, str):
            raise InvalidArgumentsError(
                f"meta_model must be a string"
            )
        if not input_meta_model in ["objectiveai/pauper_1"]:
            raise InvalidArgumentsError(
                f"invalid meta model: {input_meta_model}"
            )
        return input_meta_model
    
    @staticmethod
    def convert_value(value: Value) -> Any:
        match value.WhichOneof('kind'):
            case "null_value":
                return None
            case "number_value":
                return value.number_value
            case "string_value":
                return value.string_value
            case "bool_value":
                return value.bool_value
            case "struct_value":
                return {key: ObjectiveAI.convert_value(val) for key, val in value.struct_value.fields.items()}
            case "list_value":
                return [ObjectiveAI.convert_value(val) for val in value.list_value.values]
            case _:
                raise Exception("invalid proto value kind")
            
    # class Reasoning(TypedDict):
    #     expert_name: str
    #     reasoning: str
    
    class Choice(TypedDict):
        id: str
        reasoning: list[str]
        response: Any
        response_confidence: float
    
    class Response(TypedDict):
        choices: list['ObjectiveAI.Choice']
        winner_id: str
        winner_confidence: float

    async def objective_ai(
        meta_model: Any,
        messages: Any,
        schema: Any,
        ctx: AppContext,
    ) -> list[mcp.types.TextContent | mcp.types.ImageContent | mcp.types.EmbeddedResource]:
        client = ctx.client
        request = proto.QueryRequest(
            meta_model=ObjectiveAI.convert_input_meta_model(meta_model),
            messages=ObjectiveAI.convert_input_messages(messages),
            response_format=ObjectiveAI.convert_input_schema(schema),
        )
        response = ObjectiveAI.Response(
            choices=[],
            winner_id="",
            winner_confidence=0.0,
        )
        stream = cast(
            grpc.aio.UnaryStreamCall[
                proto.QueryRequest,
                proto.QueryStreamingResponse,
            ],
            client.QueryStreaming(request),
        )
        i = 0
        i_max = 27
        while True:
            item = await stream.read()
            if item == grpc.aio.EOF:
                break
            item = cast(proto.QueryStreamingResponse, item)
            if item.choice is not None and \
                item.choice.id is not None and \
                len(item.choice.id) > 0:
                vote = item.choice.votes[0]
                response["choices"].append(
                    ObjectiveAI.Choice(
                        id=item.choice.id,
                        reasoning=[vote.reasoning],
                        response=ObjectiveAI.convert_value(item.choice.message.content),
                        response_confidence=item.choice.confidence,
                    )
                )
            elif item.vote is not None and \
                item.vote.id is not None and \
                len(item.vote.id) > 0:
                choice = next(
                    (c for c in response["choices"] if c["id"] == vote.id),
                    None,
                )
                choice["reasoning"].append(vote.reasoning)
            elif item.choice_confidence is not None and \
                len(item.choice_confidence.confidence) > 0:
                for choice in response["choices"]:
                    choice["response_confidence"] = \
                        item.choice_confidence.confidence[choice["id"]]
                response["choices"].sort(
                    key=lambda x: x["response_confidence"],
                    reverse=True
                )
                if len(response["choices"]) > 0:
                    response["winner_id"] = \
                        response["choices"][0]["id"]
                    response["winner_confidence"] = \
                        response["choices"][0]["response_confidence"]
            else:
                raise Exception("invalid query streaming response kind")
            i += 1
        return [
            mcp.types.EmbeddedResource(
                type="text",
                text=json.dumps(response, indent=2)
            )
        ]

app = Server("Objective AI", lifespan=app_lifespan)
    
@app.list_tools()
async def list_tools() -> list[mcp.types.Tool]:
    return [
        mcp.types.Tool(
            name="query_objective_ai",
            description="Query Objective AI. Get a JSON response to an objective query.",
            annotations=mcp.types.ToolAnnotations(
                title="Objective AI",
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            inputSchema={
                "type": "object",
                "required": ["meta_model", "messages", "schema"],
                "additionalProperties": False,
                "properties": {
                    "meta_model": {
                        "description": "Objective AI MetaModel.",
                        "type": "string",
                        "enum": [
                            "objectiveai/pauper_1",
                        ],
                    },
                    "messages": {
                        "description": "Objective AI query. Conforms to the OpenAI API chat message format.",
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["role", "content"],
                            "additionalProperties": False,
                            "properties": {
                                "role": {
                                    "description": "Role of the message sender",
                                    "type": "string",
                                    "enum": [
                                        "user",
                                        "assistant",
                                        "system",
                                    ],
                                },
                                "content": {
                                    "description": "Content of the message",
                                    "type": "string",
                                },
                            },
                        },
                    },
                    "schema": {
                        "$ref": "#/$defs/schema",
                    },
                },
                "$defs": {
                    "schema": {
                        "anyOf": [
                            {
                                "type": "object",
                                "required": ["type", "name", "description"],
                                "additionalProperties": False,
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "enum": ["boolean"]
                                    },
                                    "name": {
                                        "type": "string",
                                    },
                                    "description": {
                                        "type": "string",
                                    },
                                },
                            },
                            {
                                "type": "object",
                                "required": ["type", "name", "description"],
                                "additionalProperties": False,
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "enum": ["integer"]
                                    },
                                    "name": {
                                        "type": "string",
                                    },
                                    "description": {
                                        "type": "string",
                                    },
                                },
                            },
                            {
                                "type": "object",
                                "required": ["type", "name", "description"],
                                "additionalProperties": False,
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "enum": ["number"]
                                    },
                                    "name": {
                                        "type": "string",
                                    },
                                    "description": {
                                        "type": "string",
                                    },
                                },
                            },
                            {
                                "type": "object",
                                "required": ["type", "name", "description", "enum"],
                                "additionalProperties": False,
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "enum": ["string"]
                                    },
                                    "name": {
                                        "type": "string",
                                    },
                                    "description": {
                                        "type": "string",
                                    },
                                    "enum": {
                                        "type": ["array", "null"],
                                        "items": {
                                            "type": "string",
                                        },
                                    },
                                },
                            },
                            {
                                "type": "object",
                                "required": ["type", "name", "description", "items"],
                                "additionalProperties": False,
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "enum": ["array"]
                                    },
                                    "name": {
                                        "type": "string",
                                    },
                                    "description": {
                                        "type": "string",
                                    },
                                    "items": {
                                        "$ref": "#/$defs/schema",
                                    },
                                },
                            },
                            {
                                "type": "object",
                                "required": ["type", "name", "description", "properties"],
                                "additionalProperties": False,
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "enum": ["object"]
                                    },
                                    "name": {
                                        "type": "string",
                                    },
                                    "description": {
                                        "type": "string",
                                    },
                                    "properties": {
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/$defs/schema",
                                        },
                                    },
                                },
                            },
                        ],
                    },
                },
            },
        )
    ]

@app.call_tool()
async def call_tool(
    name: str,
    argument: dict[str, Any],
) -> list[mcp.types.TextContent | mcp.types.ImageContent | mcp.types.EmbeddedResource]:
    ctx = app.request_context.lifespan_context
    print(f"call_tool: {name} {argument}")
    try:
        match name:
            case "query_objective_ai":
                return await ObjectiveAI.objective_ai(
                    argument.get("meta_model"),
                    argument.get("messages"),
                    argument.get("schema"),
                    ctx,
                )
            case _:
                raise InvalidArgumentsError(f"invalid tool name: {name}")
    except grpc.aio.AioRpcError as e:
        raise GrpcError(e)
    except Exception as e:
        raise GenericError(e)
        
def run():
    from mcp.server.sse import SseServerTransport
    from starlette.applications import Starlette
    from starlette.responses import Response
    from starlette.routing import Mount, Route
    import uvicorn

    sse = SseServerTransport("/messages/")

    async def handle_sse(request):
        async with sse.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            await app.run(
                streams[0], streams[1], app.create_initialization_options()
            )
        return Response()
    
    uvicorn.run(
        Starlette(
            debug=True,
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages/", app=sse.handle_post_message),
                Route("/", endpoint=handle_sse),
            ],
        ),
        host="0.0.0.0",
        port=PORT,
    )

if __name__ == "__main__":
    run()
