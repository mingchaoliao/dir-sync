from abc import ABC, abstractmethod
from typing import Tuple, Callable

from typing.io import BinaryIO

from sync.file_collection import FileCollection


class ListFileResponse(ABC):
    @abstractmethod
    def next(self) -> FileCollection or None:
        pass


class Filesystem(ABC):
    @abstractmethod
    def list_files(self, file_id: str) -> ListFileResponse:
        pass

    @abstractmethod
    def read_file(self, file_id: str, fh: BinaryIO) -> None:
        pass

    @abstractmethod
    def create_file(self, file_path: str, downloader: Callable[[BinaryIO], None]):
        pass

    @abstractmethod
    def delete_file(self, file_id: str) -> None:
        pass

    @abstractmethod
    def has_file(self, file_path: str, md5_checksum: str) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def get_filesystem_name() -> str:
        pass
