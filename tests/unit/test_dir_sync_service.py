import pytest

from sync.application_exception import ApplicationException
from sync.dir_sync_service import DirSyncService
from sync.google_drive.google_drive_filesystem_factory import GoogleDriveFilesystemFactory
from sync.local.local_filesystem import LocalFilesystem
from sync.local.local_filesystem_factory import LocalFilesystemFactory


class TestDirSyncService:
    def test_src_type_must_not_same_as_dst_type(self):
        service = DirSyncService()
        with pytest.raises(ApplicationException):
            service.run({
                "src_type": "local",
                "dst_type": "local",
                "src": "./",
                "dst": "asdfasdf",
                "auth_key_file": "./key.json"
            })

    def test_register_filesystem_factory_into_the_service(self):
        service = DirSyncService()
        assert len(service.filesystem_factories) == 0

        service.register_filesystem_factories(LocalFilesystemFactory)
        assert len(service.filesystem_factories) == 1
        assert service.filesystem_factories[0] == LocalFilesystemFactory

    def test_get_all_available_filesystem_names(self):
        service = DirSyncService()

        service.register_filesystem_factories(LocalFilesystemFactory)
        service.register_filesystem_factories(GoogleDriveFilesystemFactory)

        assert len(service.get_available_filesystem_names()) == 2
        assert service.get_available_filesystem_names() == [
            LocalFilesystemFactory.get_filesystem_name(),
            GoogleDriveFilesystemFactory.get_filesystem_name()
        ]

    def test_instantiate_fs_if_found(self):
        service = DirSyncService()

        service.register_filesystem_factories(LocalFilesystemFactory)
        service.register_filesystem_factories(GoogleDriveFilesystemFactory)

        fs = service.instantiate_filesystem('local', {})
        assert isinstance(fs, LocalFilesystem)

    def test_raise_error_if_the_fs_not_found(self):
        service = DirSyncService()

        service.register_filesystem_factories(LocalFilesystemFactory)

        with pytest.raises(ApplicationException):
            service.instantiate_filesystem('aaa', {})
