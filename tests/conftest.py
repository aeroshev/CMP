from typing import Generator, List

import pytest


@pytest.fixture
def right_tokens() -> Generator[List[str], None, None]:
    yield ['IF', 'LPAREN', 'WORD', 'EQ_OP', 'NUMBER',
           'RPAREN', 'WORD', 'ELSE', 'WORD']
