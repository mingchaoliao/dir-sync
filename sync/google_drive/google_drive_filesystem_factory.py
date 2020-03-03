from typing import Dict

from sync.application_exception import ApplicationException
from sync.filesystem import Filesystem
from sync.filesystem_factory import FilesystemFactory
from sync.google_drive.google_drive_filesystem import GoogleDriveFilesystem


class GoogleDriveFilesystemFactory(FilesystemFactory):
    @staticmethod
    def create(args: Dict) -> Filesystem:
        if 'auth_key_file' in args:
            return GoogleDriveFilesystem.create(args['auth_key_file'])

        raise ApplicationException('Unable to connect to Google Drive: un-sufficient parameters.')

    @staticmethod
    def get_filesystem_name() -> str:
        return GoogleDriveFilesystem.get_filesystem_name()
