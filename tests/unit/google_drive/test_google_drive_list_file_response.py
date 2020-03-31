from unittest.mock import MagicMock

from googleapiclient.discovery import Resource

from sync.google_drive.google_drive_list_file_request import GoogleDriveListFileRequest
from sync.google_drive.google_drive_list_file_response import GoogleDriveListFileResponse


class TestGoogleDriveListFileResponse:
    def test_return_none_if_there_is_nothing_in_the_requests(self, mocker):
        google_drive_service = mocker.patch('googleapiclient.discovery.Resource', autospec=True, spec_set=True)

        response = GoogleDriveListFileResponse(google_drive_service, [])
        files = response.next()

        assert files is None

    def test_retrieve_files_and_directories(self):
        google_drive_service = MagicMock(spec=Resource)
        google_drive_service.mock_add_spec(['files'])

        file_resource = MagicMock(spec=Resource)
        file_resource.mock_add_spec(['list'])
        google_drive_service.files.return_value = file_resource

        list_resource = MagicMock(spec=Resource)
        list_resource.mock_add_spec(['execute'])
        file_resource.list.return_value = list_resource

        list_resource.execute.return_value = {
            "nextPageToken": "alkjxckj309skldk",
            "files": [
                {
                    "id": "zxjlweioskal",
                    "name": "file.txt",
                    "mimeType": "application/text",
                    "md5Checksum": "akdlfjskdleoskdj"
                },
                {
                    "id": "zxvjl4e80alks",
                    "name": "dir",
                    "mimeType": "application/vnd.google-apps.folder"
                }
            ]
        }

        response = GoogleDriveListFileResponse(google_drive_service, [
            GoogleDriveListFileRequest(
                'asdjflasgkjerjwlkj',
                '.',
                'gjlkxzjoeiwlkj',
                10
            )
        ], True)
        files = response.next()

        google_drive_service.files.assert_called_once()
        file_resource.list.assert_called_once_with(
            pageToken='gjlkxzjoeiwlkj',
            pageSize=10,
            fields="nextPageToken, files(id, name, md5Checksum, mimeType)",
            q="'asdjflasgkjerjwlkj' in parents"
        )
        list_resource.execute.assert_called_once()
        assert len(files.files) == 2

        assert files.files[0].file_id == 'zxjlweioskal'
        assert files.files[0].file_path == './file.txt'
        assert files.files[0].file_name == 'file.txt'
        assert files.files[0].get_md5_checksum() == 'akdlfjskdleoskdj'
        assert not files.files[0].is_dir()

        assert files.files[1].file_id == 'zxvjl4e80alks'
        assert files.files[1].file_path == './dir'
        assert files.files[1].file_name == 'dir'
        assert files.files[1].get_md5_checksum() is None
        assert files.files[1].is_dir()

        assert len(response.requests) == 2
        assert response.requests[0].directory_id == 'zxvjl4e80alks'
        assert response.requests[0].base_directory == './dir'
        assert response.requests[0].page_size == 10
        assert response.requests[0].page_token is None

        assert response.requests[1].directory_id == 'asdjflasgkjerjwlkj'
        assert response.requests[1].base_directory == '.'
        assert response.requests[1].page_size == 10
        assert response.requests[1].page_token == 'alkjxckj309skldk'
