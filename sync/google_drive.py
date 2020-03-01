from typing import Tuple, List, BinaryIO

from google.oauth2 import service_account
from googleapiclient.discovery import Resource, build
from googleapiclient.http import MediaIoBaseDownload

from sync.google_drive_file import GoogleDriveFile


class GoogleDrive:
    drive: Resource = None

    def __init__(self, drive: Resource):
        self.drive = drive

    @staticmethod
    def create(service_account_key_file: str) -> 'GoogleDrive':
        """Create Google Drive service from the specified service account key file.

          Args:
            service_account_key_file: string, path to the service account key file.

          Returns:
            A Google Drive Service authenticated from the service account key file.
        """
        credentials = service_account.Credentials.from_service_account_file(service_account_key_file)
        drive = build('drive', 'v3', credentials=credentials)
        return GoogleDrive(drive)

    def list(self, folder_id: str, next_page_token: str = None, page_size: int = 10) -> Tuple[
        List[GoogleDriveFile], str]:
        """List files (including directories) in the Google Drive folder.

          Args:
            folder_id: string, Google Drive directory ID.
            next_page_token: string, The token for continuing a previous list request
              on the next page. This should be set to the value of 'nextPageToken' from
              the previous response. It can be None.
            page_size: string, The maximum number of files to return per page. Partial or
              empty result pages are possible even before the end of the files list has been
              reached. Acceptable values are 1 to 1000, inclusive. (Default: 10)

          Returns:
            A list of GoogleDriveFile in the directory.
        """
        res = self.drive.files().list(
            pageToken=next_page_token,
            pageSize=page_size,
            fields="nextPageToken, files(id, name, md5Checksum, mimeType)",
            q="'{}' in parents".format(folder_id)
        ).execute()

        next_page_token: str = res['nextPageToken'] if 'nextPageToken' in res else None
        files = list(map(lambda x: GoogleDriveFile(
            x['id'],
            x['name'],
            x['mimeType'],
            x['md5Checksum'] if 'md5Checksum' in x else None
        ), res['files']))

        return files, next_page_token

    def download(self, fid: str, fh: BinaryIO) -> None:
        """Download file.

          Args:
            fid: string, Google Drive file ID.
            fh: BinaryIO, a stream where the downloaded file should go
        """
        req = self.drive.files().get_media(fileId=fid)
        downloader = MediaIoBaseDownload(fh, req)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
