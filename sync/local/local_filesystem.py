from os import path, mkdir, rename, remove, rmdir
from typing import Callable

from typing.io import BinaryIO

from sync.filesystem import Filesystem
from sync.local.local_list_file_response import LocalListFileResponse
from sync.local.utils import Utils


class LocalFilesystem(Filesystem):
    @staticmethod
    def get_filesystem_name() -> str:
        return 'local'

    def list_files(self, file_id: str) -> LocalListFileResponse:
        return LocalListFileResponse([file_id])

    def read_file(self, file_id: str, fh: BinaryIO) -> None:
        with open(file_id, 'rb') as read_fh:
            byte = read_fh.read()
            while byte:
                fh.write(byte)
                byte = read_fh.read()

    def has_file(self, file_path: str, md5_checksum: str) -> bool:
        if not path.isfile(file_path):
            return False

        if md5_checksum != Utils.cal_md5_checksum(file_path):
            return False

        return True

    def create_file(self, file_path: str, downloader: Callable[[BinaryIO], None]):
        base_dir, filename = path.split(file_path)
        tmp_file_path = path.join(base_dir, filename + '.lock')
        if not path.exists(base_dir):
            mkdir(base_dir)
        try:
            with open(tmp_file_path, 'wb+') as fh:
                downloader(fh)
            rename(tmp_file_path, file_path)
        except Exception:
            if path.exists(tmp_file_path):
                remove(tmp_file_path)

    def delete_file(self, file_id: str) -> None:
        if path.isdir(file_id):
            rmdir(file_id)
        elif path.isfile(file_id):
            remove(file_id)
