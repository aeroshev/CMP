from ply.lex import LexToken, TOKEN, lex


class Lexer:
    # Keywords MATLAB
    keywords = {
        "break": "BREAK",
        "clear": "CLEAR",
        "else": "ELSE",
        "end": "END",
        "elseif": "ELSEIF",
        "for": "FOR",
        "function": "FUNCTION",
        "global": "GLOBAL",
        "if": "IF",
        "return": "RETURN",
        "while": "WHILE",
    }

    # All tokens
    tokens = tuple([
        "WORD",
        "NUMBER",
        "ARRAYMUL",
        "ARRAYPOW",
        "ARRAYDIV",
        "ARRAYRDIV",
        "TRANSPOSE",
        "LE_OP",
        "GE_OP",
        "EQ_OP",
        "NE_OP",
        "NEWLINE",
        "LPAREN",
        "RPAREN",
        "ASSIGN",
        "WHITESPACE",
        "COMMENT"
    ] + list(keywords.values()))

    # Ignore symbol
    t_ignore_WHITESPACE = r"\s+"
    t_ignore_COMMENT = r"\#.*"

    # Regular expressions for complex tokens
    word = r"[a-zA-Z_]+"
    newline = r"\n+"
    number = r"\d+"

    # Regular expressions for simple tokens
    t_ARRAYMUL = r"\*"
    t_ARRAYPOW = r"\^"
    t_ARRAYDIV = r"/"
    t_ARRAYRDIV = r"\\"
    t_TRANSPOSE = r"'"
    t_LE_OP = r"<="
    t_GE_OP = r">="
    t_EQ_OP = r"=="
    t_NE_OP = r"~="
    t_LPAREN = r"\("
    t_RPAREN = r"\)"
    t_ASSIGN = r"="

    def t_error(self, token: LexToken) -> None:
        """Error handler lexer"""
        print(f"Illegal character {token.value[0]}")
        token.lexer.skip(1)

    @TOKEN(word)
    def t_WORD(self, token: LexToken) -> LexToken:
        """[a-zA-Z_]+"""
        token.type = Lexer.keywords.get(token.value, "WORD")
        return token

    @TOKEN(number)
    def t_NUMBER(self, token: LexToken) -> LexToken:
        """[digit]+"""
        token.value = int(token.value)
        return token

    @TOKEN(newline)
    def t_NEWLINE(self, token: LexToken) -> None:
        """\n+"""
        token.lexer.lineno += len(token.value)

    def build(self, **kwargs):
        self.lexer = lex(module=self, **kwargs)

    def input(self, data):
        self.lexer.input(data)

    def token(self):
        for token_ in self.lexer:
            yield token_


data = '''
if (a == 245)
    do_something
else
    to_do



# Just a comment
'''


if __name__ == '__main__':
    m = Lexer()
    m.build()
    m.input(data)
    for token in m.token():
        print(token)
