from typing import Optional

from pydantic import BaseModel


class RegisterInput(BaseModel):
    username: str
    email: str
    address: Optional[str] = None
    password: str
