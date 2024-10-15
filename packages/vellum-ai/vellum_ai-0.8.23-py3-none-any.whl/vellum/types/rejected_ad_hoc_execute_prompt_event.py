# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .vellum_error import VellumError
from .ad_hoc_rejected_prompt_execution_meta import AdHocRejectedPromptExecutionMeta
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class RejectedAdHocExecutePromptEvent(UniversalBaseModel):
    """
    The final data returned indicating an error occurred during the stream.
    """

    state: typing.Literal["REJECTED"] = "REJECTED"
    error: VellumError
    execution_id: str
    meta: typing.Optional[AdHocRejectedPromptExecutionMeta] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
