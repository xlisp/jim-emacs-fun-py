import subprocess
import os


def test_search_imports():
    test_file_content = '''
import os
import sys
from math import sqrt
from collections import defaultdict
    '''
    test_file_path = 'temp_test_file.py'
    with open(test_file_path, 'w') as test_file:
        test_file.write(test_file_content)

    result = subprocess.run(['python', 'search_imports.py', test_file_path], capture_output=True, text=True)
    os.remove(test_file_path)

    expected_output = 'import os\nimport sys\nfrom math import sqrt\nfrom collections import defaultdict\n'
    assert result.stdout == expected_output, f'Expected: {expected_output}, but got: {result.stdout}'


test_search_imports()
print('All tests passed.')