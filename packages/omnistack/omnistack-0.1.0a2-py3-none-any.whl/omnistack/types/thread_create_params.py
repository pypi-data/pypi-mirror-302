# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "ThreadCreateParams",
    "Message",
    "MessageContentArrayOfContentPart",
    "MessageContentArrayOfContentPartMessageContentImageFileObject",
    "MessageContentArrayOfContentPartMessageContentImageFileObjectImageFile",
    "MessageContentArrayOfContentPartMessageContentImageURLObject",
    "MessageContentArrayOfContentPartMessageContentImageURLObjectImageURL",
    "MessageContentArrayOfContentPartMessageRequestContentTextObject",
    "MessageAttachment",
    "MessageAttachmentTool",
    "MessageAttachmentToolAssistantToolsCode",
    "MessageAttachmentToolAssistantToolsFileSearchTypeOnly",
    "ToolResources",
    "ToolResourcesCodeInterpreter",
    "ToolResourcesFileSearch",
    "ToolResourcesFileSearchUnionMember0",
    "ToolResourcesFileSearchUnionMember0VectorStore",
    "ToolResourcesFileSearchUnionMember0VectorStoreChunkingStrategy",
    "ToolResourcesFileSearchUnionMember0VectorStoreChunkingStrategyAutoChunkingStrategy",
    "ToolResourcesFileSearchUnionMember0VectorStoreChunkingStrategyStaticChunkingStrategy",
    "ToolResourcesFileSearchUnionMember0VectorStoreChunkingStrategyStaticChunkingStrategyStatic",
    "ToolResourcesFileSearchUnionMember1",
    "ToolResourcesFileSearchUnionMember1VectorStore",
    "ToolResourcesFileSearchUnionMember1VectorStoreChunkingStrategy",
    "ToolResourcesFileSearchUnionMember1VectorStoreChunkingStrategyAutoChunkingStrategy",
    "ToolResourcesFileSearchUnionMember1VectorStoreChunkingStrategyStaticChunkingStrategy",
    "ToolResourcesFileSearchUnionMember1VectorStoreChunkingStrategyStaticChunkingStrategyStatic",
]


class ThreadCreateParams(TypedDict, total=False):
    messages: Iterable[Message]
    """A list of [messages](/docs/api-reference/messages) to start the thread with."""

    metadata: Optional[object]
    """Set of 16 key-value pairs that can be attached to an object.

    This can be useful for storing additional information about the object in a
    structured format. Keys can be a maximum of 64 characters long and values can be
    a maximum of 512 characters long.
    """

    tool_resources: Optional[ToolResources]
    """
    A set of resources that are made available to the assistant's tools in this
    thread. The resources are specific to the type of tool. For example, the
    `code_interpreter` tool requires a list of file IDs, while the `file_search`
    tool requires a list of vector store IDs.
    """


class MessageContentArrayOfContentPartMessageContentImageFileObjectImageFile(TypedDict, total=False):
    file_id: Required[str]
    """The [File](/docs/api-reference/files) ID of the image in the message content.

    Set `purpose="vision"` when uploading the File if you need to later display the
    file content.
    """

    detail: Literal["auto", "low", "high"]
    """Specifies the detail level of the image if specified by the user.

    `low` uses fewer tokens, you can opt in to high resolution using `high`.
    """


class MessageContentArrayOfContentPartMessageContentImageFileObject(TypedDict, total=False):
    image_file: Required[MessageContentArrayOfContentPartMessageContentImageFileObjectImageFile]

    type: Required[Literal["image_file"]]
    """Always `image_file`."""


class MessageContentArrayOfContentPartMessageContentImageURLObjectImageURL(TypedDict, total=False):
    url: Required[str]
    """
    The external URL of the image, must be a supported image types: jpeg, jpg, png,
    gif, webp.
    """

    detail: Literal["auto", "low", "high"]
    """Specifies the detail level of the image.

    `low` uses fewer tokens, you can opt in to high resolution using `high`. Default
    value is `auto`
    """


