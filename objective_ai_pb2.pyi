from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QueryChoiceVoteKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GENERATE: _ClassVar[QueryChoiceVoteKind]
    SELECT: _ClassVar[QueryChoiceVoteKind]

class Role(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    USER: _ClassVar[Role]
    ASSISTANT: _ClassVar[Role]
    SYSTEM: _ClassVar[Role]
    TOOL: _ClassVar[Role]
GENERATE: QueryChoiceVoteKind
SELECT: QueryChoiceVoteKind
USER: Role
ASSISTANT: Role
SYSTEM: Role
TOOL: Role

class QueryRequest(_message.Message):
    __slots__ = ("meta_model", "messages", "response_format")
    META_MODEL_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FORMAT_FIELD_NUMBER: _ClassVar[int]
    meta_model: str
    messages: _containers.RepeatedCompositeFieldContainer[Message]
    response_format: JsonSchema
    def __init__(self, meta_model: _Optional[str] = ..., messages: _Optional[_Iterable[_Union[Message, _Mapping]]] = ..., response_format: _Optional[_Union[JsonSchema, _Mapping]] = ...) -> None: ...

class QueryResponse(_message.Message):
    __slots__ = ("id", "meta_model", "choices")
    ID_FIELD_NUMBER: _ClassVar[int]
    META_MODEL_FIELD_NUMBER: _ClassVar[int]
    CHOICES_FIELD_NUMBER: _ClassVar[int]
    id: str
    meta_model: str
    choices: _containers.RepeatedCompositeFieldContainer[QueryChoice]
    def __init__(self, id: _Optional[str] = ..., meta_model: _Optional[str] = ..., choices: _Optional[_Iterable[_Union[QueryChoice, _Mapping]]] = ...) -> None: ...

class QueryStreamingResponse(_message.Message):
    __slots__ = ("id", "choice", "vote", "choice_confidence")
    ID_FIELD_NUMBER: _ClassVar[int]
    CHOICE_FIELD_NUMBER: _ClassVar[int]
    VOTE_FIELD_NUMBER: _ClassVar[int]
    CHOICE_CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    id: str
    choice: QueryChoice
    vote: QueryChoiceVote
    choice_confidence: QueryStreamingChoiceConfidence
    def __init__(self, id: _Optional[str] = ..., choice: _Optional[_Union[QueryChoice, _Mapping]] = ..., vote: _Optional[_Union[QueryChoiceVote, _Mapping]] = ..., choice_confidence: _Optional[_Union[QueryStreamingChoiceConfidence, _Mapping]] = ...) -> None: ...

class QueryStreamingChoiceConfidence(_message.Message):
    __slots__ = ("confidence",)
    class ConfidenceEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    confidence: _containers.ScalarMap[str, float]
    def __init__(self, confidence: _Optional[_Mapping[str, float]] = ...) -> None: ...

class QueryChoice(_message.Message):
    __slots__ = ("id", "message", "votes", "confidence")
    ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    VOTES_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    id: str
    message: QueryMessage
    votes: _containers.RepeatedCompositeFieldContainer[QueryChoiceVote]
    confidence: float
    def __init__(self, id: _Optional[str] = ..., message: _Optional[_Union[QueryMessage, _Mapping]] = ..., votes: _Optional[_Iterable[_Union[QueryChoiceVote, _Mapping]]] = ..., confidence: _Optional[float] = ...) -> None: ...

class QueryChoiceVote(_message.Message):
    __slots__ = ("id", "model", "provider", "kind", "reasoning", "finish_reason", "usage")
    ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    REASONING_FIELD_NUMBER: _ClassVar[int]
    FINISH_REASON_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    id: str
    model: str
    provider: _wrappers_pb2.StringValue
    kind: QueryChoiceVoteKind
    reasoning: str
    finish_reason: _wrappers_pb2.StringValue
    usage: Usage
    def __init__(self, id: _Optional[str] = ..., model: _Optional[str] = ..., provider: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., kind: _Optional[_Union[QueryChoiceVoteKind, str]] = ..., reasoning: _Optional[str] = ..., finish_reason: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., usage: _Optional[_Union[Usage, _Mapping]] = ...) -> None: ...

class QueryMessage(_message.Message):
    __slots__ = ("role", "content")
    ROLE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    role: Role
    content: _struct_pb2.Value
    def __init__(self, role: _Optional[_Union[Role, str]] = ..., content: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...

class ChatRequest(_message.Message):
    __slots__ = ("model", "messages", "tools", "tool_choice")
    MODEL_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    TOOLS_FIELD_NUMBER: _ClassVar[int]
    TOOL_CHOICE_FIELD_NUMBER: _ClassVar[int]
    model: str
    messages: _containers.RepeatedCompositeFieldContainer[Message]
    tools: _containers.RepeatedCompositeFieldContainer[Tool]
    tool_choice: ToolChoice
    def __init__(self, model: _Optional[str] = ..., messages: _Optional[_Iterable[_Union[Message, _Mapping]]] = ..., tools: _Optional[_Iterable[_Union[Tool, _Mapping]]] = ..., tool_choice: _Optional[_Union[ToolChoice, _Mapping]] = ...) -> None: ...

class ChatStreamingResponse(_message.Message):
    __slots__ = ("id", "assistant_stream", "assistant_tool_call", "query_stream", "query_message")
    ID_FIELD_NUMBER: _ClassVar[int]
    ASSISTANT_STREAM_FIELD_NUMBER: _ClassVar[int]
    ASSISTANT_TOOL_CALL_FIELD_NUMBER: _ClassVar[int]
    QUERY_STREAM_FIELD_NUMBER: _ClassVar[int]
    QUERY_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    id: str
    assistant_stream: ChatResponseSingle
    assistant_tool_call: ChatResponseSingle
    query_stream: QueryStreamingResponse
    query_message: ToolMessage
    def __init__(self, id: _Optional[str] = ..., assistant_stream: _Optional[_Union[ChatResponseSingle, _Mapping]] = ..., assistant_tool_call: _Optional[_Union[ChatResponseSingle, _Mapping]] = ..., query_stream: _Optional[_Union[QueryStreamingResponse, _Mapping]] = ..., query_message: _Optional[_Union[ToolMessage, _Mapping]] = ...) -> None: ...

class ChatResponse(_message.Message):
    __slots__ = ("id", "single", "query")
    ID_FIELD_NUMBER: _ClassVar[int]
    SINGLE_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    id: str
    single: ChatResponseSingle
    query: ChatResponseWithQuery
    def __init__(self, id: _Optional[str] = ..., single: _Optional[_Union[ChatResponseSingle, _Mapping]] = ..., query: _Optional[_Union[ChatResponseWithQuery, _Mapping]] = ...) -> None: ...

class ChatResponseWithQuery(_message.Message):
    __slots__ = ("assistant_query", "query_response", "assistant_response")
    ASSISTANT_QUERY_FIELD_NUMBER: _ClassVar[int]
    QUERY_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ASSISTANT_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    assistant_query: ChatResponseSingle
    query_response: ChatQueryResponse
    assistant_response: ChatResponseSingle
    def __init__(self, assistant_query: _Optional[_Union[ChatResponseSingle, _Mapping]] = ..., query_response: _Optional[_Union[ChatQueryResponse, _Mapping]] = ..., assistant_response: _Optional[_Union[ChatResponseSingle, _Mapping]] = ...) -> None: ...

class ChatResponseSingle(_message.Message):
    __slots__ = ("model", "choices", "usage", "provider")
    MODEL_FIELD_NUMBER: _ClassVar[int]
    CHOICES_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    model: str
    choices: _containers.RepeatedCompositeFieldContainer[ChatChoice]
    usage: Usage
    provider: _wrappers_pb2.StringValue
    def __init__(self, model: _Optional[str] = ..., choices: _Optional[_Iterable[_Union[ChatChoice, _Mapping]]] = ..., usage: _Optional[_Union[Usage, _Mapping]] = ..., provider: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...) -> None: ...

class ChatQueryResponse(_message.Message):
    __slots__ = ("query_response", "message")
    QUERY_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    query_response: QueryResponse
    message: ToolMessage
    def __init__(self, query_response: _Optional[_Union[QueryResponse, _Mapping]] = ..., message: _Optional[_Union[ToolMessage, _Mapping]] = ...) -> None: ...

class ChatChoice(_message.Message):
    __slots__ = ("index", "finish_reason", "message")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    FINISH_REASON_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    index: int
    finish_reason: _wrappers_pb2.StringValue
    message: AssistantMessage
    def __init__(self, index: _Optional[int] = ..., finish_reason: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., message: _Optional[_Union[AssistantMessage, _Mapping]] = ...) -> None: ...

class Usage(_message.Message):
    __slots__ = ("prompt_tokens", "completion_tokens")
    PROMPT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_TOKENS_FIELD_NUMBER: _ClassVar[int]
    prompt_tokens: int
    completion_tokens: int
    def __init__(self, prompt_tokens: _Optional[int] = ..., completion_tokens: _Optional[int] = ...) -> None: ...

class GenerateMessage(_message.Message):
    __slots__ = ("role", "content", "reasoning")
    ROLE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    REASONING_FIELD_NUMBER: _ClassVar[int]
    role: Role
    content: _struct_pb2.Value
    reasoning: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, role: _Optional[_Union[Role, str]] = ..., content: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ..., reasoning: _Optional[_Iterable[str]] = ...) -> None: ...

class Message(_message.Message):
    __slots__ = ("user", "assistant", "system", "tool")
    USER_FIELD_NUMBER: _ClassVar[int]
    ASSISTANT_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_FIELD_NUMBER: _ClassVar[int]
    TOOL_FIELD_NUMBER: _ClassVar[int]
    user: UserMessage
    assistant: AssistantMessage
    system: SystemMessage
    tool: ToolMessage
    def __init__(self, user: _Optional[_Union[UserMessage, _Mapping]] = ..., assistant: _Optional[_Union[AssistantMessage, _Mapping]] = ..., system: _Optional[_Union[SystemMessage, _Mapping]] = ..., tool: _Optional[_Union[ToolMessage, _Mapping]] = ...) -> None: ...

class AssistantMessage(_message.Message):
    __slots__ = ("content", "tool_calls")
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    TOOL_CALLS_FIELD_NUMBER: _ClassVar[int]
    content: MessageContent
    tool_calls: _containers.RepeatedCompositeFieldContainer[ToolCall]
    def __init__(self, content: _Optional[_Union[MessageContent, _Mapping]] = ..., tool_calls: _Optional[_Iterable[_Union[ToolCall, _Mapping]]] = ...) -> None: ...

class ToolMessage(_message.Message):
    __slots__ = ("content", "tool_call_id")
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    TOOL_CALL_ID_FIELD_NUMBER: _ClassVar[int]
    content: MessageContent
    tool_call_id: str
    def __init__(self, content: _Optional[_Union[MessageContent, _Mapping]] = ..., tool_call_id: _Optional[str] = ...) -> None: ...

class UserMessage(_message.Message):
    __slots__ = ("content",)
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    content: MessageContent
    def __init__(self, content: _Optional[_Union[MessageContent, _Mapping]] = ...) -> None: ...

class SystemMessage(_message.Message):
    __slots__ = ("content",)
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    content: MessageContent
    def __init__(self, content: _Optional[_Union[MessageContent, _Mapping]] = ...) -> None: ...

class MessageContent(_message.Message):
    __slots__ = ("text", "parts")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    PARTS_FIELD_NUMBER: _ClassVar[int]
    text: str
    parts: ContentParts
    def __init__(self, text: _Optional[str] = ..., parts: _Optional[_Union[ContentParts, _Mapping]] = ...) -> None: ...

class ToolCall(_message.Message):
    __slots__ = ("id", "function")
    ID_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    function: FunctionToolCall
    def __init__(self, id: _Optional[str] = ..., function: _Optional[_Union[FunctionToolCall, _Mapping]] = ...) -> None: ...

class FunctionToolCall(_message.Message):
    __slots__ = ("name", "arguments")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    name: str
    arguments: _struct_pb2.Value
    def __init__(self, name: _Optional[str] = ..., arguments: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...

class ContentParts(_message.Message):
    __slots__ = ("parts",)
    PARTS_FIELD_NUMBER: _ClassVar[int]
    parts: _containers.RepeatedCompositeFieldContainer[ContentPart]
    def __init__(self, parts: _Optional[_Iterable[_Union[ContentPart, _Mapping]]] = ...) -> None: ...

class ContentPart(_message.Message):
    __slots__ = ("text", "image_url")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    text: str
    image_url: ImageUrl
    def __init__(self, text: _Optional[str] = ..., image_url: _Optional[_Union[ImageUrl, _Mapping]] = ...) -> None: ...

class ImageUrl(_message.Message):
    __slots__ = ("url", "detail")
    URL_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    url: str
    detail: _wrappers_pb2.StringValue
    def __init__(self, url: _Optional[str] = ..., detail: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...) -> None: ...

class Tool(_message.Message):
    __slots__ = ("function",)
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    function: FunctionTool
    def __init__(self, function: _Optional[_Union[FunctionTool, _Mapping]] = ...) -> None: ...

class FunctionTool(_message.Message):
    __slots__ = ("name", "description", "parameters")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: _wrappers_pb2.StringValue
    parameters: _struct_pb2.Value
    def __init__(self, name: _Optional[str] = ..., description: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., parameters: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...

class ToolChoice(_message.Message):
    __slots__ = ("none", "auto", "function")
    NONE_FIELD_NUMBER: _ClassVar[int]
    AUTO_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    none: NoneToolChoice
    auto: AutoToolChoice
    function: FunctionToolChoice
    def __init__(self, none: _Optional[_Union[NoneToolChoice, _Mapping]] = ..., auto: _Optional[_Union[AutoToolChoice, _Mapping]] = ..., function: _Optional[_Union[FunctionToolChoice, _Mapping]] = ...) -> None: ...

class NoneToolChoice(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class AutoToolChoice(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FunctionToolChoice(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class JsonSchema(_message.Message):
    __slots__ = ("boolean", "number", "integer", "string", "array", "object")
    BOOLEAN_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    INTEGER_FIELD_NUMBER: _ClassVar[int]
    STRING_FIELD_NUMBER: _ClassVar[int]
    ARRAY_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    boolean: BooleanJsonSchema
    number: NumberJsonSchema
    integer: IntegerJsonSchema
    string: StringJsonSchema
    array: ArrayJsonSchema
    object: ObjectJsonSchema
    def __init__(self, boolean: _Optional[_Union[BooleanJsonSchema, _Mapping]] = ..., number: _Optional[_Union[NumberJsonSchema, _Mapping]] = ..., integer: _Optional[_Union[IntegerJsonSchema, _Mapping]] = ..., string: _Optional[_Union[StringJsonSchema, _Mapping]] = ..., array: _Optional[_Union[ArrayJsonSchema, _Mapping]] = ..., object: _Optional[_Union[ObjectJsonSchema, _Mapping]] = ...) -> None: ...

class BooleanJsonSchema(_message.Message):
    __slots__ = ("description",)
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    description: _wrappers_pb2.StringValue
    def __init__(self, description: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...) -> None: ...

class NumberJsonSchema(_message.Message):
    __slots__ = ("description",)
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    description: _wrappers_pb2.StringValue
    def __init__(self, description: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...) -> None: ...

class IntegerJsonSchema(_message.Message):
    __slots__ = ("description",)
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    description: _wrappers_pb2.StringValue
    def __init__(self, description: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...) -> None: ...

class StringJsonSchema(_message.Message):
    __slots__ = ("description", "enum")
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ENUM_FIELD_NUMBER: _ClassVar[int]
    description: _wrappers_pb2.StringValue
    enum: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, description: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., enum: _Optional[_Iterable[str]] = ...) -> None: ...

class ArrayJsonSchema(_message.Message):
    __slots__ = ("description", "items")
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    description: _wrappers_pb2.StringValue
    items: JsonSchema
    def __init__(self, description: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., items: _Optional[_Union[JsonSchema, _Mapping]] = ...) -> None: ...

class ObjectJsonSchema(_message.Message):
    __slots__ = ("description", "properties")
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    description: _wrappers_pb2.StringValue
    properties: _containers.RepeatedCompositeFieldContainer[ObjectJsonSchemaProperty]
    def __init__(self, description: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., properties: _Optional[_Iterable[_Union[ObjectJsonSchemaProperty, _Mapping]]] = ...) -> None: ...

class ObjectJsonSchemaProperty(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: JsonSchema
    def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[JsonSchema, _Mapping]] = ...) -> None: ...
