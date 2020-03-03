from typing import List, Dict

from sync.application_exception import ApplicationException
from sync.file import File


class FileCollection:
    files: List[File] = []

    def __init__(self, files: List[File] = None):
        if files is None:
            files = []
        self.files = files

    def __iter__(self):
        return iter(self.files)

    def push(self, file: File):
        self.files.append(file)

    def has_file(self, file_id: str, md5_checksum: str) -> bool:
        for file in self.files:
            if file.file_id == file_id:
                if file.get_md5_checksum() == md5_checksum:
                    return True
                return False
        return False

    def to_dict_by_file_name(self) -> Dict[str, File]:
        d: Dict[str, File] = {}
        for file in self.files:
            d[file.file_name] = file
        return d

    def __add__(self, other):
        if not isinstance(other, FileCollection):
            raise ApplicationException('Expected {}, got {}.'.format(type(FileCollection), type(other)))
        return FileCollection(self.files + other.files)
