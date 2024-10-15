# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .search_result_request import SearchResultRequest
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class NamedTestCaseSearchResultsVariableValueRequest(UniversalBaseModel):
    """
    Named Test Case value that is of type SEARCH_RESULTS
    """

    type: typing.Literal["SEARCH_RESULTS"] = "SEARCH_RESULTS"
    value: typing.Optional[typing.List[SearchResultRequest]] = None
    name: str

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
