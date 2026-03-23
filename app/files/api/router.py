from fastapi import APIRouter, Header, HTTPException, status

from app.files.dependency_injection.container import (
    get_create_file_controller,
    get_delete_file_controller,
    get_get_file_controller,
    get_list_files_controller,
    get_merge_files_controller,
    get_upload_content_controller,
)
from app.files.domain.bo.file_content_input import FileContentInput
from app.files.domain.bo.file_create_input import FileCreateInput
from app.files.domain.bo.file_detail_desc import FileDetailDesc
from app.files.domain.bo.merge_input import MergeInput

router = APIRouter(tags=["Files"])


def get_user_id(auth: str | None) -> int:
    """Extract user ID from authentication token"""
    if not auth:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    try:
        # Mock auth token to user_id parsing for tests
        return hash(auth) % 10000
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create file metadata",
    description="""
    Creates a new file entry in the system (metadata only).

    **Two-step process:**
    1. This endpoint creates the file record (without content)
    2. Then use `POST /files/{id}` to upload the content

    **Required headers:**
    - `Auth`: Session token obtained from login

    **Input fields:**
    - `filename`: Visible filename (required)
    - `description`: Optional description
    - `content_type`: MIME type (e.g., application/pdf)

    **Response:**
    ID of the created file (use this to upload content later)
    """,
    responses={
        201: {
            "description": "File created successfully",
            "content": {"application/json": {"example": {"id": 42}}},
        },
        401: {
            "description": "Invalid or missing token",
            "content": {"application/json": {"example": {"detail": "Invalid token"}}},
        },
        422: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "filename"],
                                "msg": "field required",
                                "type": "value_error.missing",
                            }
                        ]
                    }
                }
            },
        },
    },
)
async def files_post(input: FileCreateInput, auth: str | None = Header(None)):
    """Create file metadata (no content)"""
    user_id = get_user_id(auth)
    controller = get_create_file_controller()
    return await controller.execute(user_id, input)


@router.get(
    "",
    response_model=list[FileDetailDesc],
    summary="List user files",
    description="""
    Retrieves all files belonging to the authenticated user.

    **Features:**
    - Returns only files owned by the user (filtered by token)
    - Includes basic metadata without content
    - `content_base64` is always `null` in this endpoint

    **Required headers:**
    - `Auth`: Session token obtained from login

    **Response:**
    List of files with summary information (no content)
    """,
    responses={
        200: {
            "description": "List of user files",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "filename": "document.pdf",
                            "has_content": True,
                            "content_type": "application/pdf",
                            "content_base64": None,
                        },
                        {
                            "id": 2,
                            "filename": "image.jpg",
                            "has_content": False,
                            "content_type": "image/jpeg",
                            "content_base64": None,
                        },
                    ]
                }
            },
        },
        401: {
            "description": "Invalid or missing token",
            "content": {"application/json": {"example": {"detail": "Invalid token"}}},
        },
    },
)
async def files_get(auth: str | None = Header(None)):
    """List all files owned by the authenticated user"""
    user_id = get_user_id(auth)
    controller = get_list_files_controller()
    return await controller.execute(user_id)


@router.post(
    "/{file_id}",
    status_code=status.HTTP_200_OK,
    summary="Upload file content",
    description="""
    Uploads content for an existing file.

    **Required headers:**
    - `Auth`: Session token obtained from login

    **Parameters:**
    - `file_id`: ID of the file to upload content to

    **Request body:**
    - `content_base64`: File content encoded in base64

    **Response:**
    Success confirmation
    """,
    responses={
        200: {
            "description": "Content uploaded successfully",
            "content": {"application/json": {"example": {"status": "ok"}}},
        },
        401: {
            "description": "Invalid or missing token",
            "content": {"application/json": {"example": {"detail": "Invalid token"}}},
        },
        403: {
            "description": "Access denied",
            "content": {"application/json": {"example": {"detail": "Unauthorized"}}},
        },
        404: {
            "description": "File not found",
            "content": {"application/json": {"example": {"detail": "File not found"}}},
        },
        422: {
            "description": "Invalid base64",
            "content": {"application/json": {"example": {"detail": "Invalid base64 payload"}}},
        },
    },
)
async def files_id_post(file_id: int, input: FileContentInput, auth: str | None = Header(None)):
    """Upload content for an existing file"""
    user_id = get_user_id(auth)
    controller = get_upload_content_controller()
    return await controller.execute(user_id, file_id, input)


