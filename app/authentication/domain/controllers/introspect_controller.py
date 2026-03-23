from fastapi import HTTPException, status

from app.authentication.domain.bo.introspect_output import IntrospectOutput
from app.authentication.persistence.user_repository import get_user_by_email


class IntrospectController:
    """Controller for token introspection"""

    def __init__(self, login_controller):
        self.login_controller = login_controller

    async def execute(self, token: str) -> IntrospectOutput:
        """Execute introspect logic"""
        if token not in self.login_controller.sessions_db:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        email = self.login_controller.sessions_db[token]
        user_db = await get_user_by_email(email)

        if user_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return IntrospectOutput(
            username=user_db.username, email=user_db.email, address=user_db.address
        )
