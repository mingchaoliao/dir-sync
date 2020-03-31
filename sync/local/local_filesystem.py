from os import path, mkdir, remove
from shutil import rmtree
from shutil import move

from sync.file import File
from sync.filesystem import Filesystem
from sync.local.local_file import LocalFile
from sync.local.local_list_file_response import LocalListFileResponse


class LocalFilesystem(Filesystem):
    @staticmethod
    def get_filesystem_name() -> str:
        return 'local'

    def list_files(self, file_id: str, is_recursive: bool = False) -> LocalListFileResponse:
        return LocalListFileResponse([file_id], is_recursive)

    def read_file(self, file_id: str) -> str:
        return file_id

    def create_file(self, base_dir: File, file_name: str, tmp_file_path: str) -> File:
        file_path = path.join(base_dir.file_path, file_name)
        if not path.isfile(file_path) or not path.samefile(file_path, tmp_file_path):
            move(tmp_file_path, file_path)
        return LocalFile(file_path, False)

    def create_directory(self, base_dir: File, dir_name: str) -> File:
        dir_path = path.join(base_dir.file_path, dir_name)
        mkdir(dir_path)
        return LocalFile(dir_path, True)

    def delete_file(self, file_id: str) -> None:
        if path.isdir(file_id):
            rmtree(file_id)
        elif path.isfile(file_id):
            remove(file_id)

    def get_root_dir(self, dir_path: str) -> File:
        return LocalFile(dir_path, True)
