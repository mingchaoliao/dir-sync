from argparse import ArgumentParser

import sync
from sync.application_exception import ApplicationException
from sync.dir_sync_service import DirSyncService
from sync.google_drive.google_drive_filesystem_factory import GoogleDriveFilesystemFactory
from sync.local.local_filesystem_factory import LocalFilesystemFactory


class DirSyncCommand:
    dir_sync_service: DirSyncService = None

    def __init__(self, dir_sync_service: DirSyncService):
        self.dir_sync_service = dir_sync_service

    def handle(self):
        self.dir_sync_service.register_filesystem_factories(LocalFilesystemFactory)
        self.dir_sync_service.register_filesystem_factories(GoogleDriveFilesystemFactory)

        available_filesystem_names = self.dir_sync_service.get_available_filesystem_names()

        # command setup
        parser = ArgumentParser(
            description='Sync files in the local folder with files in the remote location, e.g. Google Drive.',
            prog='Google Drive Sync'
        )
        parser.add_argument('--version', help='Print version of this program.', action='version',
                            version='Version: {}'.format(sync.VERSION))
        parser.add_argument('--src-type', required=True, help='Source type.', choices=available_filesystem_names)
        parser.add_argument('--dst-type', required=True, help='Destination type.', choices=available_filesystem_names)
        parser.add_argument('--src', required=True, help='Source directory path. The value depends on the source type.')
        parser.add_argument('--dst', required=True,
                            help='Destination directory path. The value depends on the source type.')
        parser.add_argument('--auth-key-file', required=True, help='Path to auth key file.')
        args = vars(parser.parse_args())

        self.dir_sync_service.run(args)
