# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "AssistantCreateParams",
    "ResponseFormat",
    "ResponseFormatResponseFormatText",
    "ResponseFormatResponseFormatJsonObject",
    "ResponseFormatResponseFormatJsonSchema",
    "ResponseFormatResponseFormatJsonSchemaJsonSchema",
    "ToolResources",
    "ToolResourcesCodeInterpreter",
    "ToolResourcesFileSearch",
    "Tool",
    "ToolAssistantToolsCode",
    "ToolAssistantToolsFileSearch",
    "ToolAssistantToolsFileSearchFileSearch",
    "ToolAssistantToolsFileSearchFileSearchRankingOptions",
    "ToolAssistantToolsFunction",
    "ToolAssistantToolsFunctionFunction",
]


class AssistantCreateParams(TypedDict, total=False):
    description: Optional[str]
    """The description of the assistant. The maximum length is 512 characters."""

    instructions: Optional[str]
    """The system instructions that the assistant uses.

    The maximum length is 256,000 characters.
    """

    metadata: Optional[object]
    """Set of 16 key-value pairs that can be attached to an object.

    This can be useful for storing additional information about the object in a
    structured format. Keys can be a maximum of 64 characters long and values can be
    a maximum of 512 characters long.
    """

    model: str
    """ID of the model to use.

    You can use the [List models](/docs/api-reference/models/list) API to see all of
    your available models, or see our [Model overview](/docs/models/overview) for
    descriptions of them.
    """

    name: Optional[str]
    """The name of the assistant. The maximum length is 256 characters."""

    response_format: Optional[ResponseFormat]
    """Specifies the format that the model must output.

    Compatible with [GPT-4o](/docs/models/gpt-4o),
    [GPT-4 Turbo](/docs/models/gpt-4-turbo-and-gpt-4), and all GPT-3.5 Turbo models
    since `gpt-3.5-turbo-1106`.

    Setting to `{ "type": "json_schema", "json_schema": {...} }` enables Structured
    Outputs which ensures the model will match your supplied JSON schema. Learn more
    in the [Structured Outputs guide](/docs/guides/structured-outputs).

    Setting to `{ "type": "json_object" }` enables JSON mode, which ensures the
    message the model generates is valid JSON.

    **Important:** when using JSON mode, you **must** also instruct the model to
    produce JSON yourself via a system or user message. Without this, the model may
    generate an unending stream of whitespace until the generation reaches the token
    limit, resulting in a long-running and seemingly "stuck" request. Also note that
    the message content may be partially cut off if `finish_reason="length"`, which
    indicates the generation exceeded `max_tokens` or the conversation exceeded the
    max context length.
    """

    temperature: Optional[float]
    """What sampling temperature to use, between 0 and 2.

    Higher values like 0.8 will make the output more random, while lower values like
    0.2 will make it more focused and deterministic.
    """

    tool_resources: Optional[ToolResources]
    """A set of resources that are used by the assistant's tools.

    The resources are specific to the type of tool. For example, the
    `code_interpreter` tool requires a list of file IDs, while the `file_search`
    tool requires a list of vector store IDs.
    """

    tools: Iterable[Tool]
    """A list of tool enabled on the assistant.

    There can be a maximum of 128 tools per assistant. Tools can be of types
    `code_interpreter`, `file_search`, or `function`.
    """

    top_p: Optional[float]
    """
    An alternative to sampling with temperature, called nucleus sampling, where the
    model considers the results of the tokens with top_p probability mass. So 0.1
    means only the tokens comprising the top 10% probability mass are considered.

    We generally recommend altering this or temperature but not both.
    """


class ResponseFormatResponseFormatText(TypedDict, total=False):
    type: Required[Literal["text"]]
    """The type of response format being defined: `text`"""


class ResponseFormatResponseFormatJsonObject(TypedDict, total=False):
    type: Required[Literal["json_object"]]
    """The type of response format being defined: `json_object`"""


class ResponseFormatResponseFormatJsonSchemaJsonSchema(TypedDict, total=False):
    name: Required[str]
    """The name of the response format.

    Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length
    of 64.
    """

    description: str
    """
    A description of what the response format is for, used by the model to determine
    how to respond in the format.
    """

    schema: Dict[str, object]
    """The schema for the response format, described as a JSON Schema object."""

    strict: Optional[bool]
    """Whether to enable strict schema adherence when generating the output.

    If set to true, the model will always follow the exact schema defined in the
    `schema` field. Only a subset of JSON Schema is supported when `strict` is
    `true`. To learn more, read the
    [Structured Outputs guide](/docs/guides/structured-outputs).
    """


