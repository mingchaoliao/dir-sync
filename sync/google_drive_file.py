import json


class GoogleDriveFile:
    # Google Drive file ID
    fid = None
    # file name
    name = None
    # file mime type
    mime = None
    # md5 checksum of the file. The value can be None
    # if it is a directory
    md5 = None

    def __init__(self, fid: str, name: str, mime: str, md5: str = None):
        self.fid = fid
        self.name = name
        self.mime = mime
        self.md5 = md5

    def __str__(self):
        return json.dumps({
            "fid": self.fid,
            "name": self.name,
            "mine": self.mime,
            "md5": self.md5,
            "is_dir": self.is_dir()
        })

    def is_dir(self) -> bool:
        """Check if the file is a directory.

          Returns:
              True: if the file is a directory
              False: if the file is not a directory
        """
        return self.mime == 'application/vnd.google-apps.folder'
