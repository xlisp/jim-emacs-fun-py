# GPT1: pytest how to run any test  finished  to do the clean something 
# GPT2: setup_and_teardown need pass the argument new_codezone_id from `yield  # This is where the test will run` code eval result. 
import pytest

class Context:
    def __init__(self):
        self.new_codezone_id = None

@pytest.fixture
def setup_and_teardown():
    # Setup: Initialize the context object
    context = Context()
    print("1. Setup code here\n")

    yield context

    # Teardown: Access the new_codezone_id for cleanup
    print(f"\n2. Teardown code here, new_codezone_id: {context.new_codezone_id}\n")

def test_example(setup_and_teardown):
    # Access the context object
    context = setup_and_teardown
    
    # Generate the new_codezone_id dynamically
    context.new_codezone_id = "12345"
    
    # Test code here
    assert context.new_codezone_id == "12345"

## pytest pytest_setup_and_teardown2.py   -s => 
# pytest_setup_and_teardown2.py 1. Setup code here
# .
# 2. Teardown code here, new_codezone_id: 12345

