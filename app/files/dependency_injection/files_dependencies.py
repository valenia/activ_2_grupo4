from app.files.domain.files_service import FilesService
from app.files.persistence.files_repository import FilesRepository


def get_files_repository():
    return FilesRepository()


def get_files_service():
    repository = get_files_repository()
    return FilesService(repository)