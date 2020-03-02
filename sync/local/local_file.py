from sync.file import File
from os import path
from hashlib import md5


class LocalFile(File):
    def __init__(self, file_path: str):
        dirname, filename = path.split(file_path)
        super().__init__(file_path, file_path, filename)

    def get_md5_checksum(self) -> str:
        md5_checksum = md5()
        with open(self.file_path, 'rb') as fh:
            for block in iter(lambda: fh.read(4096), b""):
                md5_checksum.update(block)
        return md5_checksum.hexdigest()
