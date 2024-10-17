from typing import Annotated, Literal

import bson
import bson.json_util
from pydantic import BeforeValidator, StringConstraints, WrapSerializer
from pydantic_core.core_schema import SerializationInfo


_ObjectIdString = Annotated[
    str, StringConstraints(min_length=24, max_length=24, pattern=r"^[a-f\d]{24}$")
]

_DictObjectId = dict[Literal["$oid"], _ObjectIdString]


def check_object_id(value: _ObjectIdString | _DictObjectId) -> str:
    if isinstance(value, dict):
        value = value["$oid"]

    if not bson.ObjectId.is_valid(value):
        raise ValueError("Invalid ObjectId")

    return str(value)


def convert_object_id(
    value: str, handler, info: SerializationInfo
):
    if info.context is not None and info.context.get("document"):
        return {"$oid": handler(value, info)}

    return handler(value, info)


ObjectId = Annotated[
    _ObjectIdString,
    BeforeValidator(check_object_id),
    WrapSerializer(convert_object_id),
]

__all__ = ["ObjectId"]
