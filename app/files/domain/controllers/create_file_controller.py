from app.files.domain.bo.file_create_input import FileCreateInput
from app.files.domain.services.files_services import FilesService


class CreateFileController:

    def __init__(self, files_service: FilesService):
        self.files_service = files_service

    async def execute(self, user_id: int, input_data: FileCreateInput):
        return await self.files_service.create_file(
            user_id, input_data.filename, input_data.description, input_data.content_type
        )
