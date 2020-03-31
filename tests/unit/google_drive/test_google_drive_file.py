from sync.google_drive.google_drive_file import GoogleDriveFile


class TestGoogleDriveFile:
    def test_get_file_id_path_and_name(self):
        file = GoogleDriveFile('abasdlfkjla', 'path/to/file.txt', 'file.txt', 'application/text', 'akslfjdkclfjdkfl')
        assert file.file_path == 'path/to/file.txt'
        assert file.file_id == 'abasdlfkjla'
        assert file.file_name == 'file.txt'

    def test_check_if_the_file_is_a_directory(self):
        file1 = GoogleDriveFile('abasdlfkjla', 'path/to/file.txt', 'file.txt', 'application/text', 'akslfjdkclfjdkfl')
        file2 = GoogleDriveFile('asdljglkjlskjfd', 'path/to/dir', 'dir', 'application/vnd.google-apps.folder', None)
        assert not file1.is_dir()
        assert file2.is_dir()

    def test_get_md5_checksum_of_the_file(self):
        file = GoogleDriveFile('abasdlfkjla', 'path/to/file.txt', 'file.txt', 'application/text', 'akslfjdkclfjdkfl')
        assert file.get_md5_checksum() == 'akslfjdkclfjdkfl'

    def test_get_relative_path_to_the_file(self):
        file = GoogleDriveFile('abasdlfkjla', 'path/to/file.txt', 'file.txt', 'application/text', 'akslfjdkclfjdkfl')
        assert file.get_relative_path('anything') == 'path/to/file.txt'
