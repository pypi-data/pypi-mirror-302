# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "CompletionCreateParams",
    "Message",
    "MessageChatCompletionRequestSystemMessage",
    "MessageChatCompletionRequestSystemMessageContentArrayOfContentPart",
    "MessageChatCompletionRequestUserMessage",
    "MessageChatCompletionRequestUserMessageContentArrayOfContentPart",
    "MessageChatCompletionRequestUserMessageContentArrayOfContentPartChatCompletionRequestMessageContentPartText",
    "MessageChatCompletionRequestUserMessageContentArrayOfContentPartChatCompletionRequestMessageContentPartImage",
    "MessageChatCompletionRequestUserMessageContentArrayOfContentPartChatCompletionRequestMessageContentPartImageImageURL",
    "MessageChatCompletionRequestAssistantMessage",
    "MessageChatCompletionRequestAssistantMessageContentArrayOfContentPart",
    "MessageChatCompletionRequestAssistantMessageContentArrayOfContentPartChatCompletionRequestMessageContentPartText",
    "MessageChatCompletionRequestAssistantMessageContentArrayOfContentPartChatCompletionRequestMessageContentPartRefusal",
    "MessageChatCompletionRequestAssistantMessageFunctionCall",
    "MessageChatCompletionRequestAssistantMessageToolCall",
    "MessageChatCompletionRequestAssistantMessageToolCallFunction",
    "MessageChatCompletionRequestToolMessage",
    "MessageChatCompletionRequestToolMessageContentArrayOfContentPart",
    "MessageChatCompletionRequestFunctionMessage",
    "FunctionCall",
    "FunctionCallChatCompletionFunctionCallOption",
    "Function",
    "ResponseFormat",
    "ResponseFormatResponseFormatText",
    "ResponseFormatResponseFormatJsonObject",
    "ResponseFormatResponseFormatJsonSchema",
    "ResponseFormatResponseFormatJsonSchemaJsonSchema",
    "StreamOptions",
    "ToolChoice",
    "ToolChoiceChatCompletionNamedToolChoice",
    "ToolChoiceChatCompletionNamedToolChoiceFunction",
    "Tool",
    "ToolFunction",
]


