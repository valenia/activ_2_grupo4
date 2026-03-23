from pydantic import BaseModel


class FileContentInput(BaseModel):
    content_base64: str
