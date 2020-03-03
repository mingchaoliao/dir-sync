from os import scandir, DirEntry
from typing import List

from sync.file_collection import FileCollection
from sync.filesystem import ListFileResponse
from sync.local.local_file import LocalFile


class LocalListFileResponse(ListFileResponse):
    dirs: List[str] = []

    def __init__(self, dirs: List[str]):
        self.dirs = dirs

    def next(self) -> FileCollection or None:
        if len(self.dirs) == 0:
            return None

        files = FileCollection()
        dirs = []
        scanned_files: List[DirEntry] = scandir(self.dirs.pop())
        for scanned_file in scanned_files:
            if scanned_file.is_file():
                files.push(LocalFile(scanned_file.path))
            elif scanned_file.is_dir():
                dirs.append(scanned_file.path)
        self.dirs = self.dirs + dirs
        return files
