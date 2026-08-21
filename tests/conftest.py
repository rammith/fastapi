from unittest.mock import MagicMock

import pytest


@pytest.fixture
def database_mocks():
    connection = MagicMock()
    cursor = connection.cursor.return_value
    return connection, cursor
