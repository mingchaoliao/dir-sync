from typing import List

from pytest import raises

from sync.application_exception import ApplicationException
from sync.file import File
from sync.file_collection import FileCollection


class FakeFile(File):

    def get_md5_checksum(self) -> str:
        return 'abcdefkalsjfkdlf'

    def is_dir(self) -> bool:
        return True

    def get_relative_path(self, base_path: str) -> str:
        return self.file_path


class TestFileCollection():
    def test_file_collection_is_iterable(self):
        f = [
            FakeFile('path/to/file1', 'path/to/file1', 'file1'),
            FakeFile('path/to/file2', 'path/to/file2', 'file2')
        ]

        files = FileCollection(f)

        i = 0
        for file in files:
            assert file == f[i]
            i += 1
        assert i == 2

    def test_add_file_in_the_collection(self):
        file1 = FakeFile('path/to/file1', 'path/to/file1', 'file1')
        file2 = FakeFile('path/to/file2', 'path/to/file2', 'file2')

        f = [
            file1,
            file2
        ]

        files = FileCollection([file1])
        files.push(file2)

        assert files.files == f

    def test_concat_two_collection_by_using_add_operator(self):
        file1 = FakeFile('path/to/file1', 'path/to/file1', 'file1')
        file2 = FakeFile('path/to/file2', 'path/to/file2', 'file2')

        f = [
            file1,
            file2
        ]

        files1 = FileCollection([file1])
        files2 = FileCollection([file2])

        assert (files1 + files2).files == f

    def test_only_two_collection_can_be_concat_together(self):
        with raises(ApplicationException):
            files1 = FileCollection()
            files1 + 1

    def test_create_collection_with_no_files(self):
        files = FileCollection()
        assert len(files.files) == 0

    def test_convert_the_collection_to_a_dictionary_with_name_as_key(self):
        f = [
            FakeFile('path/to/file1', 'path/to/file1', 'file1'),
            FakeFile('path/to/file2', 'path/to/file2', 'file2')
        ]

        files = FileCollection(f)
        file_dict = files.to_dict_by_file_name()

        assert 'file1' in file_dict
        assert f[0] == file_dict['file1']

        assert 'file2' in file_dict
        assert f[1] == file_dict['file2']
