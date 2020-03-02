import google

from sync.google_drive import GoogleDrive


class TestGoogleDrive:
    def test_create_drive_from_service_account_file(self, mocker):
        key_file_path = 'path/to/key.json'
        mocker.patch('google.oauth2.service_account.Credentials.from_service_account_file')
        GoogleDrive.create(key_file_path)
        google.oauth2.service_account.Credentials.from_service_account_file.assert_called_once_with(key_file_path)

    # TODO: finish unit test cases
