from sync.file import File


class GoogleDriveFile(File):
    mime_type: str = None
    md5_checksum: str = None

    def __init__(self, file_id: str, file_path: str, file_name: str, mime_type: str, md5_checksum: str or None):
        super().__init__(file_id, file_path, file_name)
        self.mime_type = mime_type
        self.md5_checksum = md5_checksum

    def get_md5_checksum(self) -> str:
        return self.md5_checksum

    def is_dir(self) -> bool:
        return self.mime_type == 'application/vnd.google-apps.folder'

    def get_relative_path(self, base_path: str) -> str:
        return self.file_path

