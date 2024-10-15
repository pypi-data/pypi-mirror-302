# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .function_call import FunctionCall
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class FunctionCallVellumValue(UniversalBaseModel):
    """
    A value representing a Function Call.
    """

    type: typing.Literal["FUNCTION_CALL"] = "FUNCTION_CALL"
    value: typing.Optional[FunctionCall] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
