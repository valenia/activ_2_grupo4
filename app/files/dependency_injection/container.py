from app.files.domain.controllers.create_file_controller import CreateFileController
from app.files.domain.controllers.delete_file_controller import DeleteFileController
from app.files.domain.controllers.get_file_controller import GetFileController
from app.files.domain.controllers.list_files_controller import ListFilesController
from app.files.domain.controllers.merge_files_controller import MergeFilesController
from app.files.domain.controllers.upload_content_controller import UploadContentController
from app.files.domain.services.files_services import FilesService
from app.files.persistence.files_repository import FilesRepository

# Singletons
_repository = None
_service = None

# Controllers
_create_file_controller = None
_list_files_controller = None
_upload_content_controller = None
_get_file_controller = None
_delete_file_controller = None
_merge_files_controller = None


def get_repository():
    global _repository
    if _repository is None:
        _repository = FilesRepository()
    return _repository


def get_files_service():
    global _service
    if _service is None:
        _service = FilesService(repository=get_repository())
    return _service


def get_create_file_controller():
    global _create_file_controller
    if _create_file_controller is None:
        _create_file_controller = CreateFileController(files_service=get_files_service())
    return _create_file_controller


def get_list_files_controller():
    global _list_files_controller
    if _list_files_controller is None:
        _list_files_controller = ListFilesController(files_service=get_files_service())
    return _list_files_controller


def get_upload_content_controller():
    global _upload_content_controller
    if _upload_content_controller is None:
        _upload_content_controller = UploadContentController(files_service=get_files_service())
    return _upload_content_controller


def get_get_file_controller():
    global _get_file_controller
    if _get_file_controller is None:
        _get_file_controller = GetFileController(files_service=get_files_service())
    return _get_file_controller


def get_delete_file_controller():
    global _delete_file_controller
    if _delete_file_controller is None:
        _delete_file_controller = DeleteFileController(files_service=get_files_service())
    return _delete_file_controller


def get_merge_files_controller():
    global _merge_files_controller
    if _merge_files_controller is None:
        _merge_files_controller = MergeFilesController(files_service=get_files_service())
    return _merge_files_controller
