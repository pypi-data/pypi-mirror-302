# TODO: implement test for url param

import os

from simple_mongodb.mongodb_client import MongoDBClient


def test_mongodb_client_host_default_value() -> None:
    client: MongoDBClient = MongoDBClient()
    assert client.host == 'localhost'


def test_mongodb_client_host_load_from_env() -> None:
    os.environ['MONGODB_HOST'] = 'test-host'
    client: MongoDBClient = MongoDBClient()
    assert client.host == 'test-host'


def test_mongodb_client_initialization_with_host() -> None:
    client: MongoDBClient = MongoDBClient(host='test-host')
    assert client.host == 'test-host'


def test_mongodb_client_port_default_value() -> None:
    client: MongoDBClient = MongoDBClient()
    assert client.port == 27017


def test_mongodb_client_port_load_from_env() -> None:
    os.environ['MONGODB_PORT'] = '27000'
    client: MongoDBClient = MongoDBClient()
    os.environ.pop('MONGODB_PORT', None)
    assert client.port == 27000


def test_mongodb_client_initialization_with_port() -> None:
    client: MongoDBClient = MongoDBClient(port=27000)
    assert client.port == 27000


def test_mongodb_client_username_default_value() -> None:
    client: MongoDBClient = MongoDBClient()
    assert client.username == 'user'


def test_mongodb_client_username_load_from_env() -> None:
    os.environ['MONGODB_USERNAME'] = 'test-user'
    client: MongoDBClient = MongoDBClient()
    assert client.username == 'test-user'


def test_mongodb_client_initialization_with_username() -> None:
    client: MongoDBClient = MongoDBClient(username='test-user')
    assert client.username == 'test-user'


def test_mongodb_client_password_default_value() -> None:
    client: MongoDBClient = MongoDBClient()
    assert client.password == 'user'


def test_mongodb_client_password_load_from_env() -> None:
    os.environ['MONGODB_PASSWORD'] = 'test-password'
    client: MongoDBClient = MongoDBClient()
    assert client.password == 'test-password'


def test_mongodb_client_initialization_with_password() -> None:
    client: MongoDBClient = MongoDBClient(password='test-password')
    assert client.password == 'test-password'


def test_mongodb_client_response_timeout_default_value() -> None:
    client: MongoDBClient = MongoDBClient()
    assert client.response_timeout == 5000


def test_mongodb_client_response_timeout_load_from_env() -> None:
    os.environ['MONGODB_RESPONSE_TIMEOUT'] = '2000'
    client: MongoDBClient = MongoDBClient()
    assert client.response_timeout == 2000


def test_mongodb_client_initialization_with_response_timeout() -> None:
    client: MongoDBClient = MongoDBClient(response_timeout=2000)
    assert client.response_timeout == 2000


def test_mongodb_client_connection_timeout_default_value() -> None:
    client: MongoDBClient = MongoDBClient()
    assert client.connection_timeout == 5000


def test_mongodb_client_connection_timeout_load_from_env() -> None:
    os.environ['MONGODB_CONNECTION_TIMEOUT'] = '2000'
    client: MongoDBClient = MongoDBClient()
    assert client.connection_timeout == 2000


def test_mongodb_client_initialization_with_connection_timeout() -> None:
    client: MongoDBClient = MongoDBClient(connection_timeout=2000)
    assert client.connection_timeout == 2000


def test_mongodb_client_db_default_value() -> None:
    client: MongoDBClient = MongoDBClient()
    assert client.db == 'default-db'


def test_mongodb_client_db_load_from_env() -> None:
    os.environ['MONGODB_DB'] = 'test-db'
    client: MongoDBClient = MongoDBClient()
    assert client.db == 'test-db'
