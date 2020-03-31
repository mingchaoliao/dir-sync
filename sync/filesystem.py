import random
import string
from abc import ABC, abstractmethod
from typing import Callable, BinaryIO

from sync.file import File
from sync.file_collection import FileCollection


class ListFileResponse(ABC):
    is_recursive: bool = False

    def __init__(self, is_recursive: bool = False):
        self.is_recursive = is_recursive

    @abstractmethod
    def next(self) -> FileCollection or None:  # pragma: no cover
        pass

    def get_all(self) -> FileCollection:
        files = FileCollection()
        while True:
            f = self.next()
            if f is None:
                break
            files = files + f
        return files


class Filesystem(ABC):
    @abstractmethod
    def list_files(self, file_id: str, is_recursive: bool = False) -> ListFileResponse:  # pragma: no cover
        pass

    @abstractmethod
    def read_file(self, file_id: str) -> str:  # pragma: no cover
        pass

    @abstractmethod
    def create_file(self, base_dir: File, file_name: str, tmp_file_path: str) -> File:  # pragma: no cover
        pass

    @abstractmethod
    def create_directory(self, base_dir: File, dir_name: str) -> File:  # pragma: no cover
        pass

    @abstractmethod
    def delete_file(self, file_id: str) -> None:  # pragma: no cover
        pass

    @abstractmethod
    def get_root_dir(self, dir_path: str) -> File:  # pragma: no cover
        pass

    @staticmethod
    @abstractmethod
    def get_filesystem_name() -> str:  # pragma: no cover
        pass

    def create_tmp_file(self, downloader: Callable[[BinaryIO], None]) -> str:
        letters_and_digits = string.ascii_letters + string.digits
        random_str = ''.join(random.choice(letters_and_digits) for i in range(16))
        tmp_file_path = '/tmp/dir_sync_{}.lock'.format(random_str)
        with open(tmp_file_path, 'wb+') as fh:
            downloader(fh)
        return tmp_file_path
