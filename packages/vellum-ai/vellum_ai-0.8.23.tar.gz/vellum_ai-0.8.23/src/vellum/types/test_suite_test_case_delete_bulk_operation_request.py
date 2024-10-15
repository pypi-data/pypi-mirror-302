# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import pydantic
import typing
from .test_suite_test_case_delete_bulk_operation_data_request import TestSuiteTestCaseDeleteBulkOperationDataRequest
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class TestSuiteTestCaseDeleteBulkOperationRequest(UniversalBaseModel):
    """
    A bulk operation that represents the deletion of a Test Case.
    """

    id: str = pydantic.Field()
    """
    An ID representing this specific operation. Can later be used to look up information about the operation's success in the response.
    """

    type: typing.Literal["DELETE"] = "DELETE"
    data: TestSuiteTestCaseDeleteBulkOperationDataRequest = pydantic.Field()
    """
    Information about the Test Case to delete
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