class MessageContentArrayOfContentPartMessageContentImageURLObject(TypedDict, total=False):
    image_url: Required[MessageContentArrayOfContentPartMessageContentImageURLObjectImageURL]

    type: Required[Literal["image_url"]]
    """The type of the content part."""


class MessageContentArrayOfContentPartMessageRequestContentTextObject(TypedDict, total=False):
    text: Required[str]
    """Text content to be sent to the model"""

    type: Required[Literal["text"]]
    """Always `text`."""


MessageContentArrayOfContentPart: TypeAlias = Union[
    MessageContentArrayOfContentPartMessageContentImageFileObject,
    MessageContentArrayOfContentPartMessageContentImageURLObject,
    MessageContentArrayOfContentPartMessageRequestContentTextObject,
]


class MessageAttachmentToolAssistantToolsCode(TypedDict, total=False):
    type: Required[Literal["code_interpreter"]]
    """The type of tool being defined: `code_interpreter`"""


class MessageAttachmentToolAssistantToolsFileSearchTypeOnly(TypedDict, total=False):
    type: Required[Literal["file_search"]]
    """The type of tool being defined: `file_search`"""


MessageAttachmentTool: TypeAlias = Union[
    MessageAttachmentToolAssistantToolsCode, MessageAttachmentToolAssistantToolsFileSearchTypeOnly
]


class MessageAttachment(TypedDict, total=False):
    file_id: str
    """The ID of the file to attach to the message."""

    tools: Iterable[MessageAttachmentTool]
    """The tools to add this file to."""


class Message(TypedDict, total=False):
    content: Required[Union[str, Iterable[MessageContentArrayOfContentPart]]]
    """The text contents of the message."""

    role: Required[Literal["user", "assistant"]]
    """The role of the entity that is creating the message. Allowed values include:

    - `user`: Indicates the message is sent by an actual user and should be used in
      most cases to represent user-generated messages.
    - `assistant`: Indicates the message is generated by the assistant. Use this
      value to insert messages from the assistant into the conversation.
    """

    attachments: Optional[Iterable[MessageAttachment]]
    """A list of files attached to the message, and the tools they should be added to."""

    metadata: Optional[object]
    """Set of 16 key-value pairs that can be attached to an object.

    This can be useful for storing additional information about the object in a
    structured format. Keys can be a maximum of 64 characters long and values can be
    a maximum of 512 characters long.
    """


class ToolResourcesCodeInterpreter(TypedDict, total=False):
    file_ids: List[str]
    """
    A list of [file](/docs/api-reference/files) IDs made available to the
    `code_interpreter` tool. There can be a maximum of 20 files associated with the
    tool.
    """


class ToolResourcesFileSearchUnionMember0VectorStoreChunkingStrategyAutoChunkingStrategy(TypedDict, total=False):
    type: Required[Literal["auto"]]
    """Always `auto`."""


class ToolResourcesFileSearchUnionMember0VectorStoreChunkingStrategyStaticChunkingStrategyStatic(
    TypedDict, total=False
):
    chunk_overlap_tokens: Required[int]
    """The number of tokens that overlap between chunks. The default value is `400`.

    Note that the overlap must not exceed half of `max_chunk_size_tokens`.
    """

    max_chunk_size_tokens: Required[int]
    """The maximum number of tokens in each chunk.

    The default value is `800`. The minimum value is `100` and the maximum value is
    `4096`.
    """


class ToolResourcesFileSearchUnionMember0VectorStoreChunkingStrategyStaticChunkingStrategy(TypedDict, total=False):
    static: Required[ToolResourcesFileSearchUnionMember0VectorStoreChunkingStrategyStaticChunkingStrategyStatic]

    type: Required[Literal["static"]]
    """Always `static`."""


ToolResourcesFileSearchUnionMember0VectorStoreChunkingStrategy: TypeAlias = Union[
    ToolResourcesFileSearchUnionMember0VectorStoreChunkingStrategyAutoChunkingStrategy,
    ToolResourcesFileSearchUnionMember0VectorStoreChunkingStrategyStaticChunkingStrategy,
]


