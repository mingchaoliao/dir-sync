from typing import Dict, List, Type, Tuple

from sync.application_exception import ApplicationException
from sync.file import File
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

        dir_pairs: List[Tuple[File, File]] = self.sync_dir(
            src_fs.get_root_dir(args['src']),
            dst_fs.get_root_dir(args['dst']),
            src_fs,
            dst_fs
        )

        while True:
            if len(dir_pairs) == 0:
                break

            src_dir, dst_dir = dir_pairs.pop()

            dir_pairs = dir_pairs + self.sync_dir(src_dir, dst_dir, src_fs, dst_fs)

    def sync_dir(self,
                 src_dir: File,
                 dst_dir: File,
                 src_fs: Filesystem,
                 dst_fs: Filesystem) -> List[Tuple[File, File]]:
        src_files: FileCollection = src_fs.list_files(src_dir.file_id).get_all()
        dst_files_dict: Dict[str, File] = dst_fs.list_files(dst_dir.file_id).get_all().to_dict_by_file_name()

        rtn: List[Tuple[File, File]] = []

        for src_file in src_files:
            src_file_name = src_file.file_name

            if src_file.is_dir():
                if src_file_name in dst_files_dict and dst_files_dict[src_file_name].is_dir():
                    rtn.append((src_file, dst_files_dict[src_file_name]))
                else:
                    rtn.append((src_file, dst_fs.create_directory(dst_dir, src_file_name)))
            else:
                if src_file_name not in dst_files_dict \
                        or dst_files_dict[src_file_name].get_md5_checksum() != src_file.get_md5_checksum():
                    dst_fs.create_file(
                        dst_dir,
                        src_file_name,
                        lambda fh: src_fs.read_file(src_file.file_id, fh)
                    )
        return rtn

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
