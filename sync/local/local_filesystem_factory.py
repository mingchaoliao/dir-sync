from typing import Dict

from sync.filesystem import Filesystem
from sync.filesystem_factory import FilesystemFactory
from sync.local.local_filesystem import LocalFilesystem


class LocalFilesystemFactory(FilesystemFactory):
    @staticmethod
    def create(args: Dict) -> Filesystem:
        return LocalFilesystem()

    @staticmethod
    def get_filesystem_name() -> str:
        return LocalFilesystem.get_filesystem_name()
