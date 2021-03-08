import ply.lex as lex

keywords = {
    "BREAK": "break",
    "CLEAR": "clear",
    "ELSE": "else",
    "END": "end",
    "ELSEIF": "elseif",
    "FOR": "for",
    "FUNCTION": "function",
    "GLOBAL": "global",
    "IF": "if",
    "RETURN": "return",
    "WHILE": "while"
}

tokens = tuple([
    "DECLARATION",
    "WORD",
    "ARRAYMUL",
    "ARRAYPOW",
    "ARRAYDIV",
    "ARRAYRDIV",
    "TRANSPOSE",
    "LE_OP",
    "GE_OP",
    "EQ_OP",
    "NE_OP",
    "NEWLINE"
] + list(keywords))


t_DECLARATION = r"[DdEe][+-][0-9]+"
t_ARRAYMUL = r"\.\*"
t_ARRAYPOW = r"\.\^"
t_ARRAYDIV = r"\.\/"
t_ARRAYRDIV = r"\.\\"
t_TRANSPOSE = r"\.\'"
t_LE_OP = r"<="
t_GE_OP = r">="
t_EQ_OP = r"=="
t_NE_OP = r"~="
t_NEWLINE = r"\n"


def t_error(token):
    print(f"Illegal character {token.value[0]}")
    token.lexer.skip(1)


def t_WORD(t):
    """r'[a-zA-Z_]'"""
    t.type = keywords.get(t.value.upper(), 'IF')
    return t


lexer = lex.lex()

data = '''
ifD+34.*
'''

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
