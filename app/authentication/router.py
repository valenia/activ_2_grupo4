import hashlib
import uuid
from typing import Optional

from fastapi import APIRouter, Body, Header, HTTPException, status
from pydantic import BaseModel

from app.authentication.models import UserDB

router = APIRouter(tags=["Authentication"])


class RegisterInput(BaseModel):
    username: str
    email: str
    address: Optional[str] = None
    password: str


class UserBO(BaseModel):
    username: str
    email: str
    address: Optional[str] = None
    hashed_password: str


class LoginInput(BaseModel):
    email: str
    password: str


class IntrospectOutput(BaseModel):
    username: str
    email: str
    address: Optional[str] = None


""" Local dictionary to store users and sessions
users_db: dict[str, UserBO] = {} no longer in use"""
sessions_db: dict[str, str] = {}


def hash_pass(password: str) -> str:
    # Simple SHA-256 hash for demonstration purposes only
    return hashlib.sha256(password.encode()).hexdigest()


@router.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@router.post(
    "/register",
    status_code=status.HTTP_200_OK,
    summary="Register a new user",
    description="""
    Creates a new user account in the system.

    Required fields:
    - `username`: User's display name
    - `email`: Valid email address (must be unique)
    - `password`: User's password

    Optional fields:
    - `address`: Physical address (optional)

    Process:
    1. Validates that email is not already registered
    2. Creates a new user with hashed password
    3. Stores user in memory database

    Important:
    - Email addresses must be unique across the system
    - Passwords are hashed (simulated) before storage
    """,
    responses={
        200: {
            "description": "User registered successfully",
            "content": {"application/json": {"example": {"status": "ok"}}},
        },
        409: {
            "description": "Email already exists",
            "content": {"application/json": {"example": {"detail": "Email already registered"}}},
        },
        422: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "email"],
                                "msg": "field required",
                                "type": "value_error.missing",
                            }
                        ]
                    }
                }
            },
        },
    },
)
async def register(input: RegisterInput = Body()) -> dict:
    try:
        inner_object = UserBO(
            username=input.username,
            email=input.email,
            address=input.address,
            hashed_password=hash_pass(input.password),
        )

        if await UserDB.filter(email=inner_object.email).exists():
            raise HTTPException(status_code=409, detail="Email already registered")
        if await UserDB.filter(username=inner_object.username).exists():
            raise HTTPException(status_code=409, detail="Username already registered")


        user_db = await UserDB.create(
            username=inner_object.username,
            email=inner_object.email,
            address=inner_object.address,
            hashed_password=inner_object.hashed_password,
        )
        return {"user_db.id = ": user_db.id}
    
    except Exception as e:
        print("REGISTER ERROR:", repr(e))
        raise


def UserNotFoundException(Exception):
    pass


async def get_user(email: str):
    user_db = await UserDB.get_or_none(email=email)
    if user_db is None:
        raise UserNotFoundException
    return user_db


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="Authenticate user",
    description="""
    Authenticates a user and returns a session token.

    Required fields:
    - `email`: User's registered email
    - `password`: User's password

    Process:
    1. Validates that email exists in the system
    2. Verifies password matches
    3. Generates a unique UUID token
    4. Stores session in memory

    Response:
    Returns an authentication token that must be included in the `Auth` header
    for subsequent authenticated requests.

    Important:
    - Tokens are UUID v4 format
    - Tokens are unique and will not collide
    - Token must be sent in `Auth` header for protected endpoints
    """,
    responses={
        200: {
            "description": "Login successful",
            "content": {
                "application/json": {"example": {"auth": "550e8400-e29b-41d4-a716-446655440000"}}
            },
        },
        401: {
            "description": "Invalid password",
            "content": {"application/json": {"example": {"detail": "Incorrect password"}}},
        },
        404: {
            "description": "Email not found",
            "content": {"application/json": {"example": {"detail": "Email not registered"}}},
        },
        422: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "email"],
                                "msg": "field required",
                                "type": "value_error.missing",
                            }
                        ]
                    }
                }
            },
        },
    },
)
async def login(input: LoginInput = Body()) -> dict[str, str]:
    try:
        user_db = await get_user(input.email)
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="Email not registered")

    if hash_pass(input.password) != user_db.hashed_password:
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = str(uuid.uuid4())
    while token in sessions_db:
        token = str(uuid.uuid4())
    sessions_db[token] = input.email
    return {"auth": token}


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Logout user",
    description="""
    Invalidates a user session token.

    Required headers:
    - `Auth`: Session token obtained from login

    Process:
    1. Validates that the token exists
    2. Removes the session from memory
    3. Token becomes invalid for future requests

    Important:
    - After logout, the same token cannot be used again
    - User must login again to get a new token
    """,
    responses={
        200: {
            "description": "Logout successful",
            "content": {"application/json": {"example": {"status": "ok"}}},
        },
        401: {
            "description": "Invalid token",
            "content": {"application/json": {"example": {"detail": "Incorrect Token"}}},
        },
    },
)
async def logout(auth: str = Header()) -> dict[str, str]:
    if auth not in sessions_db:
        raise HTTPException(status_code=401, detail="Incorrect Token")

    del sessions_db[auth]
    return {"status": "ok"}


@router.get(
    "/introspect",
    response_model=IntrospectOutput,
    summary="Validate token and get user info",
    description="""
    Validates a session token and returns user information.

    Required headers:
    - `Auth`: Session token obtained from login

    Process:
    1. Validates that the token exists
    2. Retrieves the associated user email
    3. Fetches user details from database
    4. Returns user information without sensitive data

    Response:
    Returns user profile information:
    - `username`: User's display name
    - `email`: User's email address
    - `address`: User's address (if provided)

    Useful for:
    - Checking if a token is still valid
    - Getting current user information
    - Verifying authentication status
    """,
    responses={
        200: {
            "description": "Token is valid",
            "content": {
                "application/json": {
                    "example": {
                        "username": "john_doe",
                        "email": "john@example.com",
                        "address": "123 Main St",
                    }
                }
            },
        },
        401: {
            "description": "Invalid token",
            "content": {"application/json": {"example": {"detail": "Incorrect Token"}}},
        },
    },
)
async def checkToken(auth: str = Header()) -> IntrospectOutput:
    if auth not in sessions_db:
        raise HTTPException(status_code=401, detail="Incorrect Token")

    current_email = sessions_db[auth]
    try:
        user_db = await get_user(current_email)
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="Email not registered")

    return IntrospectOutput(username=user_db.username, email=user_db.email, address=user_db.address)
