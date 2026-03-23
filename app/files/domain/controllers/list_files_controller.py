from app.files.domain.bo.file_detail_desc import FileDetailDesc
from app.files.domain.services.files_services import FilesService


class ListFilesController:

    def __init__(self, files_service: FilesService):
        self.files_service = files_service

    async def execute(self, user_id: int):
        items = await self.files_service.list_files(user_id)
        return [
            FileDetailDesc(
                id=item.id,
                filename=item.filename,
                has_content=bool(item.content),
                content_type=item.mime_type,
                content_base64=None,
            )
            for item in items
        ]
