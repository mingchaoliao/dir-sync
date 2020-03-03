from hashlib import md5


class Utils:
    @staticmethod
    def cal_md5_checksum(file_path: str) -> str:
        md5_checksum = md5()
        with open(file_path, 'rb') as fh:
            for block in iter(lambda: fh.read(4096), b""):
                md5_checksum.update(block)
        return md5_checksum.hexdigest()
