import re

from ply.lex import TOKEN, LexToken, lex

from cmp.grammar.cmp_tables import abs_module_path
from cmp.helpers import LogMixin


class Lexer(LogMixin):
    """
    Executive lexer object.
    Containing primary tokens.
    This class give next token
    """
    # Keywords MATLAB
    keywords = {
        "for": "FOR",
        "while": "WHILE",
        "break": "BREAK",
        "if": "IF",
        "else": "ELSE",
        "elseif": "ELSEIF",
        "end": "END",
        "function": "FUNCTION",
        "return": "RETURN",
        "global": "GLOBAL",
        "clear": "CLEAR",
    }

    # All tokens
    tokens = tuple([
        "IDENTIFIER",
        "CONSTANT",
        "STRING_LITERAL",
        "LE_OP", "GE_OP", "EQ_OP", "NE_OP",
        "ARRAY_MUL", "ARRAY_POW", "ARRAY_DIV", "ARRAY_RDIV", "TRANSPOSE",
        "NEWLINE",
        "COMMENT",
        "TCOMMENT"
    ] + list(keywords.values()))

    # Ignore symbol
    t_ignore_WHITESPACE = r"\s+"

    # literals
    literals = [
        '~', ';', ',', ':', '=', '(',
        ')', '[', ']', '&', '-', '+',
        '*', '/', '\\', '>', '<', '|'
    ]

    states = (
        ('string', 'exclusive'),
    )

    # Regular expressions for complex tokens
    D = r"[0-9]"
    L = r"[a-zA-Z_]"
    E = fr"[DdEe][+-]?{D}+"

    constant_1 = fr'{D}+({E})?'
    constant_2 = fr'{D}*"."{D}+({E})?'
    constant_3 = fr'{D}+"."{D}*({E})?'
    constant = constant_1 + r'|' + constant_2 + r'|' + constant_3

    transpose_1 = r"'"
    transpose_2 = r"\.'"
    transpose = transpose_1 + r'|' + transpose_2

    identifier = fr'{L}({L}|{D})*'

    # Regular expressions for simple tokens
    # Logic operations
    t_LE_OP = r"<="
    t_GE_OP = r"\>="
    t_EQ_OP = r"=="
    t_NE_OP = r"(~=)|(!=)"
    # Array operations
    t_ARRAY_MUL = r"\.\*"
    t_ARRAY_POW = r"\.\^"
    t_ARRAY_DIV = r"\./"
    t_ARRAY_RDIV = r"\.//"
    # Comments
    t_string_TCOMMENT = r'[^\n]+'
    t_string_ignore = r''

    def __init__(self) -> None:
        self._lexer = lex(
            module=self,
            optimize=False,
            debug=False,
            outputdir=abs_module_path,
            lextab='cmp_lex_tab',
            reflags=re.UNICODE | re.DOTALL
        )

    def t_error(self, token_: LexToken) -> None:
        """Error handler lexer"""
        print(f"Illegal character {token_.value[0]}")
        token_.lexer.skip(1)

    def t_string_error(self, token_: LexToken) -> None:
        """Error handler lexer for string state"""
        print(f"Illegal character {token_.value[0]}")
        token_.lexer.skip(1)

    @TOKEN(constant)
    def t_CONSTANT(self, token_: LexToken) -> LexToken:
        token_.type = self.keywords.get(token_.value, "CONSTANT")
        return token_

    @TOKEN(identifier)
    def t_IDENTIFIER(self, token_: LexToken) -> LexToken:
        token_.type = self.keywords.get(token_.value, "IDENTIFIER")
        return token_

    def t_STRING_LITERAL(self, token_: LexToken) -> LexToken:
        r"""'[^'\n]*'"""
        return token_

    @TOKEN(transpose)
    def t_TRANSPOSE(self, token_: LexToken) -> LexToken:
        """"""
        return token_

    def t_NEWLINE(self, token_: LexToken) -> LexToken:
        r"""\n"""
        token_.lexer.lineno += 1
        token_.type = 'NEWLINE'
        return token_

    def t_ANY_COMMENT(self, token_: LexToken) -> LexToken:
        r"""[\%]|[\n]"""
        if token_.lexer.current_state() == 'string':
            token_.type = 'NEWLINE'
            token_.lexer.begin('INITIAL')
        else:
            token_.lexer.begin('string')
        return token_

    def input(self, data_: str) -> None:
        self._lexer.input(data_)

    def token(self) -> LexToken:
        return self._lexer.token()


data = '''
% Comment 1

% Comment 2
'''

if __name__ == '__main__':
    l = Lexer()
    l.input(data)
    while True:
        t = l.token()
        if t is None:
            break
        print(t)
