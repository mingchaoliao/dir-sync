from os import path, mkdir, rename, remove, rmdir
from typing import Callable

from typing.io import BinaryIO

from sync.application_exception import ApplicationException
from sync.file import File
from sync.filesystem import Filesystem
from sync.local.local_file import LocalFile
from sync.local.local_list_file_response import LocalListFileResponse
from sync.local.utils import Utils


class LocalFilesystem(Filesystem):
    @staticmethod
    def get_filesystem_name() -> str:
        return 'local'

    def list_files(self, file_id: str, is_recursive: bool = False) -> LocalListFileResponse:
        return LocalListFileResponse([file_id], is_recursive)

    def read_file(self, file_id: str, fh: BinaryIO) -> None:
        with open(file_id, 'rb') as read_fh:
            for block in iter(lambda: read_fh.read(4096), b""):
                fh.write(block)

    def create_file(self, base_dir: File, file_name: str, downloader: Callable[[BinaryIO], None]) -> File:
        file_path = path.join(base_dir.file_path, file_name)
        tmp_file_path = path.join(base_dir.file_path, file_name + '.lock')
        try:
            with open(tmp_file_path, 'wb+') as fh:
                downloader(fh)
            rename(tmp_file_path, file_path)
            return LocalFile(file_path, False)
        except Exception:
            if path.exists(tmp_file_path):
                remove(tmp_file_path)
            raise ApplicationException('Unable to create file at {}'.format(file_path))

    def create_directory(self, base_dir: File, dir_name: str) -> File:
        dir_path = path.join(base_dir.file_path, dir_name)
        mkdir(dir_path)
        return LocalFile(dir_path, True)

    def delete_file(self, file_id: str) -> None:
        if path.isdir(file_id):
            rmdir(file_id)
        elif path.isfile(file_id):
            remove(file_id)

    def get_root_dir(self, dir_path: str) -> File:
        return LocalFile(dir_path, True)
