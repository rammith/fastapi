from unittest.mock import patch

import pytest
from fastapi import HTTPException

from register import register
from schemas.register_request import RegisterRequest


def test_registers_new_user(database_mocks):
    connection, cursor = database_mocks
    cursor.fetchone.return_value = None
    request = RegisterRequest(username="newuser", password="Strong1!")

    with patch("register.get_connection", return_value=connection):
        result = register(request)

    assert result == {"message": "User registered successfully"}
    connection.commit.assert_called_once_with()
    cursor.execute.assert_any_call(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        ("newuser", "Strong1!"),
    )
    cursor.close.assert_called_once_with()
    connection.close.assert_called_once_with()


def test_rejects_duplicate_user(database_mocks):
    connection, cursor = database_mocks
    cursor.fetchone.return_value = (1, "newuser", "Strong1!")
    request = RegisterRequest(username="newuser", password="Strong1!")

    with patch("register.get_connection", return_value=connection):
        with pytest.raises(HTTPException) as error:
            register(request)

    assert error.value.status_code == 400
    assert error.value.detail == "User already exists"
    connection.commit.assert_not_called()
    cursor.close.assert_called_once_with()
    connection.close.assert_called_once_with()


def test_converts_database_failure_to_server_error(database_mocks):
    connection, cursor = database_mocks
    cursor.execute.side_effect = RuntimeError("database unavailable")
    request = RegisterRequest(username="newuser", password="Strong1!")

    with patch("register.get_connection", return_value=connection):
        with pytest.raises(HTTPException) as error:
            register(request)

    assert error.value.status_code == 500
    assert error.value.detail == "Something went wrong"
    connection.rollback.assert_called_once_with()
    cursor.close.assert_called_once_with()
    connection.close.assert_called_once_with()


@pytest.mark.parametrize(
    "password",
    ["weakpass", "lowercase1!", "UPPERCASE1!", "NoNumber!", "NoSpecial1"],
)
def test_rejects_password_missing_required_character(password):
    with pytest.raises(ValueError):
        RegisterRequest(username="newuser", password=password)