@router.get(
    "/{file_id}",
    response_model=FileDetailDesc,
    summary="Get file by ID",
    description="""
    Retrieves complete file information, including content.

    **Required headers:**
    - `Auth`: Session token obtained from login

    **Parameters:**
    - `file_id`: ID of the file to retrieve

    **Response:**
    - Complete file metadata
    - `content_base64` contains the file content (if exists)
    """,
    responses={
        200: {
            "description": "File found",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "filename": "document.pdf",
                        "has_content": True,
                        "content_type": "application/pdf",
                        "content_base64": "JVBERi0xLjQKJcOkw7zD...",
                    }
                }
            },
        },
        401: {
            "description": "Invalid or missing token",
            "content": {"application/json": {"example": {"detail": "Invalid token"}}},
        },
        403: {
            "description": "Access denied",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
        404: {
            "description": "File not found",
            "content": {"application/json": {"example": {"detail": "Not found"}}},
        },
    },
)
async def files_id_get(file_id: int, auth: str | None = Header(None)):
    """Get a specific file with its content"""
    user_id = get_user_id(auth)
    controller = get_get_file_controller()
    return await controller.execute(user_id, file_id)


@router.delete(
    "/{file_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete file",
    description="""
    Permanently deletes a file.

    **Required headers:**
    - `Auth`: Session token obtained from login

    **Parameters:**
    - `file_id`: ID of the file to delete

    **Important:**
    This operation is irreversible. The file is completely removed from the system.

    **Response:**
    Deletion confirmation
    """,
    responses={
        200: {
            "description": "File deleted",
            "content": {"application/json": {"example": {"status": "deleted"}}},
        },
        401: {
            "description": "Invalid or missing token",
            "content": {"application/json": {"example": {"detail": "Invalid token"}}},
        },
        403: {
            "description": "Access denied",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
        404: {
            "description": "File not found",
            "content": {"application/json": {"example": {"detail": "Not found"}}},
        },
    },
)
async def files_id_delete(file_id: int, auth: str | None = Header(None)):
    """Delete a file permanently"""
    user_id = get_user_id(auth)
    controller = get_delete_file_controller()
    return await controller.execute(user_id, file_id)


@router.post(
    "/merge",
    status_code=status.HTTP_201_CREATED,
    summary="Merge files",
    description="""
    Merges multiple files into a new one.

    **Requirements:**
    - All files must exist and belong to the user
    - All files must have content uploaded

    **Required headers:**
    - `Auth`: Session token obtained from login

    **Input fields:**
    - `file_id_1`: First file ID
    - `file_id_2`: Second file ID
    - `merged_filename`: Name for the merged file

    **Process:**
    1. Validates that both files exist and belong to the user
    2. Merges content in order (first file, then second file)
    3. Creates a new file with the result

    **Response:**
    ID of the newly merged file
    """,
    responses={
        201: {
            "description": "Files merged successfully",
            "content": {"application/json": {"example": {"id": 43}}},
        },
        401: {
            "description": "Invalid or missing token",
            "content": {"application/json": {"example": {"detail": "Invalid token"}}},
        },
        403: {
            "description": "Access denied",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
        404: {
            "description": "File not found",
            "content": {"application/json": {"example": {"detail": "Not found"}}},
        },
        422: {
            "description": "Invalid merge request",
            "content": {
                "application/json": {
                    "example": {"detail": "Both files must have content before merge"}
                }
            },
        },
    },
)
async def files_merge_post(input: MergeInput, auth: str | None = Header(None)):
    """Merge two files into a new one"""
    user_id = get_user_id(auth)
    controller = get_merge_files_controller()
    return await controller.execute(user_id, input)
