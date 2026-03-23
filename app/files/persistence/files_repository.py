from app.files.models import StoredFile


class FilesRepository:
    async def list_by_owner(self, owner_external_id: int):
        return await StoredFile.filter(owner_external_id=owner_external_id)

    async def create_file(
        self,
        owner_external_id: int,
        filename: str,
        description: str | None,
        mime_type: str | None,
    ):
        return await StoredFile.create(
            owner_external_id=owner_external_id,
            filename=filename,
            description=description,
            mime_type=mime_type,
        )

    async def get_file_by_id(self, file_id: int):
        return await StoredFile.get_or_none(id=file_id)

    async def save(self, file_obj: StoredFile):
        await file_obj.save()
        return file_obj

    async def delete(self, file_obj: StoredFile):
        await file_obj.delete()
