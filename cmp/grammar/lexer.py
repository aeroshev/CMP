import ply.lex as lex


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
    "RPAREN"
] + list(keywords.values()))

# Ignore symbol
t_ignore = r" "

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


def t_error(token):
    """Error handler lexer"""
    print(f"Illegal character {token.value[0]}")
    token.lexer.skip(1)


@lex.TOKEN(word)
def t_WORD(token: lex.LexToken) -> lex.LexToken:
    """[a-zA-Z_]+"""
    token.type = keywords.get(token.value, "WORD")
    return token


@lex.TOKEN(number)
def t_NUMBER(token: lex.LexToken) -> lex.LexToken:
    """[digit]+"""
    token.value = int(token.value)
    return token


@lex.TOKEN(newline)
def t_NEWLINE(token: lex.LexToken) -> None:
    """\n+"""
    token.lexer.lineno += len(token.value)


lexer = lex.lex()

data = '''
if (a == 245)
    do_something
else
    to_do
'''

lexer.input(data)

if __name__ == '__main__':
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
