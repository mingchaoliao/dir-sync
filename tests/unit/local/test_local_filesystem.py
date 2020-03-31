from os import path

from testfixtures import TempDirectory

from sync.local.local_file import LocalFile
from sync.local.local_filesystem import LocalFilesystem


class TestLocalFilesystem:
    def test_get_filesystem_name(self):
        assert LocalFilesystem.get_filesystem_name() == 'local'

    def test_read_file_should_return_file_path(self):
        fs = LocalFilesystem()
        assert '/path/to/file' == fs.read_file('/path/to/file')

    def test_move_file_from_tmp_dir_when_create_a_file(self):
        fs = LocalFilesystem()
        with TempDirectory() as root_dir:
            root_dir.makedir('dst')
            root_dir.makedir('tmp')
            root_dir.write('tmp/tmp.txt', b'this is a file')

            root_dir_path = root_dir.path

            file = fs.create_file(
                LocalFile(path.join(root_dir_path, 'dst'), True),
                'file.txt',
                path.join(root_dir_path, 'tmp/tmp.txt')
            )

            assert file.file_path == path.join(root_dir_path, 'dst/file.txt')
            with open(file.file_path, 'r') as fh:
                assert fh.read() == 'this is a file'

    def test_list_file_should_return_a_response(self, mocker):
        fs = LocalFilesystem()
        res = fs.list_files('/path/to/dir')
        assert not res.is_recursive
        assert res.dirs == ['/path/to/dir']

    def test_get_root_dir(self):
        assert 'path/to/root/dir' == LocalFilesystem().get_root_dir('path/to/root/dir').file_path

    def test_delete_a_directory(self):
        with TempDirectory() as root_dir:
            root_dir.makedir('dir')
            root_dir.write('dir/test.txt', b'abc')
            LocalFilesystem().delete_file(path.join(root_dir.path, 'dir'))
            assert not path.isdir(path.join(root_dir.path, 'dir'))

    def test_delete_a_file(self):
        with TempDirectory() as root_dir:
            root_dir.write('test.txt', b'abc')
            LocalFilesystem().delete_file(path.join(root_dir.path, 'test.txt'))
            assert not path.isfile(path.join(root_dir.path, 'test.txt'))

    def test_create_a_directory(self):
        with TempDirectory() as root_dir:
            LocalFilesystem().create_directory(LocalFile(root_dir.path, True), 'c')
            assert path.isdir(path.join(root_dir.path, 'c'))
