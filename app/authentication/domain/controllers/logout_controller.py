from fastapi import HTTPException, status


class LogoutController:
    """Controller for user logout"""

    def __init__(self, login_controller):
        self.login_controller = login_controller

    async def execute(self, token: str) -> dict:
        """Execute logout logic"""
        if token not in self.login_controller.sessions_db:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        del self.login_controller.sessions_db[token]
        return {"status": "ok"}
