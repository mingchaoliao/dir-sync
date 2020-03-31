from abc import ABC, abstractmethod


class File(ABC):
    file_id: str = None
    file_path: str = None
    file_name: str = None

    def __init__(self, file_id: str, file_path: str, file_name: str):
        self.file_id = file_id
        self.file_path = file_path
        self.file_name = file_name

    @abstractmethod
    def get_md5_checksum(self) -> str:  # pragma: no cover
        """Get md5 checksum of the file.

          Returns:
              A string representation of md5 checksum of the file.
        """
        pass

    @abstractmethod
    def is_dir(self) -> bool:  # pragma: no cover
        pass

    @abstractmethod
    def get_relative_path(self, base_path: str) -> str:  # pragma: no cover
        pass
