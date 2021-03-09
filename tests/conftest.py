import pytest


@pytest.fixture
def string() -> str:
    return '''
        if (a == 245)
            do_something
        else
            to_do
        
        
        
        # Just a comment
    '''
