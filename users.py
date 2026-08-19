from fastapi import APIRouter, Depends

from auth import get_current_user

router = APIRouter()


@router.get("/users/me")
def get_user(current_user: str = Depends(get_current_user)):

    return {
        "message": "Access granted",
        "username": current_user
    }

