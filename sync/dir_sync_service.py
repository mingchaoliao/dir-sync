from os import path
from typing import Dict, List, Type

from sync.application_exception import ApplicationException
from sync.file_collection import FileCollection
from sync.filesystem import Filesystem
from sync.filesystem_factory import FilesystemFactory


class DirSyncService:
    filesystem_factories: List[Type[FilesystemFactory]] = []

    def run(self, args: Dict):
        if args['src_type'] == args['dst_type']:
            raise ApplicationException('Destination type (--dst-type) must not same as source type (--src-type).')

        src_fs = self.instantiate_filesystem(args['src_type'], args)
        dst_fs = self.instantiate_filesystem(args['dst_type'], args)

        src_list_file_res = src_fs.list_files(args['src'])
        while True:
            src_files: FileCollection = src_list_file_res.next()

            if src_files is None:
                break

            for src_file in src_files:
                dst_file_path = path.join(args['dst'], src_file.file_path)
                if not dst_fs.has_file(dst_file_path, src_file.get_md5_checksum()):
                    dst_fs.create_file(
                        dst_file_path,
                        lambda fh: src_fs.read_file(src_file.file_id, fh)
                    )

        pass

    def instantiate_filesystem(self, name: str, args: Dict) -> Filesystem:
        for filesystem_factory in self.filesystem_factories:
            if filesystem_factory.get_filesystem_name() == name:
                return filesystem_factory.create(args)
        raise ApplicationException('Unable to instantiate filesystem: filesystem {} is undefined.'.format(name))

    def register_filesystem_factories(self, filesystem_factory: Type[FilesystemFactory]):
        self.filesystem_factories.append(filesystem_factory)
        pass

    def get_available_filesystem_names(self) -> List[str]:
        return list(map(lambda x: x.get_filesystem_name(), self.filesystem_factories))
