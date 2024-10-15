import pytest

from simple_mongodb import BaseCollection, MongoDBClient


class ExampleCollection(BaseCollection):
    collection = 'example-collection'
    db = 'test_db'


@pytest.fixture()
def client() -> MongoDBClient:
    return MongoDBClient()


@pytest.fixture()
def example_collection(client: MongoDBClient) -> ExampleCollection:
    return ExampleCollection(client)
