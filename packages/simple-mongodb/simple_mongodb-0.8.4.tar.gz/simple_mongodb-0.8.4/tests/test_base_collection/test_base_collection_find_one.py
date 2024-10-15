from typing import Any
from unittest.mock import AsyncMock

import pytest
from bson import ObjectId

from simple_mongodb import BaseCollection


@pytest.mark.asyncio
async def test_base_collection_find_one_find_error(
    example_collection: BaseCollection,
) -> None:
    example_collection.client.find_one = AsyncMock(
        side_effect=BaseCollection.FindError()
    )

    with pytest.raises(BaseCollection.FindError):
        await example_collection.find_one(where={})


@pytest.mark.asyncio
async def test_base_collection_find_one_not_found(
    example_collection: BaseCollection,
) -> None:
    example_collection.client.find_one = AsyncMock(
        side_effect=BaseCollection.NotFoundError()
    )

    with pytest.raises(BaseCollection.NotFoundError):
        await example_collection.find_one(where={})


@pytest.mark.asyncio
async def test_base_collection_find_one_server_timeout_error(
    example_collection: BaseCollection,
) -> None:
    example_collection.client.find_one = AsyncMock(
        side_effect=BaseCollection.ServerTimeoutError()
    )

    with pytest.raises(BaseCollection.ServerTimeoutError):
        await example_collection.find_one(where={})


@pytest.mark.asyncio
async def test_base_collection_find_one_success(
    example_collection: BaseCollection,
) -> None:
    mock_document: dict[str, Any] = {'_id': ObjectId(), 'name': 'Test Document'}
    example_collection.client.find_one = AsyncMock(return_value=mock_document)

    where: dict[str, Any] = {'name': 'Test Document'}
    result: dict[str, Any] = await example_collection.find_one(where=where)
    assert result == mock_document

    example_collection.client.find_one.assert_awaited_once_with(
        db=example_collection.db, collection=example_collection.collection, where=where
    )
