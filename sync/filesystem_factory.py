from abc import ABC, abstractmethod
from typing import Dict

from sync.filesystem import Filesystem


class FilesystemFactory(ABC):
    @staticmethod
    @abstractmethod
    def create(args: Dict) -> Filesystem:
        pass

    @staticmethod
    @abstractmethod
    def get_filesystem_name() -> str:
        pass
