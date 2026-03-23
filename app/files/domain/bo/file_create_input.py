from typing import Optional

from pydantic import BaseModel


class FileCreateInput(BaseModel):
    filename: str
    description: Optional[str] = None
    content_type: Optional[str] = None
