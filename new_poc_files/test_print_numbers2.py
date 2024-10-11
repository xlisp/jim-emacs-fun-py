
import subprocess


def test_print_numbers():
    result = subprocess.run(['python', 'print_numbers.py'], capture_output=True, text=True)
    output = result.stdout.strip().split('\n')
    expected_output = [str(i) for i in range(1, 101)]
    assert output == expected_output, 'The output is not as expected.'


test_print_numbers()
