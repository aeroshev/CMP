from typing import Generator

from ply.lex import TOKEN, LexToken, lex


class Lexer:
    # Keywords MATLAB
    keywords = {
        # Loops keywords
        "for": "FOR",
        "while": "WHILE",
        "break": "BREAK",
        # "continue": "CONTINUE",
        # Conditions
        "if": "IF",
        "else": "ELSE",
        "elseif": "ELSEIF",
        "end": "END",
        # Catch exceptions
        # "try": "TRY",
        # "catch": "CATCH",
        # Function
        "function": "FUNCTION",
        "return": "RETURN",
        # Switch
        # "switch": "SWITCH",
        # "case": "CASE",
        # Other
        "global": "GLOBAL",
        # "end_unwind_protect": "END_UNWIND_PROTECT",
        # "unwind_protect": "UNWIND_PROTECT",
        # "unwind_protect_cleanup": "UNWIND_PROTECT_CLEANUP",
        # "otherwise": "OTHERWISE",
        # "persistent": "PERSISTENT",
        "clear": "CLEAR",
    }

    # All tokens
    tokens = tuple([
        # Complex objects
        "IDENTIFIER",
        "CONSTANT",
        "STRING_LITERAL",
        "CONTINUATION",
        # Logic operations
        "LE_OP", "GE_OP", "EQ_OP", "NE_OP",
        # "AND_AND", "OR_OR",
        # Arithmetic operations
        # "DIV_DIV",
        # Plus operations
        # "PLUS_EQ", "PLUS_PLUS",
        # Minus operations
        # "MINUS_EQ", "MINUS_MINUS",
        # Array operations
        "ARRAY_MUL", "ARRAY_POW", "ARRAY_DIV", "ARRAY_RDIV", "TRANSPOSE",

        # Ignore
        "WHITESPACE",
        "COMMENT"
    ] + list(keywords.values()))

    # Ignore symbol
    t_ignore_WHITESPACE = r"\s+"
    t_ignore_COMMENT = r"\%.*\n"

    # literals
    literals = [
        '~', ';', ',', ':', '=', '(',
        ')', '[', ']', '&', '-', '+',
        '*', '/', '\\', '>', '<', '|'
    ]

    # Regular expressions for complex tokens
    D = r"[0-9]"
    L = r"[a-zA-Z]_"
    E = fr"[DdEe][+-]?{D}+"

    constant_1 = fr'{D}+({E})?'
    constant_2 = fr'{D}*"."{D}+({E})?'
    constant_3 = fr'{D}+"."{D}*({E})?'

    transpose_1 = r"'"
    transpose_2 = r"\.'"

    identifier = fr'{L}({L}|{D})*'

    # Regular expressions for simple tokens
    # Logic operations
    t_LE_OP = r"<="
    t_GE_OP = r"\>="
    t_EQ_OP = r"=="
    t_NE_OP = r"(~=)|(!=)"
    t_CONTINUATION = r"[...].*\n"
    # t_AND_AND = r"\&\&"
    # t_OR_OR = r"\|\|"
    # Plus operations
    # t_PLUS_EQ = r"\+="
    # t_PLUS_PLUS = r"\+\+"
    # Minus operations
    # t_MINUS_EQ = r"\-="
    # t_MINUS_MINUS = r"\-\-"

    def __init__(self, **kwargs) -> None:
        self._lexer = lex(module=self, optimize=1, **kwargs)

    def t_error(self, token_: LexToken) -> None:
        """Error handler lexer"""
        print(f"Illegal character {token_.value[0]}")
        token_.lexer.skip(1)

    @TOKEN(constant_1 + constant_2 + constant_3)
    def t_CONSTANT(self, token_: LexToken) -> LexToken:
        ...

    @TOKEN(identifier)
    def t_IDENTIFIER(self, token_: LexToken) -> LexToken:
        token_.type = Lexer.keywords.get(token_.value, "IDENTIFIER")
        return token_

    def t_STRING_LITERAL(self, token_: LexToken) -> LexToken:
        r"""\w+"""
        token_.type = Lexer.keywords.get(token_.value, "STRING_LITERAL")
        return token_

    @TOKEN(transpose_1 + transpose_2)
    def t_TRANSPOSE(self, token_: LexToken) -> LexToken:
        """"""
        ...

    def t_NEWLINE(self, token_: LexToken) -> LexToken:
        r"""\n"""
        token_.lexer.lineno += 1
        token_.type = 'CR'
        return token_

    def input(self, data_: str) -> None:
        self._lexer.input(data_)

    def token(self) -> Generator[LexToken, None, None]:
        for token_ in self._lexer:
            yield token_


data = '''
if (a == 245)
    do_something
else
    to_do



% Just a comment
'''


if __name__ == '__main__':
    m = Lexer()
    m.input(data)
    for token in m.token():
        print(token)
