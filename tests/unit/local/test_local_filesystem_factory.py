from sync.local.local_filesystem import LocalFilesystem

from sync.local.local_filesystem_factory import LocalFilesystemFactory


class TestLocalFilesystemFactory:
    def test_get_name_of_local_filesystem(self):
        assert LocalFilesystemFactory.get_filesystem_name() == LocalFilesystem.get_filesystem_name()

    def test_create_local_fs(self):
        assert isinstance(LocalFilesystemFactory.create({}), LocalFilesystem)
