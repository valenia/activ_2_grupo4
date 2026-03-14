from fastapi import APIRouter

router = APIRouter()

# Local dictrionary to store theoretical files
files_db = {}        # {file_id: {"name": str, "user_id": int, "description": str, "content": str}}
file_id_counter = 1

@router.get("")
async def files_get() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/{id}")
async def files_id_get(id: int) -> dict[str, int]:
    return {"status": id}


@router.post("/{id}")
async def files_id_post(id: str) -> dict[str, str]:
    return {"status": id}


@router.delete("/{id}")
async def files_id_post(id: str) -> dict[str, int]:
    return {"status": id}
