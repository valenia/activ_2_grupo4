from typing import Optional

from pydantic import BaseModel


class FileDetailDesc(BaseModel):
    id: int
    filename: str
    has_content: bool
    content_type: Optional[str] = None
    content_base64: Optional[str] = None
