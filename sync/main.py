from argparse import ArgumentParser
from os.path import join
from typing import List

from setuptools_scm import get_version

from sync.google_drive import GoogleDrive
from sync.local_fs import LocalFS


def main():
    # command setup
    parser = ArgumentParser(
        description='Sync files in the local folder with files in the remote location, e.g. Google Drive.',
        prog='Google Drive Sync'
    )
    parser.add_argument('--version', help='Print version of this program.', action='version',
                        version='Version: {}'.format(get_version()))
    parser.add_argument('--src-type', required=True, help='Source type.', choices=['google-drive'])
    parser.add_argument('--dst-type', required=True, help='Destination type.', choices=['local'])
    parser.add_argument('--src', required=True, help='Source directory path. The value depends on the source type.')
    parser.add_argument('--dst', required=True,
                        help='Destination directory path. The value depends on the source type.')
    parser.add_argument('--auth-key-file', required=True, help='Path to auth key file.')
    args = vars(parser.parse_args())

    # local file system
    local_fs = LocalFS(args['dst'])

    # create google drive service
    google_drive = GoogleDrive.create(args['auth_key_file'])

    # 0: Google Drive folder ID
    # 1: local base directory path
    # 2: next page token (if there is any)
    dir_request_queue: List[List[str]] = [[args['src'], args['dst'], None]]

    while len(dir_request_queue) > 0:
        dir_request = dir_request_queue.pop()
        files, next_page_token = google_drive.list(dir_request[0], page_size=10, next_page_token=dir_request[2])

        # add to queue for requesting the next page
        if next_page_token:
            dir_request_queue.append([dir_request[0], dir_request[1], next_page_token])

        for file in files:
            # add to queue for requesting files in the sub-directory
            if file.is_dir():
                dir_request_queue.append([file.fid, join(dir_request[1], file.name), None])
            else:  # sync file to local
                path = join(dir_request[1], file.name)
                if not local_fs.is_file_existed(path, file.md5):
                    local_fs.create_file(path, lambda fh: google_drive.download(file.fid, fh))
