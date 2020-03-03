from os import path

from sync.file import File
from sync.local.utils import Utils


class LocalFile(File):
    md5_checksum: str = None

    def __init__(self, file_path: str):
        dirname, filename = path.split(file_path)
        super().__init__(file_path, file_path, filename)

    def get_md5_checksum(self) -> str:
        if self.md5_checksum is None:
            self.md5_checksum = Utils.cal_md5_checksum(self.file_path)

        return self.md5_checksum
