# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = [
    "RunObject",
    "IncompleteDetails",
    "LastError",
    "RequiredAction",
    "RequiredActionSubmitToolOutputs",
    "RequiredActionSubmitToolOutputsToolCall",
    "RequiredActionSubmitToolOutputsToolCallFunction",
    "ResponseFormat",
    "ResponseFormatResponseFormatText",
    "ResponseFormatResponseFormatJsonObject",
    "ResponseFormatResponseFormatJsonSchema",
    "ResponseFormatResponseFormatJsonSchemaJsonSchema",
    "ToolChoice",
    "ToolChoiceAssistantsNamedToolChoice",
    "ToolChoiceAssistantsNamedToolChoiceFunction",
    "Tool",
    "ToolAssistantToolsCode",
    "ToolAssistantToolsFileSearch",
    "ToolAssistantToolsFileSearchFileSearch",
    "ToolAssistantToolsFileSearchFileSearchRankingOptions",
    "ToolAssistantToolsFunction",
    "ToolAssistantToolsFunctionFunction",
    "TruncationStrategy",
    "Usage",
]


class IncompleteDetails(BaseModel):
    reason: Optional[Literal["max_completion_tokens", "max_prompt_tokens"]] = None
    """The reason why the run is incomplete.

    This will point to which specific token limit was reached over the course of the
    run.
    """


class LastError(BaseModel):
    code: Literal["server_error", "rate_limit_exceeded", "invalid_prompt"]
    """One of `server_error`, `rate_limit_exceeded`, or `invalid_prompt`."""

    message: str
    """A human-readable description of the error."""


class RequiredActionSubmitToolOutputsToolCallFunction(BaseModel):
    arguments: str
    """The arguments that the model expects you to pass to the function."""

    name: str
    """The name of the function."""


class RequiredActionSubmitToolOutputsToolCall(BaseModel):
    id: str
    """The ID of the tool call.

    This ID must be referenced when you submit the tool outputs in using the
    [Submit tool outputs to run](/docs/api-reference/runs/submitToolOutputs)
    endpoint.
    """

    function: RequiredActionSubmitToolOutputsToolCallFunction
    """The function definition."""

    type: Literal["function"]
    """The type of tool call the output is required for.

    For now, this is always `function`.
    """


class RequiredActionSubmitToolOutputs(BaseModel):
    tool_calls: List[RequiredActionSubmitToolOutputsToolCall]
    """A list of the relevant tool calls."""


class RequiredAction(BaseModel):
    submit_tool_outputs: RequiredActionSubmitToolOutputs
    """Details on the tool outputs needed for this run to continue."""

    type: Literal["submit_tool_outputs"]
    """For now, this is always `submit_tool_outputs`."""


class ResponseFormatResponseFormatText(BaseModel):
    type: Literal["text"]
    """The type of response format being defined: `text`"""


class ResponseFormatResponseFormatJsonObject(BaseModel):
    type: Literal["json_object"]
    """The type of response format being defined: `json_object`"""


class ResponseFormatResponseFormatJsonSchemaJsonSchema(BaseModel):
    name: str
    """The name of the response format.

    Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length
    of 64.
    """

    description: Optional[str] = None
    """
    A description of what the response format is for, used by the model to determine
    how to respond in the format.
    """

    schema_: Optional[Dict[str, object]] = FieldInfo(alias="schema", default=None)
    """The schema for the response format, described as a JSON Schema object."""

    strict: Optional[bool] = None
    """Whether to enable strict schema adherence when generating the output.

    If set to true, the model will always follow the exact schema defined in the
    `schema` field. Only a subset of JSON Schema is supported when `strict` is
    `true`. To learn more, read the
    [Structured Outputs guide](/docs/guides/structured-outputs).
    """


class ResponseFormatResponseFormatJsonSchema(BaseModel):
    json_schema: ResponseFormatResponseFormatJsonSchemaJsonSchema

    type: Literal["json_schema"]
    """The type of response format being defined: `json_schema`"""


ResponseFormat: TypeAlias = Union[
    Literal["auto"],
    ResponseFormatResponseFormatText,
    ResponseFormatResponseFormatJsonObject,
    ResponseFormatResponseFormatJsonSchema,
    None,
]


