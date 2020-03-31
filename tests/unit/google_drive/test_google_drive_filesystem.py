from unittest.mock import MagicMock

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import Resource
from googleapiclient.http import MediaFileUpload

from sync.google_drive.google_drive_file import GoogleDriveFile
from sync.google_drive.google_drive_filesystem import GoogleDriveFilesystem
from sync.google_drive.google_drive_list_file_response import GoogleDriveListFileResponse


class TestGoogleDriveFilesystem:
    def test_fs_name_is_google_drive(self):
        assert GoogleDriveFilesystem.get_filesystem_name() == 'google-drive'

    def test_create_fs_from_service_key_file(self, mocker):
        credential = MagicMock(spec=Credentials)
        from_service_account_file = mocker.patch('google.oauth2.service_account.Credentials.from_service_account_file',
                                                 return_value=credential)

        service = MagicMock(spec=Resource)
        build = mocker.patch('googleapiclient.discovery.build', return_value=service)

        fs = GoogleDriveFilesystem.create('key.json')

        from_service_account_file.assert_called_once_with('key.json')
        build.assert_called_once_with('drive', 'v3', credentials=credential)
        assert isinstance(fs, GoogleDriveFilesystem)
        assert fs.drive_service == service

    def test_list_file(self):
        drive = MagicMock(spec=Resource)
        fs = GoogleDriveFilesystem(drive)

        res = fs.list_files('asdfasdsadfasdfasd', True)
        assert isinstance(res, GoogleDriveListFileResponse)
        assert res.google_drive_service == drive
        assert len(res.requests) == 1
        assert res.requests[0].directory_id == 'asdfasdsadfasdfasd'
        assert res.is_recursive

    def test_create_a_file(self, mocker):
        google_drive_service = MagicMock(spec=Resource)
        google_drive_service.mock_add_spec(['files'])

        file_resource = MagicMock(spec=Resource)
        file_resource.mock_add_spec(['create'])
        google_drive_service.files.return_value = file_resource

        create_resource = MagicMock(spec=Resource)
        create_resource.mock_add_spec(['execute'])
        file_resource.create.return_value = create_resource

        create_resource.execute.return_value = {
            "id": "asdgasdfasdf",
            "mimeType": "application/text",
            "md5Checksum": "akcklsjfkdlsjfk"
        }

        mocked_upload = MagicMock(spec=MediaFileUpload)
        mocker.patch('googleapiclient.http.MediaFileUpload', return_value=mocked_upload)

        fs = GoogleDriveFilesystem(google_drive_service)
        file = fs.create_file(
            GoogleDriveFile('asdgasdfasdf', 'aa', 'dir', 'application/vnd.google-apps.folder', None),
            'a.txt',
            'tmp.txt'
        )

        assert isinstance(file, GoogleDriveFile)
        file_resource.create.assert_called_once_with(
            body={
                "name": "a.txt",
                "parents": [
                    "asdgasdfasdf"
                ]
            },
            media_body=mocked_upload,
            fields='id, mimeType, md5Checksum'
        )
        assert file.file_id == 'asdgasdfasdf'
        assert file.file_path == 'aa/a.txt'
        assert file.file_name == 'a.txt'
        assert file.mime_type == 'application/text'
        assert file.md5_checksum == 'akcklsjfkdlsjfk'
        assert not file.is_dir()

    def test_create_a_directory(self):
        google_drive_service = MagicMock(spec=Resource)
        google_drive_service.mock_add_spec(['files'])

        file_resource = MagicMock(spec=Resource)
        file_resource.mock_add_spec(['create'])
        google_drive_service.files.return_value = file_resource

        create_resource = MagicMock(spec=Resource)
        create_resource.mock_add_spec(['execute'])
        file_resource.create.return_value = create_resource

        create_resource.execute.return_value = {
            "id": "asdgasdfasdf"
        }

        fs = GoogleDriveFilesystem(google_drive_service)
        file = fs.create_directory(
            GoogleDriveFile('asdgasdfasdf', 'aa', 'dir', 'application/vnd.google-apps.folder', None),
            'bb',
        )

        assert isinstance(file, GoogleDriveFile)
        file_resource.create.assert_called_once_with(
            body={
                "name": "bb",
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [
                    "asdgasdfasdf"
                ]
            },
            fields='id'
        )
        assert file.file_id == 'asdgasdfasdf'
        assert file.file_path == 'aa/bb'
        assert file.file_name == 'bb'
        assert file.mime_type == 'application/vnd.google-apps.folder'
        assert file.md5_checksum is None
        assert file.is_dir()

    def test_delete_a_file(self):
        google_drive_service = MagicMock(spec=Resource)
        google_drive_service.mock_add_spec(['files'])

        file_resource = MagicMock(spec=Resource)
        file_resource.mock_add_spec(['delete'])
        google_drive_service.files.return_value = file_resource

        delete_resource = MagicMock(spec=Resource)
        delete_resource.mock_add_spec(['execute'])
        file_resource.delete.return_value = delete_resource

        fs = GoogleDriveFilesystem(google_drive_service)
        fs.delete_file('asdfjlasdkfj')

        file_resource.delete.assert_called_once_with(fileId='asdfjlasdkfj')

    def test_get_root_directory(self):
        fs = GoogleDriveFilesystem(MagicMock(spec=Resource))
        file = fs.get_root_dir('asdfasgsdafdasdfas')

        assert file.file_id == 'asdfasgsdafdasdfas'
        assert file.file_path == '.'
        assert file.file_name == 'root'
        assert file.is_dir()
