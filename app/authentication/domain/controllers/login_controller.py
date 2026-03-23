import uuid

from fastapi import HTTPException, status

from app.authentication.domain.bo.login_input import LoginInput
from app.authentication.domain.services.hashing_password_service import HashingPasswordService
from app.authentication.persistence.user_repository import get_user_by_email


class LoginController:
    """Controller for user login"""

    def __init__(self):
        self.hashing_service = HashingPasswordService()
        self.sessions_db: dict[str, str] = {}  # token -> email

    async def execute(self, input_data: LoginInput) -> dict:
        """Execute login logic"""
        # Get user from database
        user_db = await get_user_by_email(input_data.email)

        if user_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Email not registered"
            )

        # Verify password
        if not self.hashing_service.verify(input_data.password, user_db.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
            )

        # Generate session token
        token = str(uuid.uuid4())
        while token in self.sessions_db:
            token = str(uuid.uuid4())

        self.sessions_db[token] = input_data.email

        return {"auth": token}

    def get_session_email(self, token: str) -> str:
        """Get email from session token"""
        return self.sessions_db.get(token)
