from hashlib import md5
from os import DirEntry, scandir, path, mkdir, remove, rename, rmdir
from typing import List, Dict, Callable, BinaryIO


class LocalFS:
    root_path: str = None
    cached_path_md5_dict: Dict[str, str] = None

    def __init__(self, root_path: str):
        self.root_path = root_path

    def get_all_files(self, dir_path: str) -> List[DirEntry]:
        """Get all file in the specified directory recursively.

          Get all file in the specified directory recursively. (including files in
          the sub-directory).

          Args:
            dir_path: string, path of the directory.

          Returns:
            A list of files (without directory) in the dir_path (including files in
            the sub-directories).
        """
        files: List[DirEntry] = []
        all_files: List[DirEntry] = scandir(dir_path)
        for file in all_files:
            if file.is_file():
                files.append(file)
            elif file.is_dir():
                files = files + self.get_all_files(file.path)
        return files

    def cal_md5_checksum(self, file_path: str) -> str:
        """Calculate md5 checksum of the specified file.

          Args:
            file_path: string, path of the file.

          Returns:
            md5 checksum string of the file.
        """
        md5_checksum = md5()
        with open(file_path, 'rb') as fh:
            for block in iter(lambda: fh.read(4096), b""):
                md5_checksum.update(block)
        return md5_checksum.hexdigest()

    def build_dict_path_md5(self) -> Dict[str, str]:
        """Create a dictionary for lookup.

          Create a dictionary for lookup for all files in the root_path,
          put file_path -> md5_checksum in the dictionary.

          Returns:
            A dictionary of file_path -> md5_checksum.
        """
        if self.cached_path_md5_dict is None:
            path_md5_dict: Dict[str, str] = {}
            files = self.get_all_files(self.root_path)
            for file in files:
                path_md5_dict[file.path] = self.cal_md5_checksum(file.path)
            self.cached_path_md5_dict = path_md5_dict

        return self.cached_path_md5_dict

    def is_file_existed(self, file_path: str, md5_checksum: str):
        """Check if the file exists, with the exactly same md5 checksum.

          Args:
            file_path: string, path of the file.
            md5_checksum: string, expected md5 checksum.

          Returns:
            True: if the file at file_path exists and its md5 checksum matches md5_checksum.
            False: if the file at file_path does not exists, or the file has a different
              md5 checksum with the expected one.
        """
        path_md5_dict = self.build_dict_path_md5()
        if file_path not in path_md5_dict:
            return False
        if path_md5_dict[file_path] != md5_checksum:
            return False
        return True

    def create_file(self, file_path: str, downloader: Callable[[BinaryIO], None]):
        """Create a file at file_path with the content from the specified remote stream.

          Create a file at file_path with the content from the specified remote stream.
          It creates a temporary file, and then rename it to the final file_path. The temporary
          file will be deleted if the process fails.

          Args:
            file_path: string, path of the file.
            downloader: Callable[[BinaryIO], None], a callback function accepts the file
              handler (BinaryIO) pointed to the temporary file path

          Returns:
            True: if the file at file_path exists and its md5 checksum matches md5_checksum.
            False: if the file at file_path does not exists, or the file has a different
              md5 checksum with the expected one.
        """
        base_dir, filename = path.split(file_path)
        tmp_file_path = path.join(base_dir, filename + '.lock')
        if not path.exists(base_dir):
            mkdir(base_dir)
        try:
            with open(tmp_file_path, 'wb+') as fh:
                downloader(fh)
            rename(tmp_file_path, file_path)
        except Exception:
            if path.exists(tmp_file_path):
                remove(tmp_file_path)

    def delete_file(self, file_path: str):
        """Delete file/directory at specified location.

          Args:
            file_path: string, path to the file/directory.
        """
        if path.isdir(file_path):
            rmdir(file_path)
        elif path.isfile(file_path):
            remove(file_path)
