from typing import Callable

from google.oauth2 import service_account
from googleapiclient.discovery import Resource, build
from googleapiclient.http import MediaIoBaseDownload
from typing.io import BinaryIO

from sync.file import File
from sync.filesystem import ListFileResponse, Filesystem
from sync.google_drive.google_drive_list_file_request import GoogleDriveListFileRequest
from sync.google_drive.google_drive_list_file_response import GoogleDriveListFileResponse


class GoogleDriveFilesystem(Filesystem):
    @staticmethod
    def get_filesystem_name() -> str:
        return 'google-drive'

    drive_service: Resource = None

    def __init__(self, drive: Resource):
        self.drive_service = drive

    @staticmethod
    def create(service_account_key_file: str) -> 'GoogleDriveFilesystem':
        """Create Google Drive service from the specified service account key file.

          Args:
            service_account_key_file: string, path to the service account key file.

          Returns:
            A Google Drive Service authenticated from the service account key file.
        """
        credentials = service_account.Credentials.from_service_account_file(service_account_key_file)
        google_drive_service = build('drive', 'v3', credentials=credentials)
        return GoogleDriveFilesystem(google_drive_service)

    def list_files(self, file_id: str, is_recursive: bool = False) -> ListFileResponse:
        return GoogleDriveListFileResponse(self.drive_service, [GoogleDriveListFileRequest(file_id)], is_recursive)

    def read_file(self, file_id: str, fh: BinaryIO) -> None:
        req = self.drive_service.files().get_media(fileId=file_id)
        downloader = MediaIoBaseDownload(fh, req)
        done = False
        while done is False:
            status, done = downloader.next_chunk()

    def has_file(self, file_path: str, md5_checksum: str) -> bool:
        raise Exception('Unimplemented method')  # TODO: Implement this method

    def create_file(self, base_dir: str, file_name: str, downloader: Callable[[BinaryIO], None]) -> File:
        raise Exception('Unimplemented method')  # TODO: Implement this method

    def create_directory(self, base_dir: str, dir_name: str) -> File:
        raise Exception('Unimplemented method')  # TODO: Implement this method

    def delete_file(self, file_id: str) -> None:
        raise Exception('Unimplemented method')  # TODO: Implement this method
