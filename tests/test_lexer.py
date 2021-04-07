from typing import Iterator

import pytest

from cmp.grammar.lexer import Lexer


@pytest.fixture
def string() -> str:
    return '''
        if (a == 245)
            'do_something'
        else
            'to_do'



        % Just a comment
    '''


@pytest.fixture
def right_tokens() -> Iterator[str]:
    return iter(['IF', '(', 'IDENTIFIER', 'EQ_OP', 'CONSTANT',
                 ')', 'STRING_LITERAL', 'ELSE', 'STRING_LITERAL'])


def test_lexer(string: str, right_tokens: Iterator[str]) -> None:
    m = Lexer()
    m.input(string)

    gen_tok = m.token()
    rhg_tok = next(right_tokens)

    while gen_tok:
        try:
            if gen_tok.type == 'NEWLINE':
                gen_tok = m.token()
                continue

            assert gen_tok.type == rhg_tok
            gen_tok = m.token()
            rhg_tok = next(right_tokens)
        except StopIteration:
            break
