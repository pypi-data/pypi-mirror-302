from typing import Annotated

import bson
from pydantic import BeforeValidator


def check_object_id(value: str) -> str:
    if not bson.ObjectId.is_valid(value):
        raise ValueError("Invalid ObjectId")
    return str(value)


ObjectId = Annotated[str, BeforeValidator(check_object_id)]
