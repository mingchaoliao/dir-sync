from unittest.mock import MagicMock

import pytest

from sync.dir_sync_command import DirSyncCommand
from sync.dir_sync_service import DirSyncService


class TestDirSyncCommand:
    def test_parse_options_from_command_line(self):
        sync_service = MagicMock(spec=DirSyncService)
        command = DirSyncCommand(sync_service)
        sync_service.get_available_filesystem_names.return_value = ['local', 'google-drive']

        command.handle([
            '--src-type=local',
            '--dst-type=google-drive',
            '--src=./',
            '--dst=asdfasdf',
            '--auth-key-file=./key.json'
        ])
        sync_service.run.assert_called_once_with({
            "src_type": "local",
            "dst_type": "google-drive",
            "src": "./",
            "dst": "asdfasdf",
            "auth_key_file": "./key.json"
        })

    def test_command_line_option_src_type_is_required(self):
        sync_service = MagicMock(spec=DirSyncService)
        command = DirSyncCommand(sync_service)
        sync_service.get_available_filesystem_names.return_value = ['local', 'google-drive']

        with pytest.raises(SystemExit):
            command.handle([
                '--dst-type=google-drive',
                '--src=./',
                '--dst=asdfasdf',
                '--auth-key-file=./key.json'
            ])

    def test_command_line_option_dst_type_is_required(self):
        sync_service = MagicMock(spec=DirSyncService)
        command = DirSyncCommand(sync_service)
        sync_service.get_available_filesystem_names.return_value = ['local', 'google-drive']

        with pytest.raises(SystemExit):
            command.handle([
                '--src-type=local',
                '--src=./',
                '--dst=asdfasdf',
                '--auth-key-file=./key.json'
            ])

    def test_command_line_option_src_is_required(self):
        sync_service = MagicMock(spec=DirSyncService)
        command = DirSyncCommand(sync_service)
        sync_service.get_available_filesystem_names.return_value = ['local', 'google-drive']

        with pytest.raises(SystemExit):
            command.handle([
                '--src-type=local',
                '--dst-type=google-drive',
                '--dst=asdfasdf',
                '--auth-key-file=./key.json'
            ])

    def test_command_line_option_dst_is_required(self):
        sync_service = MagicMock(spec=DirSyncService)
        command = DirSyncCommand(sync_service)
        sync_service.get_available_filesystem_names.return_value = ['local', 'google-drive']

        with pytest.raises(SystemExit):
            command.handle([
                '--src-type=local',
                '--dst-type=google-drive',
                '--src=./',
                '--auth-key-file=./key.json'
            ])

    def test_command_line_option_auth_key_file_is_required(self):
        sync_service = MagicMock(spec=DirSyncService)
        command = DirSyncCommand(sync_service)
        sync_service.get_available_filesystem_names.return_value = ['local', 'google-drive']

        with pytest.raises(SystemExit):
            command.handle([
                '--src-type=local',
                '--dst-type=google-drive',
                '--src=./',
                '--dst=asdfasdf'
            ])

    def test_application_should_exit_if_src_type_is_unsupported(self):
        sync_service = MagicMock(spec=DirSyncService)
        command = DirSyncCommand(sync_service)
        sync_service.get_available_filesystem_names.return_value = ['local', 'google-drive']

        with pytest.raises(SystemExit):
            command.handle([
                '--src-type=aaa',
                '--dst-type=google-drive',
                '--src=./',
                '--dst=asdfasdf',
                '--auth-key-file=./key.json'
            ])

    def test_application_should_exit_if_dst_type_is_unsupported(self):
        sync_service = MagicMock(spec=DirSyncService)
        command = DirSyncCommand(sync_service)
        sync_service.get_available_filesystem_names.return_value = ['local', 'google-drive']

        with pytest.raises(SystemExit):
            command.handle([
                '--src-type=local',
                '--dst-type=aaa',
                '--src=./',
                '--dst=asdfasdf',
                '--auth-key-file=./key.json'
            ])