class ResponseFormatResponseFormatJsonSchema(TypedDict, total=False):
    json_schema: Required[ResponseFormatResponseFormatJsonSchemaJsonSchema]

    type: Required[Literal["json_schema"]]
    """The type of response format being defined: `json_schema`"""


ResponseFormat: TypeAlias = Union[
    Literal["auto"],
    ResponseFormatResponseFormatText,
    ResponseFormatResponseFormatJsonObject,
    ResponseFormatResponseFormatJsonSchema,
]


class ToolResourcesCodeInterpreter(TypedDict, total=False):
    file_ids: List[str]
    """
    Overrides the list of [file](/docs/api-reference/files) IDs made available to
    the `code_interpreter` tool. There can be a maximum of 20 files associated with
    the tool.
    """


class ToolResourcesFileSearch(TypedDict, total=False):
    vector_store_ids: List[str]
    """
    Overrides the [vector store](/docs/api-reference/vector-stores/object) attached
    to this assistant. There can be a maximum of 1 vector store attached to the
    assistant.
    """


class ToolResources(TypedDict, total=False):
    code_interpreter: ToolResourcesCodeInterpreter

    file_search: ToolResourcesFileSearch


class ToolAssistantToolsCode(TypedDict, total=False):
    type: Required[Literal["code_interpreter"]]
    """The type of tool being defined: `code_interpreter`"""


class ToolAssistantToolsFileSearchFileSearchRankingOptions(TypedDict, total=False):
    score_threshold: Required[float]
    """The score threshold for the file search.

    All values must be a floating point number between 0 and 1.
    """

    ranker: Literal["auto", "default_2024_08_21"]
    """The ranker to use for the file search.

    If not specified will use the `auto` ranker.
    """


class ToolAssistantToolsFileSearchFileSearch(TypedDict, total=False):
    max_num_results: int
    """The maximum number of results the file search tool should output.

    The default is 20 for `gpt-4*` models and 5 for `gpt-3.5-turbo`. This number
    should be between 1 and 50 inclusive.

    Note that the file search tool may output fewer than `max_num_results` results.
    See the
    [file search tool documentation](/docs/assistants/tools/file-search/customizing-file-search-settings)
    for more information.
    """

    ranking_options: ToolAssistantToolsFileSearchFileSearchRankingOptions
    """The ranking options for the file search.

    If not specified, the file search tool will use the `auto` ranker and a
    score_threshold of 0.

    See the
    [file search tool documentation](/docs/assistants/tools/file-search/customizing-file-search-settings)
    for more information.
    """


class ToolAssistantToolsFileSearch(TypedDict, total=False):
    type: Required[Literal["file_search"]]
    """The type of tool being defined: `file_search`"""

    file_search: ToolAssistantToolsFileSearchFileSearch
    """Overrides for the file search tool."""


class ToolAssistantToolsFunctionFunction(TypedDict, total=False):
    name: Required[str]
    """The name of the function to be called.

    Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length
    of 64.
    """

    description: str
    """
    A description of what the function does, used by the model to choose when and
    how to call the function.
    """

    parameters: Dict[str, object]
    """The parameters the functions accepts, described as a JSON Schema object.

    See the [guide](/docs/guides/function-calling) for examples, and the
    [JSON Schema reference](https://json-schema.org/understanding-json-schema/) for
    documentation about the format.

    Omitting `parameters` defines a function with an empty parameter list.
    """

    strict: Optional[bool]
    """Whether to enable strict schema adherence when generating the function call.

    If set to true, the model will follow the exact schema defined in the
    `parameters` field. Only a subset of JSON Schema is supported when `strict` is
    `true`. Learn more about Structured Outputs in the
    [function calling guide](docs/guides/function-calling).
    """


class ToolAssistantToolsFunction(TypedDict, total=False):
    function: Required[ToolAssistantToolsFunctionFunction]

    type: Required[Literal["function"]]
    """The type of tool being defined: `function`"""


Tool: TypeAlias = Union[ToolAssistantToolsCode, ToolAssistantToolsFileSearch, ToolAssistantToolsFunction]
