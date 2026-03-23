from fastapi import HTTPException

from app.files.domain.bo.file_content_input import FileContentInput
from app.files.domain.persistences.exceptions import FileNotFoundError, UnauthorizedFileAccessError
from app.files.domain.services.files_services import FilesService


class UploadContentController:

    def __init__(self, files_service: FilesService):
        self.files_service = files_service

    async def execute(self, user_id: int, file_id: int, input_data: FileContentInput):
        try:
            await self.files_service.upload_content(user_id, file_id, input_data.content_base64)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="File not found")
        except UnauthorizedFileAccessError:
            raise HTTPException(status_code=403, detail="Unauthorized")

        return {"status": "ok"}
