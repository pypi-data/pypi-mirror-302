# TODO: Moved Exceptions handling to base collection for better tests

import os
from typing import Any, Dict, List, Literal

from bson import ObjectId
from motor.core import AgnosticCursor
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import IndexModel
from pymongo.errors import DuplicateKeyError, ServerSelectionTimeoutError
from pymongo.results import (
    DeleteResult,
    InsertManyResult,
    InsertOneResult,
    UpdateResult,
)

from .exceptions import Exceptions
from .index import Index


class MongoDBClient:
    '''
    MongoDBClient is responsible for managing connections to a MongoDB database
    using the AsyncIOMotorClient. It supports both direct URL-based connections
    and parameter-based connections with configurable timeouts.
    '''

    DEFAULT_HOST: str = 'localhost'
    DEFAULT_PORT: int = 27017
    DEFAULT_USERNAME: str = 'user'
    DEFAULT_PASSWORD: str = 'user'
    DEFAULT_DB: str = 'default-db'
    DEFAULT_RESPONSE_TIMEOUT: int = 5000
    DEFAULT_CONNECTION_TIMEOUT: int = 5000

    def __init__(
        self,
        url: str | None = None,
        host: str | None = None,
        port: int | None = None,
        username: str | None = None,
        password: str | None = None,
        db: str | None = None,
        response_timeout: int | float | None = None,
        connection_timeout: int | float | None = None,
    ) -> None:
        '''
        Initialize a MongoDBClient instance with optional connection parameters.

        If a parameter is not provided, it will be fetched from environment
        variables or fall back to default values.

        Attributes:
            url (str | None):
                The connection URL, automatically generated if not provided.
            host (str):
                MongoDB host address.
            port (int):
                MongoDB port number.
            username (str):
                MongoDB username.
            password (str):
                MongoDB password.
            db (str):
                Name of the database to connect to.
            response_timeout (int | float):
                Timeout for server responses in milliseconds.
            connection_timeout (int | float):
                Timeout for establishing connections in milliseconds.
        '''

        self.host: str = host or self._get_host()
        self.port: int = port or self._get_port()
        self.username: str = username or self._get_username()
        self.password: str = password or self._get_password()
        self.db: str = db or self._get_db()
        self.response_timeout: int | float = (
            response_timeout or self._get_response_timeout()
        )
        self.connection_timeout: int | float = (
            connection_timeout or self._get_connection_timeout()
        )
        self.url: str = url or self._generate_url()
        self.__client: AsyncIOMotorClient[Any] = self._create_client()  # type: ignore

    def _get_host(self) -> str:
        '''
        Get the host for the MongoDB connection.

        Returns:
            str:
                The host from the environment or the default.
        '''
        return os.getenv('MONGODB_HOST', self.DEFAULT_HOST)

    def _get_port(self) -> int:
        '''
        Get the port for the MongoDB connection.

        Returns:
            int:
                The port from the environment or the default.
        '''
        return int(os.getenv('MONGODB_PORT', str(self.DEFAULT_PORT)))

    def _get_username(self) -> str:
        '''
        Get the username for the MongoDB connection.

        Returns:
            str:
                The username from the environment or the default.
        '''
        return os.getenv('MONGODB_USERNAME', self.DEFAULT_USERNAME)

    def _get_password(self) -> str:
        '''
        Get the password for the MongoDB connection.

        Returns:
            str:
                The password from the environment or the default.
        '''
        return os.getenv('MONGODB_PASSWORD', self.DEFAULT_PASSWORD)

    def _get_db(self) -> str:
        '''
        Get the database name for the MongoDB connection.

        Returns:
            str:
                The database name from the environment or the default.
        '''
        return os.getenv('MONGODB_DB', self.DEFAULT_DB)

    def _get_response_timeout(self) -> int | float:
        '''
        Get the response timeout for the MongoDB connection.

        Returns:
            int | float:
                The response timeout from the environment or the default.
        '''
        return int(
            os.getenv('MONGODB_RESPONSE_TIMEOUT', str(self.DEFAULT_RESPONSE_TIMEOUT))
        )

    def _get_connection_timeout(self) -> int | float:
        '''
        Get the connection timeout for the MongoDB connection.

        Returns:
            int | float:
                The connection timeout from the environment or the default.
        '''
        return int(
            os.getenv(
                'MONGODB_CONNECTION_TIMEOUT', str(self.DEFAULT_CONNECTION_TIMEOUT)
            )
        )

    def _generate_url(self) -> str:
        '''
        Generate the MongoDB connection URL using the provided host, port, username, and password.

        Returns:
            str:
                The constructed MongoDB URL.
        '''
        return f'mongodb://{self.username}:{self.password}@{self.host}:{self.port}'

    def _create_client(self) -> AsyncIOMotorClient:  # type: ignore
        '''
        Create an instance of AsyncIOMotorClient with configured timeouts.

        Returns:
            AsyncIOMotorClient[Any]:
                The initialized MongoDB client.
        '''
        return AsyncIOMotorClient(
            self.url,
            serverSelectionTimeoutMS=self.response_timeout,
            connectTimeoutMS=self.connection_timeout,
        )  # type: ignore

    def close(self) -> None:
        '''
        Close the MongoDB client connection.

        Returns:
            None
        '''
        self.__client.close()

    async def find_one(
        self, db: str, collection: str, where: dict[str, Any]
    ) -> Dict[str, Any]:
        try:
            result: dict[str, Any] | None = await self.__client[db][
                collection
            ].find_one(where)
        except ServerSelectionTimeoutError as e:
            raise Exceptions.ServerTimeoutError(e)
        except Exception as e:
            raise Exceptions.FindError(e)

        if not result:
            raise Exceptions.NotFoundError('The document was not found')

        return result

    async def find(
        self,
        db: str,
        collection: str,
        where: dict[str, Any] = {},
        skip: int = 0,
        limit: int = 25,
        sort: list[tuple[str, Literal[-1, 1]]] | None = None,
    ) -> List[Dict[str, Any]]:
        cursor: AgnosticCursor[Any] = self.__client[db][collection].find(where)
        try:
            if sort is None:
                return await cursor.skip(skip=skip).to_list(length=limit)  # type: ignore
            return await cursor.sort(sort).skip(skip=skip).to_list(length=limit)  # type: ignore
        except ServerSelectionTimeoutError as e:
            raise Exceptions.ServerTimeoutError(e)
        except Exception as e:
            raise Exceptions.FindError(e)

    async def insert_one(
        self, db: str, collection: str, document: dict[str, Any]
    ) -> ObjectId:
        try:
            result: InsertOneResult = await self.__client[db][collection].insert_one(
                document
            )
        except DuplicateKeyError as e:
            raise Exceptions.DuplicateKeyError(e)
        except ServerSelectionTimeoutError as e:
            raise Exceptions.ServerTimeoutError(e)
        except Exception as e:
            raise Exceptions.InsertError(e)

        return result.inserted_id

    async def insert_many(
        self,
        db: str,
        collection: str,
        documents: List[Dict[str, Any]],
        ordered: bool = True,
        bypass_document_validation: bool = False,
    ) -> List[ObjectId]:
        try:
            result: InsertManyResult = await self.__client[db][collection].insert_many(
                documents=documents,
                ordered=ordered,
                bypass_document_validation=bypass_document_validation,
            )
        except DuplicateKeyError as e:
            raise Exceptions.DuplicateKeyError(e)
        except ServerSelectionTimeoutError as e:
            raise Exceptions.ServerTimeoutError(e)
        except Exception as e:
            raise Exceptions.InsertError(e)

        return result.inserted_ids

    async def update_one(
        self,
        db: str,
        collection: str,
        where: dict[str, Any],
        update: dict[str, Any],
        upsert: bool = False,
    ) -> ObjectId | None:
        try:
            result: UpdateResult = await self.__client[db][collection].update_one(
                filter=where, update=update, upsert=upsert
            )
        except DuplicateKeyError as e:
            raise Exceptions.DuplicateKeyError(e)
        except ServerSelectionTimeoutError as e:
            raise Exceptions.ServerTimeoutError(e)
        except Exception as e:
            raise Exceptions.UpdateError(e)

        return result.upserted_id

    async def delete_one(self, db: str, collection: str, where: dict[str, Any]) -> int:
        try:
            result: DeleteResult = await self.__client[db][collection].delete_one(where)
        except ServerSelectionTimeoutError as e:
            raise Exceptions.ServerTimeoutError(e)
        except Exception as e:
            raise Exceptions.DeleteError(e)

        return result.deleted_count

    async def delete_many(self, db: str, collection: str, where: dict[str, Any]) -> int:
        try:
            result: DeleteResult = await self.__client[db][collection].delete_many(
                filter=where
            )
        except ServerSelectionTimeoutError as e:
            raise Exceptions.ServerTimeoutError(e)
        except Exception as e:
            raise Exceptions.DeleteError(e)

        return result.deleted_count

    async def drop_collection(self, db: str, collection: str) -> None:
        try:
            await self.__client[db][collection].drop()
        except ServerSelectionTimeoutError as e:
            raise Exceptions.ServerTimeoutError(e)
        except Exception as e:
            raise Exceptions.DropCollectionError(e)

    async def count_documents(
        self, db: str, collection: str, where: dict[str, Any]
    ) -> int:
        try:
            return await self.__client[db][collection].count_documents(filter=where)
        except ServerSelectionTimeoutError as e:
            raise Exceptions.ServerTimeoutError(e)
        except Exception as e:
            raise Exceptions.CountDocumentsError(e)

    async def create_index(
        self, db: str, collection: str, index: Index.IndexType
    ) -> None:
        try:
            await self.__client[db][collection].create_index(**index.model_dump())
        except ServerSelectionTimeoutError as e:
            raise Exceptions.ServerTimeoutError(e)
        except Exception as e:
            raise Exceptions.CreateIndexError(e)

    async def create_indexes(
        self, db: str, collection: str, indexes: list[Index.IndexType]
    ) -> None:
        try:
            await self.__client[db][collection].create_indexes(
                indexes=[IndexModel(**index.model_dump()) for index in indexes]
            )
        except ServerSelectionTimeoutError as e:
            raise Exceptions.ServerTimeoutError(e)
        except Exception as e:
            raise Exceptions.CreateIndexError(e)

    async def drop_index(self, db: str, collection: str, index_or_name: str) -> None:
        try:
            await self.__client[db][collection].drop_index(index_or_name=index_or_name)
        except ServerSelectionTimeoutError as e:
            raise Exceptions.ServerTimeoutError(e)
        except Exception as e:
            raise Exceptions.DropIndexError(e)

    async def drop_indexes(self, db: str, collection: str) -> None:
        try:
            await self.__client[db][collection].drop_indexes()
        except ServerSelectionTimeoutError as e:
            raise Exceptions.ServerTimeoutError(e)
        except Exception as e:
            raise Exceptions.DropIndexError(e)
