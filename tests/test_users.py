from users import get_user


def test_users_me_returns_authenticated_user():
    assert get_user(current_user="newuser") == {
        "message": "Access granted",
        "username": "newuser",
    }
