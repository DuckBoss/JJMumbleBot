import unittest
import sys
sys.path.append(".")
import utils
sys.path.append(".")
import helpers.image_helper as IH
import hashlib


class Tests(unittest.TestCase):
    def test_image_formatting(self):
        compare_string = "aa6bcfb8b59fc62b81c79c6150f62e2c"
        formatted_string = IH.format_image('test_image', 'jpg', f"{utils.get_main_dir()}{utils.get_tests_dir()}/", raw=True)
        fh = open("img_test.jpg", "wb")
        fh.write(formatted_string)
        fh.close()

        hashmd5 = hashlib.md5(formatted_string)
        hdigest_0 = hashmd5.hexdigest()

        self.assertEqual(hdigest_0, compare_string)


if __name__ == '__main__':
    unittest.main()
