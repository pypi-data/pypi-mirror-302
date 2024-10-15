# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class WorkflowExecutionActualStringRequest(UniversalBaseModel):
    output_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    The Vellum-generated ID of a workflow output. Must provide either this or output_key. output_key is typically preferred.
    """

    output_key: typing.Optional[str] = pydantic.Field(default=None)
    """
    The user-defined name of a workflow output. Must provide either this or output_id. Should correspond to the `Name` specified in a Final Output Node. Generally preferred over output_id.
    """

    quality: typing.Optional[float] = pydantic.Field(default=None)
    """
    Optionally provide a decimal number between 0.0 and 1.0 (inclusive) representing the quality of the output. 0 is the worst, 1 is the best.
    """

    metadata: typing.Optional[typing.Dict[str, typing.Optional[typing.Any]]] = pydantic.Field(default=None)
    """
    Optionally provide additional metadata about the feedback submission.
    """

    timestamp: typing.Optional[float] = pydantic.Field(default=None)
    """
    Optionally provide the timestamp representing when this feedback was collected. Used for reporting purposes.
    """

    output_type: typing.Literal["STRING"] = "STRING"
    desired_output_value: typing.Optional[str] = pydantic.Field(default=None)
    """
    Optionally provide the value that the output ideally should have been.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
