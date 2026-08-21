from unittest.mock import patch

import pytest
from fastapi import HTTPException

from login import login
from schemas.login_request import LoginRequest


def test_logs_in_valid_user(database_mocks):
    connection, cursor = database_mocks
    cursor.fetchone.return_value = (1, "newuser", "Strong1!")
    request = LoginRequest(username="newuser", password="Strong1!")

    with patch("login.get_connection", return_value=connection):
        with patch("login.create_access_token", return_value="test-token"):
            result = login(request)

    assert result == {
        "message": "Login successful",
        "access_token": "test-token",
        "token_type": "bearer",
    }
    cursor.execute.assert_called_once_with(
        "SELECT * FROM users WHERE username = %s AND password = %s",
        ("newuser", "Strong1!"),
    )
    cursor.close.assert_called_once_with()
    connection.close.assert_called_once_with()


def test_rejects_invalid_login(database_mocks):
    connection, cursor = database_mocks
    cursor.fetchone.return_value = None
    request = LoginRequest(username="newuser", password="Wrong1!")

    with patch("login.get_connection", return_value=connection):
        with pytest.raises(HTTPException) as error:
            login(request)

    assert error.value.status_code == 401
    assert error.value.detail == "Invalid username or password"
    cursor.close.assert_called_once_with()
    connection.close.assert_called_once_with()


def test_converts_login_database_failure_to_server_error(database_mocks):
    connection, cursor = database_mocks
    cursor.execute.side_effect = RuntimeError("database unavailable")
    request = LoginRequest(username="newuser", password="Strong1!")

    with patch("login.get_connection", return_value=connection):
        with pytest.raises(HTTPException) as error:
            login(request)

    assert error.value.status_code == 500
    assert error.value.detail == "Something went wrong"
    connection.rollback.assert_called_once_with()
    cursor.close.assert_called_once_with()
    connection.close.assert_called_once_with()
