def function_with_none_args(arg1=None, arg2=None):
    if arg1 is None and arg2 is None:
        return 'Both arguments are None'
    elif arg1 is None:
        return 'First argument is None'
    elif arg2 is None:
        return 'Second argument is None'
    else:
        return 'Both arguments are provided'

# Test cases
def test_function_with_none_args():
    assert function_with_none_args() == 'Both arguments are None'
    assert function_with_none_args(1) == 'Second argument is None'
    assert function_with_none_args(None, 2) == 'First argument is None'
    assert function_with_none_args(1, 2) == 'Both arguments are provided'
    print('All tests passed.')

test_function_with_none_args()
