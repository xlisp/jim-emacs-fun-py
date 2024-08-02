import pytest


class MyTester:
    def __init__(self, arg=["var0", "var1"]):
        self.arg = arg
        # self.use_arg_to_init_logging_part()

    def dothis(self):
        print("this")
        return self.arg

    def dothat(self):
        print("that")


@pytest.fixture
def tester(request):
    """Create tester object"""
    return MyTester(request.param)


@pytest.fixture
def tester_return_block():
    """Create tester object"""

    def tester_fn(params):
        return MyTester(params)

    yield tester_fn


class TestIt:
    # 1. @pytest.mark.parametrize给@pytest.fixture的函数去传递参数
    @pytest.mark.parametrize("tester", [["var1", "var2"]], indirect=True)
    def test_tc1(self, tester):
        assert tester.dothis() == ["var1", "var2"]


# 2. yield tester_fn通过返回闭包的方式来给@pytest.fixture的函数去传递参数
def test_tc2(tester_return_block):
    test2 = tester_return_block(["v1", "v2"])
    assert test2.dothis() == ["v1", "v2"]
