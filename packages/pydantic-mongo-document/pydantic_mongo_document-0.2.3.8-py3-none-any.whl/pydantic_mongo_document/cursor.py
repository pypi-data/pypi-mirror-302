import typing
from typing import Any, Generic, Self, TypeVar

import motor.motor_asyncio
import pymongo.cursor

D = TypeVar("D", bound="Document")


class Cursor(Generic[D]):
    model_cls: type[D]

    def __init__(
        self, cursor: pymongo.cursor.Cursor | motor.motor_asyncio.AsyncIOMotorCursor
    ) -> None:
        self.cursor = cursor
        self.iterable = None

    def __class_getitem__(cls, item) -> Self:
        result = super().__class_getitem__(item)
        result.model_cls = item
        return result

    def __aiter__(self) -> Self:
        self.iterable = self.cursor.__aiter__()
        return self

    def __iter__(self) -> Self:
        self.iterable = self.cursor.__iter__()
        return

    def __call__(self, *args, **kwargs):
        return Cursor[self.model_cls](self.cursor(*args, **kwargs))

    def __getattr__(self, item) -> Self | Any:
        value = getattr(self.cursor, item)

        if isinstance(value, typing.Callable):
            return Cursor[self.model_cls](value)

        return value

    async def __anext__(self) -> D:
        return self.model_cls.model_validate(await self.iterable.__anext__())

    def __next__(self) -> D:
        return self.model_cls.model_validate(next(self.iterable))
