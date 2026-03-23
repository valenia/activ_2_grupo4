from fastapi import HTTPException

from app.files.domain.bo.file_detail_desc import FileDetailDesc
from app.files.domain.persistences.exceptions import FileNotFoundError, UnauthorizedFileAccessError
from app.files.domain.services.files_services import FilesService


class GetFileController:

    def __init__(self, files_service: FilesService):
        self.files_service = files_service

    async def execute(self, user_id: int, file_id: int):
        try:
            file_obj = await self.files_service.get_file(user_id, file_id)
            return FileDetailDesc(
                id=file_obj.id,
                filename=file_obj.filename,
                has_content=bool(file_obj.content),
                content_type=file_obj.mime_type,
                content_base64=file_obj.content,
            )
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Not found")
        except UnauthorizedFileAccessError:
            raise HTTPException(status_code=403, detail="Forbidden")
