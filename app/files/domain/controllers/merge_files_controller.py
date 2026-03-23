from fastapi import HTTPException

from app.files.domain.bo.merge_input import MergeInput
from app.files.domain.persistences.exceptions import FileNotFoundError, UnauthorizedFileAccessError
from app.files.domain.services.files_services import FilesService


class MergeFilesController:

    def __init__(self, files_service: FilesService):
        self.files_service = files_service

    async def execute(self, user_id: int, input_data: MergeInput):
        try:
            return await self.files_service.merge_files(
                user_id,
                [input_data.file_id_1, input_data.file_id_2],
                input_data.merged_filename,
                None,
            )
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Not found")
        except UnauthorizedFileAccessError:
            raise HTTPException(status_code=403, detail="Forbidden")
