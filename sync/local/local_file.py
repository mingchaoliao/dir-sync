from os import path

from sync.file import File
from sync.local.utils import Utils


class LocalFile(File):
    md5_checksum: str = None
    isdir: bool = False

    def __init__(self, file_path: str, isdir: bool):
        dirname, filename = path.split(file_path)
        super().__init__(file_path, file_path, filename)
        self.isdir = isdir

    def get_md5_checksum(self) -> str:
        if self.md5_checksum is None:
            self.md5_checksum = Utils.cal_md5_checksum(self.file_path)

        return self.md5_checksum

    def is_dir(self) -> bool:
        return self.isdir

    def get_relative_path(self, base_path: str) -> str:
        return path.relpath(self.file_path, base_path)
