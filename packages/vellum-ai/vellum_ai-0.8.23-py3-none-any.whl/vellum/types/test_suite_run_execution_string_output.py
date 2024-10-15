# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class TestSuiteRunExecutionStringOutput(UniversalBaseModel):
    """
    Execution output of an entity evaluated during a Test Suite Run that is of type STRING
    """

    name: str
    type: typing.Literal["STRING"] = "STRING"
    value: typing.Optional[str] = None
    output_variable_id: str

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
