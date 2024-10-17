from abc import ABC, abstractmethod
from typing import Any, ClassVar, Generic, List, Optional, Self, Type, TypeVar

import bson
import pymongo.errors
import pymongo.results
from pydantic import BaseModel, Field, validate_call

from pydantic_mongo_document.config import ReplicaConfig
from pydantic_mongo_document.cursor import Cursor
from pydantic_mongo_document.encoder import JsonEncoder
from pydantic_mongo_document.exceptions import DocumentNotFound

DATABASE = TypeVar("DATABASE")
CLIENT = TypeVar("CLIENT")
COLLECTION = TypeVar("COLLECTION")

# Document Return Type
DRT = TypeVar("DRT")  # Delete return type
CCRT = TypeVar("CCRT")  # Commit changes return type
CRT = TypeVar("CRT")  # Count return type

CONFIG = {}
"""Map of replicas to mongo URIs."""


class DocumentBase(BaseModel, ABC, Generic[CRT, CCRT, DRT]):
    __primary_key__: ClassVar[str] = "id"

    __replica__: ClassVar[str]
    """Mongodb replica name."""

    __database__: ClassVar[str]
    """Mongodb database name."""

    __collection__: ClassVar[str]
    """Mongodb collection name."""

    __clients__: ClassVar[dict[str, Any]] = {}
    """Map of clients for each database."""

    __document__: dict[str, Any]
    """Document data. For internal use only."""

    NotFoundError: ClassVar[Type[Exception]] = DocumentNotFound
    DuplicateKeyError: ClassVar[Type[Exception]] = pymongo.errors.DuplicateKeyError

    encoder: ClassVar[JsonEncoder] = JsonEncoder()

    id: str = Field(default_factory=lambda: str(bson.ObjectId()), alias="_id")

    def model_post_init(self, __context: Any) -> None:
        self.__document__ = self.model_dump(by_alias=True, exclude_none=True)

    @classmethod
    @abstractmethod
    def client(cls) -> CLIENT:
        """Returns client for database."""

    @classmethod
    @abstractmethod
    def database(cls) -> DATABASE:
        """Returns database."""

    @classmethod
    @abstractmethod
    def collection(cls) -> COLLECTION:
        """Returns collection."""

    @property
    def primary_key(self) -> Any:
        return getattr(self, self.__primary_key__)

    @classmethod
    def get_replica_config(cls) -> ReplicaConfig:
        return CONFIG[cls.__replica__]

    @property
    def primary_key_field_name(self) -> str:
        return self.model_fields[self.__primary_key__].alias or self.__primary_key__

    @classmethod
    @validate_call
    def set_replica_config(cls, config: dict[str, ReplicaConfig]) -> None:
        CONFIG.clear()
        CONFIG.update(config)

    @classmethod
    def create_indexes(cls) -> None:
        """Creates indexes for collection."""

    @classmethod
    @abstractmethod
    def one(
        cls,
        document_id: str | None = None,
        add_query: dict[str, Any] | None = None,
        required: bool = True,
        **kwargs: Any,
    ) -> Self:
        """Finds one document by ID."""

        raise NotImplementedError()

    @classmethod
    def all(
        cls,
        document_ids: List[str | bson.ObjectId] | None = None,
        add_query: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Cursor[Self]:
        """Finds all documents based in IDs."""

        query = {}
        if document_ids is not None:
            query["_id"] = {"$in": document_ids}
        if add_query is not None:
            query.update(add_query)

        query = cls.encoder.encode_dict(query, reveal_secrets=True)

        return Cursor[cls](cls.collection().find(query, **kwargs))

    @classmethod
    def count(cls, add_query: dict[str, Any] | None = None, **kwargs: Any) -> CRT:
        """Counts documents in collection."""

        query = {}
        if add_query is not None:
            query.update(add_query)

        query = cls.encoder.encode_dict(query, reveal_secrets=True)

        return cls.collection().count_documents(query, **kwargs)

    def delete(self) -> DRT:
        """Deletes document from collection."""

        query = self.encoder.encode_dict(
            {self.primary_key_field_name: self.primary_key},
        )

        return self.collection().delete_one(query)

    def commit_changes(self, fields: Optional[List[str]] = None) -> CCRT:
        """Saves changes to document."""

        search_query: dict[str, Any] = {self.primary_key_field_name: self.primary_key}
        update_query: dict[str, Any] = {}

        if not fields:
            fields = [field for field in self.model_fields.keys() if field != self.__primary_key__]

        data = self.encoder.encode_dict(
            self.model_dump(by_alias=True, exclude_none=True),
            reveal_secrets=True,
        )

        for field in fields:
            if field in data and data[field] != self.__document__.get(field):
                update_query.setdefault("$set", {}).update({field: data[field]})
            elif field not in data and field in self.__document__:
                update_query.setdefault("$unset", {}).update({field: ""})

        if update_query:
            return self.collection().update_one(search_query or None, update_query)

        return self.noop()

    @abstractmethod
    def insert(self) -> Self:
        """Inserts document to collection."""

        raise NotImplementedError()

    def noop(self) -> None:
        """No operation. Does nothing."""
