# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["FineTuningJob", "Error", "Hyperparameters", "Integration", "IntegrationWandb"]


class Error(BaseModel):
    code: str
    """A machine-readable error code."""

    message: str
    """A human-readable error message."""

    param: Optional[str] = None
    """The parameter that was invalid, usually `training_file` or `validation_file`.

    This field will be null if the failure was not parameter-specific.
    """


class Hyperparameters(BaseModel):
    n_epochs: Union[Literal["auto"], int]
    """The number of epochs to train the model for.

    An epoch refers to one full cycle through the training dataset. "auto" decides
    the optimal number of epochs based on the size of the dataset. If setting the
    number manually, we support any number between 1 and 50 epochs.
    """


class IntegrationWandb(BaseModel):
    project: str
    """The name of the project that the new run will be created under."""

    entity: Optional[str] = None
    """The entity to use for the run.

    This allows you to set the team or username of the WandB user that you would
    like associated with the run. If not set, the default entity for the registered
    WandB API key is used.
    """

    name: Optional[str] = None
    """A display name to set for the run.

    If not set, we will use the Job ID as the name.
    """

    tags: Optional[List[str]] = None
    """A list of tags to be attached to the newly created run.

    These tags are passed through directly to WandB. Some default tags are generated
    by OpenAI: "openai/finetune", "openai/{base-model}", "openai/{ftjob-abcdef}".
    """


class Integration(BaseModel):
    type: Literal["wandb"]
    """The type of the integration being enabled for the fine-tuning job"""

    wandb: IntegrationWandb
    """The settings for your integration with Weights and Biases.

    This payload specifies the project that metrics will be sent to. Optionally, you
    can set an explicit display name for your run, add tags to your run, and set a
    default entity (team, username, etc) to be associated with your run.
    """


class FineTuningJob(BaseModel):
    id: str
    """The object identifier, which can be referenced in the API endpoints."""

    created_at: int
    """The Unix timestamp (in seconds) for when the fine-tuning job was created."""

    error: Optional[Error] = None
    """
    For fine-tuning jobs that have `failed`, this will contain more information on
    the cause of the failure.
    """

    fine_tuned_model: Optional[str] = None
    """The name of the fine-tuned model that is being created.

    The value will be null if the fine-tuning job is still running.
    """

    finished_at: Optional[int] = None
    """The Unix timestamp (in seconds) for when the fine-tuning job was finished.

    The value will be null if the fine-tuning job is still running.
    """

    hyperparameters: Hyperparameters
    """The hyperparameters used for the fine-tuning job.

    See the [fine-tuning guide](/docs/guides/fine-tuning) for more details.
    """

    model: str
    """The base model that is being fine-tuned."""

    object: Literal["fine_tuning.job"]
    """The object type, which is always "fine_tuning.job"."""

    organization_id: str
    """The organization that owns the fine-tuning job."""

    result_files: List[str]
    """The compiled results file ID(s) for the fine-tuning job.

    You can retrieve the results with the
    [Files API](/docs/api-reference/files/retrieve-contents).
    """

    seed: int
    """The seed used for the fine-tuning job."""

    status: Literal["validating_files", "queued", "running", "succeeded", "failed", "cancelled"]
    """
    The current status of the fine-tuning job, which can be either
    `validating_files`, `queued`, `running`, `succeeded`, `failed`, or `cancelled`.
    """

    trained_tokens: Optional[int] = None
    """The total number of billable tokens processed by this fine-tuning job.

    The value will be null if the fine-tuning job is still running.
    """

    training_file: str
    """The file ID used for training.

    You can retrieve the training data with the
    [Files API](/docs/api-reference/files/retrieve-contents).
    """

    validation_file: Optional[str] = None
    """The file ID used for validation.

    You can retrieve the validation results with the
    [Files API](/docs/api-reference/files/retrieve-contents).
    """

    estimated_finish: Optional[int] = None
    """
    The Unix timestamp (in seconds) for when the fine-tuning job is estimated to
    finish. The value will be null if the fine-tuning job is not running.
    """

    integrations: Optional[List[Integration]] = None
    """A list of integrations to enable for this fine-tuning job."""
