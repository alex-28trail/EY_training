import os
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel, Field, field_validator
from pwdlib import PasswordHash
from psycopg2 import IntegrityError
from psycopg2.extras import RealDictCursor

from database import get_db_connection

router = APIRouter(prefix="/auth", tags=["Authentication"])

password_hash = PasswordHash.recommended()
security = HTTPBearer()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)

if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is missing from .env")


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=254)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Name cannot be empty")

        return value

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value):
        value = value.strip().lower()

        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Enter a valid email address")

        return value


class LoginRequest(BaseModel):
    email: str
    password: str


def create_access_token(user):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user["id"]),
        "role": user["role"],
        "exp": expire
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register", status_code=201)
def register(request: RegisterRequest):
    connection = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        hashed_password = password_hash.hash(request.password)

        cursor.execute(
            """
            INSERT INTO users (name, email, password_hash, role)
            VALUES (%s, %s, %s, 'CUSTOMER')
            RETURNING id, name, email, role
            """,
            (
                request.name,
                request.email,
                hashed_password
            )
        )

        user = cursor.fetchone()
        connection.commit()
        cursor.close()

        return {
            "message": "Registration successful",
            "user": user
        }

    except IntegrityError:
        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists"
        )

    except Exception:
        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail="Registration failed"
        )

    finally:
        if connection:
            connection.close()


@router.post("/login")
def login(request: LoginRequest):
    connection = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute(
            """
            SELECT id, name, email, password_hash, role
            FROM users
            WHERE email = %s
            """,
            (request.email.strip().lower(),)
        )

        user = cursor.fetchone()
        cursor.close()

        if not user or not password_hash.verify(
            request.password,
            user["password_hash"]
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        token = create_access_token(user)

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"]
            }
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Login failed"
        )

    finally:
        if connection:
            connection.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication token"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired authentication token"
        )

    connection = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute(
            """
            SELECT id, name, email, role
            FROM users
            WHERE id = %s
            """,
            (user_id,)
        )

        user = cursor.fetchone()
        cursor.close()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="User account not found"
            )

        return user

    finally:
        if connection:
            connection.close()