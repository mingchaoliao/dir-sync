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

    def to_dict_by_file_name(self) -> Dict[str, File]:
        d: Dict[str, File] = {}
        for file in self.files:
            d[file.file_name] = file
        return d

    def __add__(self, other):
        if not isinstance(other, FileCollection):
            raise ApplicationException('Expected {}, got {}.'.format(type(FileCollection), type(other)))
        return FileCollection(self.files + other.files)
