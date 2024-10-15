# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .prompt_block_state import PromptBlockState
from .ephemeral_prompt_cache_config_request import EphemeralPromptCacheConfigRequest
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class VariablePromptBlockRequest(UniversalBaseModel):
    """
    A block that represents a variable in a prompt template.
    """

    block_type: typing.Literal["VARIABLE"] = "VARIABLE"
    id: str
    state: typing.Optional[PromptBlockState] = None
    cache_config: typing.Optional[EphemeralPromptCacheConfigRequest] = None
    input_variable_id: str

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
