from abc import ABC, abstractmethod
from typing import Tuple, Callable

from typing.io import BinaryIO

from sync.file_collection import FileCollection


class ListFileResponse(ABC):
    @abstractmethod
    def get_files(self) -> Tuple[FileCollection, 'ListFileResponse']:
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

    @staticmethod
    @abstractmethod
    def get_filesystem_name() -> str:
        pass
