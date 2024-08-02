import pytest

@pytest.fixture
def setup_and_teardown():
    # Setup: Code to run before the test
    print("Setup code here")
    
    yield  # This is where the test will run
    
    # Teardown: Code to run after the test
    print("Teardown code here")

def test_example(setup_and_teardown):
    # Test code here
    assert True

