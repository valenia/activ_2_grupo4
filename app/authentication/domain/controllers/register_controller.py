from fastapi import HTTPException, status

from app.authentication.domain.bo.register_input import RegisterInput
from app.authentication.domain.bo.user_bo import UserBO
from app.authentication.domain.services.hashing_password_service import HashingPasswordService
from app.authentication.persistence.user_repository import (
    create_user,
    email_exists,
    username_exists,
)


class RegisterController:
    """Controller for user registration"""

    def __init__(self):
        self.hashing_service = HashingPasswordService()

    async def execute(self, input_data: RegisterInput) -> dict:
        """Execute registration logic"""
        # Create business object
        user_bo = UserBO(
            username=input_data.username,
            email=input_data.email,
            address=input_data.address,
            hashed_password=self.hashing_service.hash(input_data.password),
        )

        # Validate uniqueness
        if await email_exists(user_bo.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
            )

        if await username_exists(user_bo.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Username already registered"
            )

        # Create user in database
        user_db = await create_user(user_bo)

        return {"user_db.id = ": user_db.id}
