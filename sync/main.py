from sync.application_exception import ApplicationException
from sync.dir_sync_command import DirSyncCommand
from sync.dir_sync_service import DirSyncService


def main() -> int:
    try:
        dir_sync_service = DirSyncService()
        dir_sync_command = DirSyncCommand(dir_sync_service)
        dir_sync_command.handle()
        return 0
    except ApplicationException as e:
        print('Error: {}'.format(e.get_message()))
        return 1
