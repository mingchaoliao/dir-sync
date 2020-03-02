class GoogleDriveListFileRequest:
    directory_id: str = None
    fields: str = "nextPageToken, files(id, name, md5Checksum, mimeType)"
    page_size: int = 10
    page_token: str = None

    def __init__(self, directory_id: str, page_token: str = None, page_size: int = 10):
        self.directory_id = directory_id
        self.page_size = page_size
        self.page_token = page_token
