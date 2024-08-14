import os
import tempfile
import time
import unittest
from file_cleanup import remove_extra_files


class TestFileCleanup(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        # Create 35 temporary files
        for i in range(35):
            with open(os.path.join(self.test_dir.name, f'test_file_{i}.txt'), 'w') as f:
                f.write('This is a test file.')
                time.sleep(0.01)  # Ensure different creation times

    def tearDown(self):
        self.test_dir.cleanup()

    def test_remove_extra_files(self):
        remove_extra_files(self.test_dir.name, max_files=30)
        remaining_files = os.listdir(self.test_dir.name)
        self.assertEqual(len(remaining_files), 30)


if __name__ == '__main__':
    unittest.main()