class CompletionCreateParams(TypedDict, total=False):
    messages: Required[Iterable[Message]]
    """A list of messages comprising the conversation so far.

    [Example Python code](https://cookbook.openai.com/examples/how_to_format_inputs_to_chatgpt_models).
    """

    model: Required[
        Union[
            str,
            Literal[
                "o1-preview",
                "o1-preview-2024-09-12",
                "o1-mini",
                "o1-mini-2024-09-12",
                "gpt-4o",
                "gpt-4o-2024-08-06",
                "gpt-4o-2024-05-13",
                "chatgpt-4o-latest",
                "gpt-4o-mini",
                "gpt-4o-mini-2024-07-18",
                "gpt-4-turbo",
                "gpt-4-turbo-2024-04-09",
                "gpt-4-0125-preview",
                "gpt-4-turbo-preview",
                "gpt-4-1106-preview",
                "gpt-4-vision-preview",
                "gpt-4",
                "gpt-4-0314",
                "gpt-4-0613",
                "gpt-4-32k",
                "gpt-4-32k-0314",
                "gpt-4-32k-0613",
                "gpt-3.5-turbo",
                "gpt-3.5-turbo-16k",
                "gpt-3.5-turbo-0301",
                "gpt-3.5-turbo-0613",
                "gpt-3.5-turbo-1106",
                "gpt-3.5-turbo-0125",
                "gpt-3.5-turbo-16k-0613",
            ],
        ]
    ]
    """ID of the model to use.

    See the
    [model endpoint compatibility](/docs/models/model-endpoint-compatibility) table
    for details on which models work with the Chat API.
    """

    frequency_penalty: Optional[float]
    """Number between -2.0 and 2.0.

    Positive values penalize new tokens based on their existing frequency in the
    text so far, decreasing the model's likelihood to repeat the same line verbatim.

    [See more information about frequency and presence penalties.](/docs/guides/text-generation/parameter-details)
    """

    function_call: FunctionCall
    """Deprecated in favor of `tool_choice`.

    Controls which (if any) function is called by the model. `none` means the model
    will not call a function and instead generates a message. `auto` means the model
    can pick between generating a message or calling a function. Specifying a
    particular function via `{"name": "my_function"}` forces the model to call that
    function.

    `none` is the default when no functions are present. `auto` is the default if
    functions are present.
    """

    functions: Iterable[Function]
    """Deprecated in favor of `tools`.

    A list of functions the model may generate JSON inputs for.
    """

    logit_bias: Optional[Dict[str, int]]
    """Modify the likelihood of specified tokens appearing in the completion.

    Accepts a JSON object that maps tokens (specified by their token ID in the
    tokenizer) to an associated bias value from -100 to 100. Mathematically, the
    bias is added to the logits generated by the model prior to sampling. The exact
    effect will vary per model, but values between -1 and 1 should decrease or
    increase likelihood of selection; values like -100 or 100 should result in a ban
    or exclusive selection of the relevant token.
    """

    logprobs: Optional[bool]
    """Whether to return log probabilities of the output tokens or not.

    If true, returns the log probabilities of each output token returned in the
    `content` of `message`.
    """

    max_completion_tokens: Optional[int]
    """
    An upper bound for the number of tokens that can be generated for a completion,
    including visible output tokens and [reasoning tokens](/docs/guides/reasoning).
    """

    max_tokens: Optional[int]
    """
    The maximum number of [tokens](/tokenizer) that can be generated in the chat
    completion. This value can be used to control
    [costs](https://openai.com/api/pricing/) for text generated via API.

    This value is now deprecated in favor of `max_completion_tokens`, and is not
    compatible with [o1 series models](/docs/guides/reasoning).
    """

    n: Optional[int]
    """How many chat completion choices to generate for each input message.

    Note that you will be charged based on the number of generated tokens across all
    of the choices. Keep `n` as `1` to minimize costs.
    """

    parallel_tool_calls: bool
    """
    Whether to enable
    [parallel function calling](/docs/guides/function-calling/parallel-function-calling)
    during tool use.
    """

    presence_penalty: Optional[float]
    """Number between -2.0 and 2.0.

    Positive values penalize new tokens based on whether they appear in the text so
    far, increasing the model's likelihood to talk about new topics.

    [See more information about frequency and presence penalties.](/docs/guides/text-generation/parameter-details)
    """

    response_format: ResponseFormat
    """An object specifying the format that the model must output.

    Compatible with [GPT-4o](/docs/models/gpt-4o),
    [GPT-4o mini](/docs/models/gpt-4o-mini),
    [GPT-4 Turbo](/docs/models/gpt-4-and-gpt-4-turbo) and all GPT-3.5 Turbo models
    newer than `gpt-3.5-turbo-1106`.

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

    seed: Optional[int]
    """
    This feature is in Beta. If specified, our system will make a best effort to
    sample deterministically, such that repeated requests with the same `seed` and
    parameters should return the same result. Determinism is not guaranteed, and you
    should refer to the `system_fingerprint` response parameter to monitor changes
    in the backend.
    """

    service_tier: Optional[Literal["auto", "default"]]
    """Specifies the latency tier to use for processing the request.

    This parameter is relevant for customers subscribed to the scale tier service:

    - If set to 'auto', and the Project is Scale tier enabled, the system will
      utilize scale tier credits until they are exhausted.
    - If set to 'auto', and the Project is not Scale tier enabled, the request will
      be processed using the default service tier with a lower uptime SLA and no
      latency guarentee.
    - If set to 'default', the request will be processed using the default service
      tier with a lower uptime SLA and no latency guarentee.
    - When not set, the default behavior is 'auto'.

    When this parameter is set, the response body will include the `service_tier`
    utilized.
    """

    stop: Union[Optional[str], List[str]]
    """Up to 4 sequences where the API will stop generating further tokens."""

    stream: Optional[bool]
    """If set, partial message deltas will be sent, like in ChatGPT.

    Tokens will be sent as data-only
    [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format)
    as they become available, with the stream terminated by a `data: [DONE]`
    message.
    [Example Python code](https://cookbook.openai.com/examples/how_to_stream_completions).
    """

    stream_options: Optional[StreamOptions]
    """Options for streaming response. Only set this when you set `stream: true`."""

    temperature: Optional[float]
    """What sampling temperature to use, between 0 and 2.

    Higher values like 0.8 will make the output more random, while lower values like
    0.2 will make it more focused and deterministic.

    We generally recommend altering this or `top_p` but not both.
    """

    tool_choice: ToolChoice
    """
    Controls which (if any) tool is called by the model. `none` means the model will
    not call any tool and instead generates a message. `auto` means the model can
    pick between generating a message or calling one or more tools. `required` means
    the model must call one or more tools. Specifying a particular tool via
    `{"type": "function", "function": {"name": "my_function"}}` forces the model to
    call that tool.

    `none` is the default when no tools are present. `auto` is the default if tools
    are present.
    """

    tools: Iterable[Tool]
    """A list of tools the model may call.

    Currently, only functions are supported as a tool. Use this to provide a list of
    functions the model may generate JSON inputs for. A max of 128 functions are
    supported.
    """

    top_logprobs: Optional[int]
    """
    An integer between 0 and 20 specifying the number of most likely tokens to
    return at each token position, each with an associated log probability.
    `logprobs` must be set to `true` if this parameter is used.
    """

    top_p: Optional[float]
    """
    An alternative to sampling with temperature, called nucleus sampling, where the
    model considers the results of the tokens with top_p probability mass. So 0.1
    means only the tokens comprising the top 10% probability mass are considered.

    We generally recommend altering this or `temperature` but not both.
    """

    user: str
    """
    A unique identifier representing your end-user, which can help OpenAI to monitor
    and detect abuse. [Learn more](/docs/guides/safety-best-practices/end-user-ids).
    """


class MessageChatCompletionRequestSystemMessageContentArrayOfContentPart(TypedDict, total=False):
    text: Required[str]
    """The text content."""

    type: Required[Literal["text"]]
    """The type of the content part."""


class MessageChatCompletionRequestSystemMessage(TypedDict, total=False):
    content: Required[Union[str, Iterable[MessageChatCompletionRequestSystemMessageContentArrayOfContentPart]]]
    """The contents of the system message."""

    role: Required[Literal["system"]]
    """The role of the messages author, in this case `system`."""

    name: str
    """An optional name for the participant.

    Provides the model information to differentiate between participants of the same
    role.
    """


class MessageChatCompletionRequestUserMessageContentArrayOfContentPartChatCompletionRequestMessageContentPartText(
    TypedDict, total=False
):
    text: Required[str]
    """The text content."""

    type: Required[Literal["text"]]
    """The type of the content part."""


class MessageChatCompletionRequestUserMessageContentArrayOfContentPartChatCompletionRequestMessageContentPartImageImageURL(
    TypedDict, total=False
):
    url: Required[str]
    """Either a URL of the image or the base64 encoded image data."""

    detail: Literal["auto", "low", "high"]
    """Specifies the detail level of the image.

    Learn more in the
    [Vision guide](/docs/guides/vision/low-or-high-fidelity-image-understanding).
    """


class MessageChatCompletionRequestUserMessageContentArrayOfContentPartChatCompletionRequestMessageContentPartImage(
    TypedDict, total=False
):
    image_url: Required[
        MessageChatCompletionRequestUserMessageContentArrayOfContentPartChatCompletionRequestMessageContentPartImageImageURL
    ]

    type: Required[Literal["image_url"]]
    """The type of the content part."""


MessageChatCompletionRequestUserMessageContentArrayOfContentPart: TypeAlias = Union[
    MessageChatCompletionRequestUserMessageContentArrayOfContentPartChatCompletionRequestMessageContentPartText,
    MessageChatCompletionRequestUserMessageContentArrayOfContentPartChatCompletionRequestMessageContentPartImage,
]


class MessageChatCompletionRequestUserMessage(TypedDict, total=False):
    content: Required[Union[str, Iterable[MessageChatCompletionRequestUserMessageContentArrayOfContentPart]]]
    """The contents of the user message."""

    role: Required[Literal["user"]]
    """The role of the messages author, in this case `user`."""

    name: str
    """An optional name for the participant.

    Provides the model information to differentiate between participants of the same
    role.
    """


class MessageChatCompletionRequestAssistantMessageContentArrayOfContentPartChatCompletionRequestMessageContentPartText(
    TypedDict, total=False
):
    text: Required[str]
    """The text content."""

    type: Required[Literal["text"]]
    """The type of the content part."""


class MessageChatCompletionRequestAssistantMessageContentArrayOfContentPartChatCompletionRequestMessageContentPartRefusal(
    TypedDict, total=False
):
    refusal: Required[str]
    """The refusal message generated by the model."""

    type: Required[Literal["refusal"]]
    """The type of the content part."""


MessageChatCompletionRequestAssistantMessageContentArrayOfContentPart: TypeAlias = Union[
    MessageChatCompletionRequestAssistantMessageContentArrayOfContentPartChatCompletionRequestMessageContentPartText,
    MessageChatCompletionRequestAssistantMessageContentArrayOfContentPartChatCompletionRequestMessageContentPartRefusal,
]


class MessageChatCompletionRequestAssistantMessageFunctionCall(TypedDict, total=False):
    arguments: Required[str]
    """
    The arguments to call the function with, as generated by the model in JSON
    format. Note that the model does not always generate valid JSON, and may
    hallucinate parameters not defined by your function schema. Validate the
    arguments in your code before calling your function.
    """

    name: Required[str]
    """The name of the function to call."""


class MessageChatCompletionRequestAssistantMessageToolCallFunction(TypedDict, total=False):
    arguments: Required[str]
    """
    The arguments to call the function with, as generated by the model in JSON
    format. Note that the model does not always generate valid JSON, and may
    hallucinate parameters not defined by your function schema. Validate the
    arguments in your code before calling your function.
    """

    name: Required[str]
    """The name of the function to call."""


class MessageChatCompletionRequestAssistantMessageToolCall(TypedDict, total=False):
    id: Required[str]
    """The ID of the tool call."""

    function: Required[MessageChatCompletionRequestAssistantMessageToolCallFunction]
    """The function that the model called."""

    type: Required[Literal["function"]]
    """The type of the tool. Currently, only `function` is supported."""


class MessageChatCompletionRequestAssistantMessage(TypedDict, total=False):
    role: Required[Literal["assistant"]]
    """The role of the messages author, in this case `assistant`."""

    content: Union[str, Iterable[MessageChatCompletionRequestAssistantMessageContentArrayOfContentPart], None]
    """The contents of the assistant message.

    Required unless `tool_calls` or `function_call` is specified.
    """

    function_call: Optional[MessageChatCompletionRequestAssistantMessageFunctionCall]
    """Deprecated and replaced by `tool_calls`.

    The name and arguments of a function that should be called, as generated by the
    model.
    """

    name: str
    """An optional name for the participant.

    Provides the model information to differentiate between participants of the same
    role.
    """

    refusal: Optional[str]
    """The refusal message by the assistant."""

    tool_calls: Iterable[MessageChatCompletionRequestAssistantMessageToolCall]
    """The tool calls generated by the model, such as function calls."""


class MessageChatCompletionRequestToolMessageContentArrayOfContentPart(TypedDict, total=False):
    text: Required[str]
    """The text content."""

    type: Required[Literal["text"]]
    """The type of the content part."""


class MessageChatCompletionRequestToolMessage(TypedDict, total=False):
    content: Required[Union[str, Iterable[MessageChatCompletionRequestToolMessageContentArrayOfContentPart]]]
    """The contents of the tool message."""

    role: Required[Literal["tool"]]
    """The role of the messages author, in this case `tool`."""

    tool_call_id: Required[str]
    """Tool call that this message is responding to."""


class MessageChatCompletionRequestFunctionMessage(TypedDict, total=False):
    content: Required[Optional[str]]
    """The contents of the function message."""

    name: Required[str]
    """The name of the function to call."""

    role: Required[Literal["function"]]
    """The role of the messages author, in this case `function`."""


Message: TypeAlias = Union[
    MessageChatCompletionRequestSystemMessage,
    MessageChatCompletionRequestUserMessage,
    MessageChatCompletionRequestAssistantMessage,
    MessageChatCompletionRequestToolMessage,
    MessageChatCompletionRequestFunctionMessage,
]


class FunctionCallChatCompletionFunctionCallOption(TypedDict, total=False):
    name: Required[str]
    """The name of the function to call."""


FunctionCall: TypeAlias = Union[Literal["none", "auto"], FunctionCallChatCompletionFunctionCallOption]


class Function(TypedDict, total=False):
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
    ResponseFormatResponseFormatText, ResponseFormatResponseFormatJsonObject, ResponseFormatResponseFormatJsonSchema
]


class StreamOptions(TypedDict, total=False):
    include_usage: bool
    """If set, an additional chunk will be streamed before the `data: [DONE]` message.

    The `usage` field on this chunk shows the token usage statistics for the entire
    request, and the `choices` field will always be an empty array. All other chunks
    will also include a `usage` field, but with a null value.
    """


class ToolChoiceChatCompletionNamedToolChoiceFunction(TypedDict, total=False):
    name: Required[str]
    """The name of the function to call."""


class ToolChoiceChatCompletionNamedToolChoice(TypedDict, total=False):
    function: Required[ToolChoiceChatCompletionNamedToolChoiceFunction]

    type: Required[Literal["function"]]
    """The type of the tool. Currently, only `function` is supported."""


ToolChoice: TypeAlias = Union[Literal["none", "auto", "required"], ToolChoiceChatCompletionNamedToolChoice]


class ToolFunction(TypedDict, total=False):
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


class Tool(TypedDict, total=False):
    function: Required[ToolFunction]

    type: Required[Literal["function"]]
    """The type of the tool. Currently, only `function` is supported."""
