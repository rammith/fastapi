from unittest.mock import patch

from database import get_connection


def test_opens_database_connection():
    environment = {
        "DB_HOST": "localhost",
        "DB_DATABASE": "app_db",
        "DB_USER": "app_user",
        "DB_PASSWORD": "secret",
        "DB_PORT": "5432",
    }

    with patch("database.os.getenv", side_effect=environment.get) as getenv:
        with patch("database.psycopg2.connect", return_value="connection") as connect:
            result = get_connection()

    assert result == "connection"
    connect.assert_called_once_with(
        host="localhost",
        database="app_db",
        user="app_user",
        password="secret",
        port="5432",
    )
    assert getenv.call_count == 5
