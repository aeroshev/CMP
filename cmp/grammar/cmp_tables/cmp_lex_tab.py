# cmp_lex_tab.py. This file automatically created by PLY (version 3.11). Don't edit!
_tabversion   = '3.10'
_lextokens    = set(('ARRAY_DIV', 'ARRAY_MUL', 'ARRAY_POW', 'ARRAY_RDIV', 'BREAK', 'CLEAR', 'CONSTANT', 'ELSE', 'ELSEIF', 'END', 'EQ_OP', 'FOR', 'FUNCTION', 'GE_OP', 'GLOBAL', 'IDENTIFIER', 'IF', 'LE_OP', 'NEWLINE', 'NE_OP', 'RETURN', 'STRING_LITERAL', 'TRANSPOSE', 'WHILE'))
_lexreflags   = 48
_lexliterals  = '~;,:=()[]&-+*/\\><|'
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere   = {'INITIAL': [('(?P<t_CONSTANT>[0-9]+([DdEe][+-]?[0-9]+)?|[0-9]*"."[0-9]+([DdEe][+-]?[0-9]+)?|[0-9]+"."[0-9]*([DdEe][+-]?[0-9]+)?)|(?P<t_IDENTIFIER>[a-zA-Z]_([a-zA-Z]_|[0-9])*)|(?P<t_STRING_LITERAL>\'[^\'\\n]*\')|(?P<t_TRANSPOSE>\'\\.\')|(?P<t_NEWLINE>\\n)|(?P<t_NE_OP>(~=)|(!=))|(?P<t_ignore_COMMENTS>\\%.*)|(?P<t_GE_OP>\\>=)|(?P<t_ignore_WHITESPACE>\\s+)|(?P<t_EQ_OP>==)|(?P<t_LE_OP><=)', [None, ('t_CONSTANT', 'CONSTANT'), None, None, None, ('t_IDENTIFIER', 'IDENTIFIER'), None, ('t_STRING_LITERAL', 'STRING_LITERAL'), ('t_TRANSPOSE', 'TRANSPOSE'), ('t_NEWLINE', 'NEWLINE'), (None, 'NE_OP'), None, None, (None, None), (None, 'GE_OP'), (None, None), (None, 'EQ_OP'), (None, 'LE_OP')])]}
_lexstateignore = {'INITIAL': ''}
_lexstateerrorf = {'INITIAL': 't_error'}
_lexstateeoff = {}
