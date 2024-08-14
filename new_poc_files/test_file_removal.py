import os
import tempfile
import unittest
import subprocess
from file_removal import remove_extra_files

class TestFileRemoval(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        # Create 40 temporary files
        for i in range(40):
            with open(os.path.join(self.test_dir.name, f'test_file_{i}.txt'), 'w') as f:
                f.write('This is a test file.')

    def tearDown(self):
        self.test_dir.cleanup()

    def test_remove_extra_files(self):
        # Run the file removal script
        remove_extra_files(self.test_dir.name, max_files=30)
        # Check the number of files remaining
        remaining_files = os.listdir(self.test_dir.name)
        self.assertEqual(len(remaining_files), 30)

if __name__ == '__main__':
    unittest.main()
