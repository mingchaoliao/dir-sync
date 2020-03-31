from pytest import raises

from sync.application_exception import ApplicationException
from sync.google_drive.google_drive_filesystem import GoogleDriveFilesystem
from sync.google_drive.google_drive_filesystem_factory import GoogleDriveFilesystemFactory


class TestGoogleDriveFilesystemFactory:
    def test_get_fs_name(self):
        assert GoogleDriveFilesystemFactory.get_filesystem_name() == GoogleDriveFilesystem.get_filesystem_name()

    def test_create_fs_from_service_account_key_file(self, mocker):
        mocker.patch.object(GoogleDriveFilesystem, 'create')
        GoogleDriveFilesystemFactory.create({
            'auth_key_file': 'path/to/key.json'
        })
        GoogleDriveFilesystem.create.assert_called_once_with('path/to/key.json')

    def test_try_to_create_fs_without_enough_information(self):
        with raises(ApplicationException):
            GoogleDriveFilesystemFactory.create({})
