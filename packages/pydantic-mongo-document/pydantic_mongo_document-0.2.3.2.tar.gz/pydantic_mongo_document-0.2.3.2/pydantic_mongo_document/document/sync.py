from typing import Any, List, Optional, Self

import pymongo.results
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.mongo_client import MongoClient

from pydantic_mongo_document.cursor import Cursor
from pydantic_mongo_document.document.base import DocumentBase
from pydantic_mongo_document.types import ObjectId

DRT = pymongo.results.DeleteResult  # Delete return type
CCRT = Optional[pymongo.results.UpdateResult]  # Commit changes return type
CRT = int  # Count return type

_SYNC_CLIENTS = {}  # type: dict[str, MongoClient]


class Document(DocumentBase[CRT, CCRT, DRT]):
    @classmethod
    def client(cls) -> MongoClient[Self]:
        if cls.__replica__ not in _SYNC_CLIENTS:
            _SYNC_CLIENTS[cls.__replica__] = MongoClient(
                str(cls.get_replica_config().uri),
                **cls.get_replica_config().client_options,
            )

        return _SYNC_CLIENTS[cls.__replica__]

    @classmethod
    def database(cls) -> Database[Self]:
        return cls.client()[cls.__database__]

    @classmethod
    def collection(cls) -> Collection[Any]:
        return cls.database()[cls.__collection__]

    @classmethod
    def create_indexes(cls) -> None:
        """Creates indexes for collection."""

    def all(
        self,
        document_ids: List[str | ObjectId] | None = None,
        add_query: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Cursor[Self]:
        """Finds all documents by IDs."""

        query = {}
        if document_ids is not None:
            query["_id"] = {"$in": [str(document_id) for document_id in document_ids]}
        if add_query is not None:
            query.update(add_query)

        query = self.encoder.encode_dict(query, reveal_secrets=True)

        return Cursor(self.collection().find(query, **kwargs))

    @classmethod
    def one(
        cls,
        document_id: str | None = None,
        add_query: dict[str, Any] | None = None,
        required: bool = True,
        **kwargs: Any,
    ) -> Self:
        """Finds one document by ID."""

        query = {}
        if document_id is not None:
            query["_id"] = document_id
        if add_query is not None:
            query.update(add_query)

        query = cls.encoder.encode_dict(query, reveal_secrets=True)

        result = cls.collection().find_one(query, **kwargs)

        if result is not None:
            return cls.model_validate(result)

        if required:
            raise cls.NotFoundError()

        return None

    def insert(self) -> Self:
        """Inserts document to collection."""

        obj = self.collection().insert_one(
            self.encoder.encode_dict(
                self.model_dump(by_alias=True, exclude_none=True),
                reveal_secrets=True,
            )
        )

        if getattr(self, self.__primary_key__, None) is None:
            setattr(self, self.__primary_key__, obj.inserted_id)

        return self
