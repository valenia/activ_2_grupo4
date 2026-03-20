from pydantic import BaseModel
from typing import List


class CreateFileRequest(BaseModel):
    filename: str
    description: str | None = None
    mime_type: str | None = None


class UploadFileContentRequest(BaseModel):
    content: str


class MergeFilesRequest(BaseModel):
    file_ids: List[int]
    filename: str
    description: str | None = None