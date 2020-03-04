from os import path

from google.oauth2 import service_account
from googleapiclient.discovery import Resource, build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from typing.io import BinaryIO

from sync.file import File
from sync.filesystem import ListFileResponse, Filesystem
from sync.google_drive.google_drive_file import GoogleDriveFile
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

    def read_file(self, file_id: str) -> str:
        def download(fid: str, fh: BinaryIO):
            req = self.drive_service.files().get_media(fileId=fid)
            downloader = MediaIoBaseDownload(fh, req)
            done = False
            while done is False:
                status, done = downloader.next_chunk()

        return self.create_tmp_file(lambda fh: download(file_id, fh))

    def create_file(self, base_dir: File, file_name: str, tmp_file_path: str) -> File:
        file_metadata = {
            'name': file_name,
            'parents': [base_dir.file_id]
        }

        res = self.drive_service.files().create(
            body=file_metadata,
            media_body=MediaFileUpload(tmp_file_path, resumable=True),
            fields='id, mimeType, md5Checksum'
        ).execute()

        return GoogleDriveFile(
            res.get('id'),
            path.join(base_dir.file_path, file_name),
            file_name,
            res.get('mimeType'),
            res.get('md5Checksum')
        )

    def create_directory(self, base_dir: File, dir_name: str) -> File:
        dir_mime = 'application/vnd.google-apps.folder'
        file_metadata = {
            'name': dir_name,
            'mimeType': dir_mime,
            'parents': [base_dir.file_id]
        }
        res = self.drive_service.files().create(body=file_metadata, fields='id').execute()
        return GoogleDriveFile(
            res.get('id'),
            path.join(base_dir.file_path, dir_name),
            dir_name,
            dir_mime,
            None
        )

    def delete_file(self, file_id: str) -> None:
        self.drive_service.files().delete(fileId=file_id).execute()

    def get_root_dir(self, dir_path: str) -> File:
        return GoogleDriveFile(dir_path, '.', 'root', 'application/vnd.google-apps.folder', None)
