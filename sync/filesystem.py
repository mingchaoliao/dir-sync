from abc import ABC, abstractmethod
from typing import Callable

from typing.io import BinaryIO

from sync.file import File
from sync.file_collection import FileCollection


class ListFileResponse(ABC):
    is_recursive: bool = False

    def __init__(self, is_recursive: bool = False):
        self.is_recursive = is_recursive

    @abstractmethod
    def next(self) -> FileCollection or None:
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
    def list_files(self, file_id: str, is_recursive: bool = False) -> ListFileResponse:
        pass

    @abstractmethod
    def read_file(self, file_id: str, fh: BinaryIO) -> None:
        pass

    @abstractmethod
    def create_file(self, base_dir: File, file_name: str, downloader: Callable[[BinaryIO], None]) -> File:
        pass

    @abstractmethod
    def create_directory(self, base_dir: File, dir_name: str) -> File:
        pass

    @abstractmethod
    def delete_file(self, file_id: str) -> None:
        pass

    @abstractmethod
    def get_root_dir(self, dir_path: str) -> File:
        pass

    @staticmethod
    @abstractmethod
    def get_filesystem_name() -> str:
        pass
