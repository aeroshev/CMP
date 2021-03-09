from cmp.grammar.lexer import Lexer


def test_lexer(string) -> None:
    m = Lexer()
    m.build()
    m.input(string)
    for token in m.token():
        print(token)
