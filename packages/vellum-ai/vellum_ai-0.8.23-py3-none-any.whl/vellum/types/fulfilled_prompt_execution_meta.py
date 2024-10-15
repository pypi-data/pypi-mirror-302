# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .finish_reason_enum import FinishReasonEnum
from .ml_model_usage import MlModelUsage
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class FulfilledPromptExecutionMeta(UniversalBaseModel):
    """
    The subset of the metadata tracked by Vellum during prompt execution that the request opted into with `expand_meta`.
    """

    latency: typing.Optional[int] = None
    finish_reason: typing.Optional[FinishReasonEnum] = None
    usage: typing.Optional[MlModelUsage] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
