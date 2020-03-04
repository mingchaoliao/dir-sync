from os import path
from typing import List

from googleapiclient.discovery import Resource

from sync.file_collection import FileCollection
from sync.filesystem import ListFileResponse
from sync.google_drive.google_drive_file import GoogleDriveFile
from sync.google_drive.google_drive_list_file_request import GoogleDriveListFileRequest


class GoogleDriveListFileResponse(ListFileResponse):
    requests: List[GoogleDriveListFileRequest] = []
    google_drive_service: Resource

    def __init__(self,
                 google_drive_service: Resource,
                 requests: List[GoogleDriveListFileRequest],
                 is_recursive: bool = False):
        super().__init__(is_recursive)
        self.requests = requests
        self.google_drive_service = google_drive_service

    def next(self) -> FileCollection or None:
        if len(self.requests) == 0:
            return None

        files = FileCollection()
        requests: List[GoogleDriveListFileRequest] = []
        request = self.requests.pop()
        res = self.google_drive_service.files().list(
            pageToken=request.page_token,
            pageSize=request.page_size,
            fields=request.fields,
            q="'{}' in parents".format(request.directory_id)
        ).execute()

        for file_data in res['files']:
            files.push(GoogleDriveFile(
                file_data['id'],
                path.join(request.base_directory, file_data['name']),
                file_data['name'],
                file_data['mimeType'],
                file_data['md5Checksum'] if 'md5Checksum' in file_data else None
            ))
            if file_data['mimeType'] == 'application/vnd.google-apps.folder' and self.is_recursive:
                requests.append(GoogleDriveListFileRequest(
                    file_data['id'],
                    path.join(request.base_directory, file_data['name'])
                ))

        if 'nextPageToken' in res:
            requests.append(GoogleDriveListFileRequest(
                request.directory_id,
                request.base_directory,
                res['nextPageToken']
            ))

        self.requests = self.requests + requests
        return files
