from testfixtures import TempDirectory

from sync.local.local_list_file_response import LocalListFileResponse


class TestLocalListFileResponse:
    def test_get_all_file_non_recursive(self):
        with TempDirectory() as root_dir:
            root_dir.write('f1.txt', b'file 1')
            root_dir.write('f2.txt', b'file 2')
            root_dir.makedir('dir1')
            root_dir.write('dir1/f3.txt', b'file 3 in dir1')

            res = LocalListFileResponse([root_dir.path], False)
            assert len(res.next().files) == 3
            assert res.next() is None

    def test_get_all_file_recursively(self):
        with TempDirectory() as root_dir:
            root_dir.write('f1.txt', b'file 1')
            root_dir.write('f2.txt', b'file 2')
            root_dir.makedir('dir1')
            root_dir.write('dir1/f3.txt', b'file 3 in dir1')

            res = LocalListFileResponse([root_dir.path], True)
            assert len(res.next().files) == 3  # list file in the root folder
            assert len(res.next().files) == 1  # list file in the dir1 folder
            assert res.next() is None
