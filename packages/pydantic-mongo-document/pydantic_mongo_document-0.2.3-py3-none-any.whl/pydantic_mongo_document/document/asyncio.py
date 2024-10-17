import asyncio
from typing import Any, Coroutine, Optional, Self

import pymongo.results
from typing_extensions import override


try:
    from motor.motor_asyncio import (
        AsyncIOMotorClient,
        AsyncIOMotorCollection,
        AsyncIOMotorDatabase,
    )
except ImportError:
    raise RuntimeError(
        "Asyncio version of pydantic-mongo-document requires 'asyncio' extra to be installed\n"
        "Use 'pip install pydantic-mongo-document[asyncio]' to install the required dependencies"
    )

from pydantic_mongo_document.document.base import DocumentBase

DRT = Coroutine[Any, Any, pymongo.results.DeleteResult]  # Delete return type
CCRT = Coroutine[Any, Any, Optional[pymongo.results.UpdateResult]]  # Commit changes return type
CRT = Coroutine[Any, Any, int]  # Count return type

_ASYNC_CLIENTS = {}  # type: dict[str, AsyncIOMotorClient]


class Document(DocumentBase[CRT, CCRT, DRT]):
    """Async document model."""

    @classmethod
    def client(cls) -> AsyncIOMotorClient:
        if cls.__replica__ not in _ASYNC_CLIENTS:
            _ASYNC_CLIENTS[cls.__replica__] = AsyncIOMotorClient(
                host=str(cls.get_replica_config().uri),
                **cls.get_replica_config().client_options,
            )

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()

        # Set the current event loop to the client's I/O loop
        _ASYNC_CLIENTS[cls.__replica__]._io_loop = loop  # noqa

        return _ASYNC_CLIENTS[cls.__replica__]

    @classmethod
    def database(cls) -> AsyncIOMotorDatabase:
        return cls.client()[cls.__database__]

    @classmethod
    def collection(cls) -> AsyncIOMotorCollection:
        return cls.database()[cls.__collection__]

    @classmethod
    async def create_indexes(cls) -> None:
        """Creates indexes for collection."""

    @classmethod
    async def one(
        cls,
        document_id: str | None = None,
        add_query: dict[str, Any] | None = None,
        required: bool = True,
        **kwargs: Any,
    ) -> Optional[Self]:
        """Finds one document by ID."""

        query = {}
        if document_id is not None:
            query["_id"] = document_id
        if add_query is not None:
            query.update(add_query)

        query = cls.encoder.encode_dict(query, reveal_secrets=True)

        result = await cls.collection().find_one(query, **kwargs)

        if result is not None:
            return cls.model_validate(result)

        if required:
            raise cls.NotFoundError()

        return None

    async def insert(self) -> Self:
        """Inserts document into collection."""

        obj = await self.collection().insert_one(
            self.encoder.encode_dict(
                self.model_dump(by_alias=True, exclude_none=True),
                reveal_secrets=True,
            )
        )

        if getattr(self, self.__primary_key__, None) is None:
            setattr(self, self.__primary_key__, obj.inserted_id)

        return self

    async def noop(self) -> None:
        """No operation. Does nothing."""
