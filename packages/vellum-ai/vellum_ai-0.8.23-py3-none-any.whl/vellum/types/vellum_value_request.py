# This file was auto-generated by Fern from our API Definition.

import typing
from .string_vellum_value_request import StringVellumValueRequest
from .number_vellum_value_request import NumberVellumValueRequest
from .json_vellum_value_request import JsonVellumValueRequest
from .image_vellum_value_request import ImageVellumValueRequest
from .function_call_vellum_value_request import FunctionCallVellumValueRequest
from .error_vellum_value_request import ErrorVellumValueRequest
from .array_vellum_value_request import ArrayVellumValueRequest
from .chat_history_vellum_value_request import ChatHistoryVellumValueRequest
from .search_results_vellum_value_request import SearchResultsVellumValueRequest

VellumValueRequest = typing.Union[
    StringVellumValueRequest,
    NumberVellumValueRequest,
    JsonVellumValueRequest,
    ImageVellumValueRequest,
    FunctionCallVellumValueRequest,
    ErrorVellumValueRequest,
    ArrayVellumValueRequest,
    ChatHistoryVellumValueRequest,
    SearchResultsVellumValueRequest,
]
