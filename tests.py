import unittest

import hid


class HIDTests(unittest.TestCase):
    def test_enumerate(self):
        self.assertTrue(len(hid.enumerate()) >= 0)


if __name__ == "__main__":
    unittest.main()
