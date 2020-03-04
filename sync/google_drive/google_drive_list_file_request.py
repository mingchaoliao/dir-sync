class GoogleDriveListFileRequest:
    directory_id: str = None
    base_directory: str = None
    fields: str = "nextPageToken, files(id, name, md5Checksum, mimeType)"
    page_size: int = 10
    page_token: str = None

    def __init__(self, directory_id: str, base_directory: str = '.', page_token: str = None, page_size: int = 10):
        self.directory_id = directory_id
        self.base_directory = base_directory
        self.page_size = page_size
        self.page_token = page_token
