from unittest.mock import patch

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt

import auth
from auth import create_access_token, get_current_user


def test_creates_and_decodes_access_token():
    with patch.object(auth, "SECRET_KEY", "test-secret"):
        token = create_access_token("newuser")
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=token,
        )

        assert get_current_user(credentials) == "newuser"


def test_rejects_token_without_username():
    with patch.object(auth, "SECRET_KEY", "test-secret"):
        token = jwt.encode({}, "test-secret", algorithm="HS256")
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=token,
        )

        with pytest.raises(HTTPException) as error:
            get_current_user(credentials)

    assert error.value.status_code == 401
    assert error.value.detail == "Could not validate credentials"


def test_rejects_invalid_access_token():
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="invalid-token",
    )

    with patch.object(auth, "SECRET_KEY", "test-secret"):
        with pytest.raises(HTTPException) as error:
            get_current_user(credentials)

    assert error.value.status_code == 401
    assert error.value.detail == "Could not validate credentials"