class ToolChoiceAssistantsNamedToolChoiceFunction(BaseModel):
    name: str
    """The name of the function to call."""


class ToolChoiceAssistantsNamedToolChoice(BaseModel):
    type: Literal["function", "code_interpreter", "file_search"]
    """The type of the tool. If type is `function`, the function name must be set"""

    function: Optional[ToolChoiceAssistantsNamedToolChoiceFunction] = None


ToolChoice: TypeAlias = Union[Literal["none", "auto", "required"], ToolChoiceAssistantsNamedToolChoice, None]


class ToolAssistantToolsCode(BaseModel):
    type: Literal["code_interpreter"]
    """The type of tool being defined: `code_interpreter`"""


class ToolAssistantToolsFileSearchFileSearchRankingOptions(BaseModel):
    score_threshold: float
    """The score threshold for the file search.

    All values must be a floating point number between 0 and 1.
    """

    ranker: Optional[Literal["auto", "default_2024_08_21"]] = None
    """The ranker to use for the file search.

    If not specified will use the `auto` ranker.
    """


class ToolAssistantToolsFileSearchFileSearch(BaseModel):
    max_num_results: Optional[int] = None
    """The maximum number of results the file search tool should output.

    The default is 20 for `gpt-4*` models and 5 for `gpt-3.5-turbo`. This number
    should be between 1 and 50 inclusive.

    Note that the file search tool may output fewer than `max_num_results` results.
    See the
    [file search tool documentation](/docs/assistants/tools/file-search/customizing-file-search-settings)
    for more information.
    """

    ranking_options: Optional[ToolAssistantToolsFileSearchFileSearchRankingOptions] = None
    """The ranking options for the file search.

    If not specified, the file search tool will use the `auto` ranker and a
    score_threshold of 0.

    See the
    [file search tool documentation](/docs/assistants/tools/file-search/customizing-file-search-settings)
    for more information.
    """


class ToolAssistantToolsFileSearch(BaseModel):
    type: Literal["file_search"]
    """The type of tool being defined: `file_search`"""

    file_search: Optional[ToolAssistantToolsFileSearchFileSearch] = None
    """Overrides for the file search tool."""


class ToolAssistantToolsFunctionFunction(BaseModel):
    name: str
    """The name of the function to be called.

    Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length
    of 64.
    """

    description: Optional[str] = None
    """
    A description of what the function does, used by the model to choose when and
    how to call the function.
    """

    parameters: Optional[Dict[str, object]] = None
    """The parameters the functions accepts, described as a JSON Schema object.

    See the [guide](/docs/guides/function-calling) for examples, and the
    [JSON Schema reference](https://json-schema.org/understanding-json-schema/) for
    documentation about the format.

    Omitting `parameters` defines a function with an empty parameter list.
    """

    strict: Optional[bool] = None
    """Whether to enable strict schema adherence when generating the function call.

    If set to true, the model will follow the exact schema defined in the
    `parameters` field. Only a subset of JSON Schema is supported when `strict` is
    `true`. Learn more about Structured Outputs in the
    [function calling guide](docs/guides/function-calling).
    """


class ToolAssistantToolsFunction(BaseModel):
    function: ToolAssistantToolsFunctionFunction

    type: Literal["function"]
    """The type of tool being defined: `function`"""


Tool: TypeAlias = Union[ToolAssistantToolsCode, ToolAssistantToolsFileSearch, ToolAssistantToolsFunction]


class TruncationStrategy(BaseModel):
    type: Literal["auto", "last_messages"]
    """The truncation strategy to use for the thread.

    The default is `auto`. If set to `last_messages`, the thread will be truncated
    to the n most recent messages in the thread. When set to `auto`, messages in the
    middle of the thread will be dropped to fit the context length of the model,
    `max_prompt_tokens`.
    """

    last_messages: Optional[int] = None
    """
    The number of most recent messages from the thread when constructing the context
    for the run.
    """