class ToolResourcesFileSearchUnionMember0VectorStore(TypedDict, total=False):
    chunking_strategy: ToolResourcesFileSearchUnionMember0VectorStoreChunkingStrategy
    """The chunking strategy used to chunk the file(s).

    If not set, will use the `auto` strategy.
    """

    file_ids: List[str]
    """A list of [file](/docs/api-reference/files) IDs to add to the vector store.

    There can be a maximum of 10000 files in a vector store.
    """

    metadata: object
    """Set of 16 key-value pairs that can be attached to a vector store.

    This can be useful for storing additional information about the vector store in
    a structured format. Keys can be a maximum of 64 characters long and values can
    be a maximum of 512 characters long.
    """


class ToolResourcesFileSearchUnionMember0(TypedDict, total=False):
    vector_store_ids: Required[List[str]]
    """
    The [vector store](/docs/api-reference/vector-stores/object) attached to this
    thread. There can be a maximum of 1 vector store attached to the thread.
    """

    vector_stores: Iterable[ToolResourcesFileSearchUnionMember0VectorStore]
    """
    A helper to create a [vector store](/docs/api-reference/vector-stores/object)
    with file_ids and attach it to this thread. There can be a maximum of 1 vector
    store attached to the thread.
    """


class ToolResourcesFileSearchUnionMember1VectorStoreChunkingStrategyAutoChunkingStrategy(TypedDict, total=False):
    type: Required[Literal["auto"]]
    """Always `auto`."""


class ToolResourcesFileSearchUnionMember1VectorStoreChunkingStrategyStaticChunkingStrategyStatic(
    TypedDict, total=False
):
    chunk_overlap_tokens: Required[int]
    """The number of tokens that overlap between chunks. The default value is `400`.

    Note that the overlap must not exceed half of `max_chunk_size_tokens`.
    """

    max_chunk_size_tokens: Required[int]
    """The maximum number of tokens in each chunk.

    The default value is `800`. The minimum value is `100` and the maximum value is
    `4096`.
    """


class ToolResourcesFileSearchUnionMember1VectorStoreChunkingStrategyStaticChunkingStrategy(TypedDict, total=False):
    static: Required[ToolResourcesFileSearchUnionMember1VectorStoreChunkingStrategyStaticChunkingStrategyStatic]

    type: Required[Literal["static"]]
    """Always `static`."""


ToolResourcesFileSearchUnionMember1VectorStoreChunkingStrategy: TypeAlias = Union[
    ToolResourcesFileSearchUnionMember1VectorStoreChunkingStrategyAutoChunkingStrategy,
    ToolResourcesFileSearchUnionMember1VectorStoreChunkingStrategyStaticChunkingStrategy,
]


class ToolResourcesFileSearchUnionMember1VectorStore(TypedDict, total=False):
    chunking_strategy: ToolResourcesFileSearchUnionMember1VectorStoreChunkingStrategy
    """The chunking strategy used to chunk the file(s).

    If not set, will use the `auto` strategy.
    """

    file_ids: List[str]
    """A list of [file](/docs/api-reference/files) IDs to add to the vector store.

    There can be a maximum of 10000 files in a vector store.
    """

    metadata: object
    """Set of 16 key-value pairs that can be attached to a vector store.

    This can be useful for storing additional information about the vector store in
    a structured format. Keys can be a maximum of 64 characters long and values can
    be a maximum of 512 characters long.
    """


class ToolResourcesFileSearchUnionMember1(TypedDict, total=False):
    vector_stores: Required[Iterable[ToolResourcesFileSearchUnionMember1VectorStore]]
    """
    A helper to create a [vector store](/docs/api-reference/vector-stores/object)
    with file_ids and attach it to this thread. There can be a maximum of 1 vector
    store attached to the thread.
    """

    vector_store_ids: List[str]
    """
    The [vector store](/docs/api-reference/vector-stores/object) attached to this
    thread. There can be a maximum of 1 vector store attached to the thread.
    """


ToolResourcesFileSearch: TypeAlias = Union[ToolResourcesFileSearchUnionMember0, ToolResourcesFileSearchUnionMember1]


class ToolResources(TypedDict, total=False):
    code_interpreter: ToolResourcesCodeInterpreter

    file_search: ToolResourcesFileSearch
