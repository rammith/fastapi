from fastapi import APIRouter,HTTPException,status
from database import get_connection
from schemas.register_request import RegisterRequest


router=APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username = %s",
            (data.username,)
        )

        user = cursor.fetchone()

        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (data.username, data.password)
        )

        connection.commit()

        return {
            "message": "User registered successfully"
        }

    except HTTPException:
        raise

    except Exception as e:
        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong"
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()
    

    """if username in users:
            return {"message":"User Already Exists"}
    users[username]=password
    if not username or not password:
        return {"message":"Username and Password Required"}

    
    return {"message":"User Registered Successfully"}"""