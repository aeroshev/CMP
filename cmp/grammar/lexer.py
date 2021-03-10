from typing import Generator

from ply.lex import LexToken, TOKEN, lex


class Lexer:
    # Keywords MATLAB
    keywords = {
        # Loops keywords
        "for": "FOR",
        "while": "WHILE",
        "break": "BREAK",
        "continue": "CONTINUE",
        # Conditions
        "if": "IF",
        "else": "ELSE",
        "elseif": "ELSEIF",
        "end": "END",
        # Catch exceptions
        "try": "TRY",
        "catch": "CATCH",
        # Function
        "function": "FUNCTION",
        "return": "RETURN",
        # Switch
        "switch": "SWITCH",
        "case": "CASE",
        # Other
        "global": "GLOBAL",
        "end_unwind_protect": "END_UNWIND_PROTECT",
        "unwind_protect": "UNWIND_PROTECT",
        "unwind_protect_cleanup": "UNWIND_PROTECT_CLEANUP",
        "otherwise": "OTHERWISE",
        "persistent": "PERSISTENT",
        "clear": "CLEAR",
    }

    # All tokens
    tokens = tuple([
        "COLON",
        # Logic operations
        "LE_OP", "LT_OP", "GE_OP", "GT_OP", "EQ_OP", "NE_OP",
        "AND_AND", "OR_OR",
        # Arithmetic operations
        "MUL", "POW", "DIV", "DIV_DIV", "TRANSPOSE",
        # Plus operations
        "PLUS", "PLUS_EQ", "PLUS_PLUS",
        # Minus operations
        "MINUS", "MINUS_EQ", "MINUS_MINUS",
        # Dot operations
        "DOT", "DOT_DIV", "DOT_DIV_EQ", "DOT_EXP", "DOT_MUL", "DOT_MUL_EQ",
        # Brackets
        "LPAREN", "RPAREN",
        # Other
        "ASSIGN",
        # Complex objects
        "ID",
        "NUMBER",
        # Ignore
        "WHITESPACE",
        "COMMENT"
    ] + list(keywords.values()))

    # Ignore symbol
    t_ignore_WHITESPACE = r"\s+"
    t_ignore_COMMENT = r"\%.*"

    # Regular expressions for complex tokens
    newline = r"\n+"
    number = r"\d+"
    identifier = r"[a-zA-Z_][a-zA-Z_0-9]*"

    # Regular expressions for simple tokens
    t_COLON = r":"
    # Logic operations
    t_LE_OP = r"<="
    t_LT_OP = r"\<"
    t_GE_OP = r"\>="
    t_GT_OP = r"\>"
    t_EQ_OP = r"=="
    t_NE_OP = r"(~=)|(!=)"
    t_AND_AND = r"\&\&"
    t_OR_OR = r"\|\|"
    # Arithmetic operations
    t_MUL = r"\*"
    t_POW = r"\^"
    t_DIV = r"/"
    t_DIV_DIV = r"\\"
    t_TRANSPOSE = r"'"
    # Plus operations
    t_PLUS = r"\+"
    t_PLUS_EQ = r"\+="
    t_PLUS_PLUS = r"\+\+"
    # Minus operations
    t_MINUS = r"\-"
    t_MINUS_EQ = r"\-="
    t_MINUS_MINUS = r"\--"
    # Dot operations
    t_DOT = r"\."
    t_DOT_DIV = r"\./"
    t_DOT_DIV_EQ = r"\./="
    t_DOT_EXP = r"\.\^"
    t_DOT_MUL = r"\.\*"
    t_DOT_MUL_EQ = r"\.\*="
    # Brackets
    t_LPAREN = r"\("
    t_RPAREN = r"\)"

    t_ASSIGN = r"="

    def __init__(self, **kwargs) -> None:
        self._lexer = lex(module=self, optimize=1, **kwargs)

    def t_error(self, token_: LexToken) -> None:
        """Error handler lexer"""
        print(f"Illegal character {token_.value[0]}")
        token_.lexer.skip(1)

    @TOKEN(identifier)
    def t_ID(self, token_: LexToken) -> LexToken:
        """Token [a-zA-Z_]+"""
        token_.type = Lexer.keywords.get(token_.value, "ID")
        return token_

    @TOKEN(number)
    def t_NUMBER(self, token_: LexToken) -> LexToken:
        """Token [digit]+"""
        token_.value = int(token_.value)
        return token_

    @TOKEN(newline)
    def t_NEWLINE(self, token_: LexToken) -> None:
        """Token \n+"""
        token_.lexer.lineno += len(token_.value)

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
