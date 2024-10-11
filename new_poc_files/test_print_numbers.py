import unittest
from io import StringIO
import sys
from print_numbers import print_numbers

class TestPrintNumbers(unittest.TestCase):
    def test_output(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        print_numbers()
        sys.stdout = sys.__stdout__
        expected_output = ''.join(f'{i}\n' for i in range(1, 101))
        self.assertEqual(captured_output.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()