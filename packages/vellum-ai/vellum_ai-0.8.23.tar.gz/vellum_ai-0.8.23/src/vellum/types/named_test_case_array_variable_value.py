# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations
from ..core.pydantic_utilities import UniversalBaseModel
from .array_vellum_value import ArrayVellumValue
import typing
from .array_vellum_value_item import ArrayVellumValueItem
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic
from ..core.pydantic_utilities import update_forward_refs


class NamedTestCaseArrayVariableValue(UniversalBaseModel):
    """
    Named Test Case value that is of type ARRAY
    """

    type: typing.Literal["ARRAY"] = "ARRAY"
    value: typing.Optional[typing.List[ArrayVellumValueItem]] = None
    name: str

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


update_forward_refs(ArrayVellumValue, NamedTestCaseArrayVariableValue=NamedTestCaseArrayVariableValue)
