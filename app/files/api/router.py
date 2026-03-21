from fastapi import APIRouter, Depends, Header, HTTPException

from app.files.dependency_injection.files_dependencies import get_files_service
from app.files.domain.exceptions import (
    FileNotFoundError,
    UnauthorizedFileAccessError,
)
from app.files.domain.files_service import FilesService
from app.files.domain.schemas import (
    CreateFileRequest,
    UploadFileContentRequest,
    MergeFilesRequest,
)

router = APIRouter(tags=["files"])


def get_current_owner_external_id(auth: str = Header(..., alias="Auth")):
    if not auth:
        raise HTTPException(status_code=401, detail="Missing Auth header")
    return 1


@router.get("")
async def list_files(
    service: FilesService = Depends(get_files_service),
    owner_external_id: int = Depends(get_current_owner_external_id),
):
    files = await service.list_files(owner_external_id)

    return [
        {
            "id": file_obj.id,
            "owner_external_id": file_obj.owner_external_id,
            "filename": file_obj.filename,
            "description": file_obj.description,
            "mime_type": file_obj.mime_type,
            "content": file_obj.content,
        }
        for file_obj in files
    ]


@router.post("")
async def create_file(
    request: CreateFileRequest,
    service: FilesService = Depends(get_files_service),
    owner_external_id: int = Depends(get_current_owner_external_id),
):
    file_obj = await service.create_file(
        owner_external_id=owner_external_id,
        filename=request.filename,
        description=request.description,
        mime_type=request.mime_type,
    )
    return {"id": file_obj.id}


@router.get("/{file_id}")
async def get_file(
    file_id: int,
    service: FilesService = Depends(get_files_service),
    owner_external_id: int = Depends(get_current_owner_external_id),
):
    try:
        file_obj = await service.get_file(owner_external_id, file_id)
        return {
            "id": file_obj.id,
            "owner_external_id": file_obj.owner_external_id,
            "filename": file_obj.filename,
            "description": file_obj.description,
            "mime_type": file_obj.mime_type,
            "content": file_obj.content,
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except UnauthorizedFileAccessError:
        raise HTTPException(status_code=403, detail="Forbidden")


@router.post("/{file_id}")
async def upload_file_content(
    file_id: int,
    request: UploadFileContentRequest,
    service: FilesService = Depends(get_files_service),
    owner_external_id: int = Depends(get_current_owner_external_id),
):
    try:
        file_obj = await service.upload_content(
            owner_external_id=owner_external_id,
            file_id=file_id,
            content=request.content,
        )
        return {"id": file_obj.id, "message": "Content uploaded"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except UnauthorizedFileAccessError:
        raise HTTPException(status_code=403, detail="Forbidden")


@router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    service: FilesService = Depends(get_files_service),
    owner_external_id: int = Depends(get_current_owner_external_id),
):
    try:
        await service.delete_file(owner_external_id, file_id)
        return {"message": "File deleted"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except UnauthorizedFileAccessError:
        raise HTTPException(status_code=403, detail="Forbidden")


@router.post("/merge")
async def merge_files(
    request: MergeFilesRequest,
    service: FilesService = Depends(get_files_service),
    owner_external_id: int = Depends(get_current_owner_external_id),
):
    try:
        file_obj = await service.merge_files(
            owner_external_id=owner_external_id,
            file_ids=request.file_ids,
            filename=request.filename,
            description=request.description,
        )
        return {"id": file_obj.id, "message": "Files merged"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except UnauthorizedFileAccessError:
        raise HTTPException(status_code=403, detail="Forbidden")