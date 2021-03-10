from typing import Generator, List

import pytest


@pytest.fixture
def string() -> str:
    return '''
        if (a == 245)
            do_something
        else
            to_do
        
        
        
        % Just a comment
    '''


@pytest.fixture
def right_tokens() -> Generator[List[str], None, None]:
    yield ['IF', 'LPAREN', 'WORD', 'EQ_OP', 'NUMBER',
           'RPAREN', 'WORD', 'ELSE', 'WORD']
