# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .sentence_chunker_config_request import SentenceChunkerConfigRequest
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class SentenceChunkingRequest(UniversalBaseModel):
    """
    Sentence chunking
    """

    chunker_name: typing.Literal["sentence-chunker"] = "sentence-chunker"
    chunker_config: typing.Optional[SentenceChunkerConfigRequest] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
