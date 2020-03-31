from sync.local.local_file import LocalFile
from sync.local.utils import Utils


class TestLocalFile:
    def test_file_id_is_same_as_file_path(self):
        file_path = '/path/to/file'
        file = LocalFile(file_path, False)
        assert file.file_path == file_path
        assert file.file_id == file_path

    def test_get_file_name_from_path(self):
        file = LocalFile('/path/to/text1.txt', False)
        assert file.file_name == 'text1.txt'

    def test_file_is_directory(self):
        file_path = '/path/to/dir'
        file = LocalFile(file_path, True)
        assert file.is_dir()

    def test_file_is_not_directory(self):
        file_path = '/path/to/file'
        file = LocalFile(file_path, False)
        assert not file.is_dir()

    def test_get_md5_checksum_of_a_file(self, mocker):
        file = LocalFile('/path/to/file', False)
        mocked_cal_md5_checksum = mocker.patch.object(Utils, 'cal_md5_checksum', return_value='abc')
        md5_checksum = file.get_md5_checksum()

        mocked_cal_md5_checksum.assert_called_once_with('/path/to/file')
        assert md5_checksum == 'abc'
        assert file.md5_checksum == 'abc'

    def test_get_relative_path_from_base_path(self):
        assert LocalFile('/path/to/file.txt', False).get_relative_path('/path') == 'to/file.txt'
        assert LocalFile('/path/to/file.txt', False).get_relative_path('/path/to') == 'file.txt'
