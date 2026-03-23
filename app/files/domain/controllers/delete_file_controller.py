from fastapi import HTTPException

from app.files.domain.persistences.exceptions import FileNotFoundError, UnauthorizedFileAccessError
from app.files.domain.services.files_services import FilesService


class DeleteFileController:

    def __init__(self, files_service: FilesService):
        self.files_service = files_service

    async def execute(self, user_id: int, file_id: int):
        try:
            await self.files_service.delete_file(user_id, file_id)
            return {"status": "deleted"}
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Not found")
        except UnauthorizedFileAccessError:
            raise HTTPException(status_code=403, detail="Forbidden")
