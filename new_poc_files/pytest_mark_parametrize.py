import pytest

class MyTester():
    def __init__(self, arg = ["var0", "var1"]):
        self.arg = arg
        # self.use_arg_to_init_logging_part()

    def dothis(self):
        print("this")

    def dothat(self):
        print("that")

@pytest.fixture
def tester(request):
    """Create tester object"""
    return MyTester(request.param)


class TestIt:
    @pytest.mark.parametrize('tester', [['var1', 'var2']], indirect=True)
    def test_tc1(self, tester):
       tester.dothis()
       assert 1

