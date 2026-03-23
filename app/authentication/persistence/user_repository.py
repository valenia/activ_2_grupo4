from app.authentication.domain.bo.user_bo import UserBO
from app.authentication.models import UserDB


async def create_user(user_bo: UserBO):
    """Create a new user in database"""
    return await UserDB.create(
        username=user_bo.username,
        email=user_bo.email,
        address=user_bo.address,
        hashed_password=user_bo.hashed_password,
    )


async def get_user_by_email(email: str):
    """Get user by email"""
    return await UserDB.get_or_none(email=email)


async def email_exists(email: str) -> bool:
    """Check if email already exists"""
    return await UserDB.filter(email=email).exists()


async def username_exists(username: str) -> bool:
    """Check if username already exists"""
    return await UserDB.filter(username=username).exists()
