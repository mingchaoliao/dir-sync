from hashlib import md5
from os import path

from testfixtures import TempDirectory

from sync.local.utils import Utils


class TestUtils:
    def test_cal_md5_checksum(self):
        content = b'hello world'
        with TempDirectory() as d:
            d.write('text.txt', content)
            actual = Utils.cal_md5_checksum(path.join(d.path, 'text.txt'))

            m = md5()
            m.update(content)
            expected = m.hexdigest()

            assert actual == expected
