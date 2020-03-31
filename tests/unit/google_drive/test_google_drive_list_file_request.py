from sync.google_drive.google_drive_list_file_request import GoogleDriveListFileRequest


class TestGoogleDriveListFileRequest:
    def test_create_request(self):
        req = GoogleDriveListFileRequest('asdfasdfasdfa', 'tmp/app', 'cxckjviaoie', 100)
        assert req.directory_id == 'asdfasdfasdfa'
        assert req.fields == "nextPageToken, files(id, name, md5Checksum, mimeType)"
        assert req.page_size == 100
        assert req.page_token == 'cxckjviaoie'
        assert req.base_directory == 'tmp/app'
