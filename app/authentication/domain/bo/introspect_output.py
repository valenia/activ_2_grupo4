from typing import Optional

from pydantic import BaseModel


class IntrospectOutput(BaseModel):
    username: str
    email: str
    address: Optional[str] = None
