from cmp.grammar.lexer import Lexer


def test_lexer(string, right_tokens) -> None:
    m = Lexer()
    m.input(string)
    for gen_tok, rhg_tok in zip(m.token(), right_tokens):
        assert gen_tok.type == rhg_tok
