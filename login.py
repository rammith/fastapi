from fastapi import APIRouter,HTTPException,status
from database import get_connection
from schemas.login_request import LoginRequest
from auth import create_access_token

router=APIRouter()

@router.post("/login")
def login(data:LoginRequest):

    connection=None
    cursor=None
    
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s",
            (data.username, data.password)
        )

        user = cursor.fetchone()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

        access_token = create_access_token(data.username)

        return {
            "message": "Login successful",
            "access_token": access_token,
            "token_type": "bearer"
        }

    except HTTPException:
        raise


    except Exception as e:
        if connection:
            connection.rollback()

        print(f"Error occurred during login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong"
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()
