from typing import List

from sync.file import File


class FileCollection:
    files: List[File] = []

    def __init__(self, files: List[File] = None):
        if files is None:
            files = []
        self.files = files

    def push(self, file: File):
        self.files.append(file)

    def has_file(self, file_id: str, md5_checksum: str) -> bool:
        for file in self.files:
            if file.file_id == file_id:
                if file.get_md5_checksum() == md5_checksum:
                    return True
                return False
        return False
