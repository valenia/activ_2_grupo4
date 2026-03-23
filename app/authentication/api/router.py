from fastapi import APIRouter, Body, Header, status

from app.authentication.dependency_injection.container import (
    get_introspect_controller,
    get_login_controller,
    get_logout_controller,
    get_register_controller,
)
from app.authentication.domain.bo.introspect_output import IntrospectOutput
from app.authentication.domain.bo.login_input import LoginInput
from app.authentication.domain.bo.register_input import RegisterInput

router = APIRouter(tags=["Authentication"])


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
async def register(input_data: RegisterInput = Body()):
    controller = get_register_controller()
    return await controller.execute(input_data)


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
async def login(input_data: LoginInput = Body()):
    controller = get_login_controller()
    return await controller.execute(input_data)


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
async def logout(auth: str = Header(..., alias="Auth")):
    controller = get_logout_controller()
    return await controller.execute(auth)


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
async def introspect(auth: str = Header(..., alias="Auth")):
    controller = get_introspect_controller()
    return await controller.execute(auth)