class Usage(BaseModel):
    completion_tokens: int
    """Number of completion tokens used over the course of the run."""

    prompt_tokens: int
    """Number of prompt tokens used over the course of the run."""

    total_tokens: int
    """Total number of tokens used (prompt + completion)."""


class RunObject(BaseModel):
    id: str
    """The identifier, which can be referenced in API endpoints."""

    assistant_id: str
    """
    The ID of the [assistant](/docs/api-reference/assistants) used for execution of
    this run.
    """

    cancelled_at: Optional[int] = None
    """The Unix timestamp (in seconds) for when the run was cancelled."""

    completed_at: Optional[int] = None
    """The Unix timestamp (in seconds) for when the run was completed."""

    created_at: int
    """The Unix timestamp (in seconds) for when the run was created."""

    expires_at: Optional[int] = None
    """The Unix timestamp (in seconds) for when the run will expire."""

    failed_at: Optional[int] = None
    """The Unix timestamp (in seconds) for when the run failed."""

    incomplete_details: Optional[IncompleteDetails] = None
    """Details on why the run is incomplete.

    Will be `null` if the run is not incomplete.
    """

    instructions: str
    """
    The instructions that the [assistant](/docs/api-reference/assistants) used for
    this run.
    """

    last_error: Optional[LastError] = None
    """The last error associated with this run. Will be `null` if there are no errors."""

    max_completion_tokens: Optional[int] = None
    """
    The maximum number of completion tokens specified to have been used over the
    course of the run.
    """

    max_prompt_tokens: Optional[int] = None
    """
    The maximum number of prompt tokens specified to have been used over the course
    of the run.
    """

    metadata: Optional[object] = None
    """Set of 16 key-value pairs that can be attached to an object.

    This can be useful for storing additional information about the object in a
    structured format. Keys can be a maximum of 64 characters long and values can be
    a maximum of 512 characters long.
    """

    model: str
    """
    The model that the [assistant](/docs/api-reference/assistants) used for this
    run.
    """

    object: Literal["thread.run"]
    """The object type, which is always `thread.run`."""

    parallel_tool_calls: bool
    """
    Whether to enable
    [parallel function calling](/docs/guides/function-calling/parallel-function-calling)
    during tool use.
    """

    required_action: Optional[RequiredAction] = None
    """Details on the action required to continue the run.

    Will be `null` if no action is required.
    """

    response_format: Optional[ResponseFormat] = None
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

    started_at: Optional[int] = None
    """The Unix timestamp (in seconds) for when the run was started."""

    status: Literal[
        "queued",
        "in_progress",
        "requires_action",
        "cancelling",
        "cancelled",
        "failed",
        "completed",
        "incomplete",
        "expired",
    ]
    """
    The status of the run, which can be either `queued`, `in_progress`,
    `requires_action`, `cancelling`, `cancelled`, `failed`, `completed`,
    `incomplete`, or `expired`.
    """

    thread_id: str
    """
    The ID of the [thread](/docs/api-reference/threads) that was executed on as a
    part of this run.
    """

    tool_choice: Optional[ToolChoice] = None
    """
    Controls which (if any) tool is called by the model. `none` means the model will
    not call any tools and instead generates a message. `auto` is the default value
    and means the model can pick between generating a message or calling one or more
    tools. `required` means the model must call one or more tools before responding
    to the user. Specifying a particular tool like `{"type": "file_search"}` or
    `{"type": "function", "function": {"name": "my_function"}}` forces the model to
    call that tool.
    """

    tools: List[Tool]
    """
    The list of tools that the [assistant](/docs/api-reference/assistants) used for
    this run.
    """

    truncation_strategy: Optional[TruncationStrategy] = None
    """Controls for how a thread will be truncated prior to the run.

    Use this to control the intial context window of the run.
    """

    usage: Optional[Usage] = None
    """Usage statistics related to the run.

    This value will be `null` if the run is not in a terminal state (i.e.
    `in_progress`, `queued`, etc.).
    """

    temperature: Optional[float] = None
    """The sampling temperature used for this run. If not set, defaults to 1."""

    top_p: Optional[float] = None
    """The nucleus sampling value used for this run. If not set, defaults to 1."""
