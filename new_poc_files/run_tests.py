import pytest

if __name__ == '__main__':
    import sys
    retcode = pytest.main(['llm_test/*.py'])
    sys.exit(retcode)