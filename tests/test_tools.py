import unittest
import tools


class TestTools(unittest.TestCase):

    def test_upload_invalid_extension_file(self):

        file_meta = {'content_type': u'application/octet-stream',
                     'filename': 'invalid_extension.exe'}

        self.assertFalse(tools.is_valid_file(file_meta))
