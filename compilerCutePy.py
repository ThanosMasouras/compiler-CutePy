import sys
## GLOBAL DECLERATIONS ##
temporary_states = {0,1,2,3,4,5,6}
final = 99
line = 1
reserved_words_list = [
    'def', 
    'declare',
    'if',
    'else',
    'while',
    'not',
    'and',
    'or',
    'return',
    'input',
    'print']

tokens_dict = {
    '+' : 'TOKEN_plus',
    '-' : 'TOKEN_minus',
    '*' : 'TOKEN_times',
    '/' : 'TOKEN_slash',
    '<' : 'TOKEN_less',
    '>' : 'TOKEN_greater',
    '=' : 'TOKEN_equal',
    '<>': 'TOKEN_nonEqual',
    '<=' : 'TOKEN_lessEqual',
    '>=' : 'TOKEN_greaterEqual',
    '(' : 'TOKEN_leftP',
    ')' : 'TOKEN_rightP',
    '[' : 'TOKEN_leftBracket',
    ']' : 'TOKEN_rightBracket',
    '{' : 'TOKEN_leftBrace',
    '}' : 'TOKEN_rightBrace',
    ';' : 'TOKEN_semiColon',
    ':' : 'TOKEN_colon',
    ',' : 'TOKEN_comma',
    '.' : 'TOKEN_programm_end',
    'declare' : 'TOKEN_declare',
    'def' : 'TOKEN_def',
    'if' : 'TOKEN_if',
    'else' : 'TOKEN_else',
    'while' : 'TOKEN_while',
    'default' : 'TOKEN_default',
    'not' : 'TOKEN_not',
    'and' : 'TOKEN_and',
    'or' : 'TOKEN_or',
    'return' : 'TOKEN_return',
    'input' : 'TOKEN_input',
    'print' : 'TOKEN_print',
    'EOF' : 'TOKEN_eof',
    'ID' : 'TOKEN_id',
    "number" : 'TOKEN_number',
    '.' : 'TOKEN_dot',
    '#$' : 'TOKEN_comment',
    '#{' : 'TOKEN_left_hashbracket',
    '#}' : 'TOKEN_rigth_hashbracket',
    '#' : 'TOKEN_hashtag'
}

class Token:
    def __init__(self, category, value, line):
        self.type = category
        self.value = value
        self.line = line

    def get_token_type(self):
        return self.token_type

def open_cpy_file():
	global file

	if len(sys.argv) < 2:
		print("Error: There is no input file")
		sys.exit()
	if sys.argv[1][-3:] != "cpy":
		print("Error: Input file is not a CutePy file")
		sys.exit()
		
	file = open(sys.argv[1], "r")

def lex():
	word = []
	state = 0
	global line
	move_file_pointer = False
	while state in temporary_states:
		previus_pos = file.tell()
		char = file.read(1)
		word.append(char)

		if state == 0:
			if char == "":
				break
			if char.isspace():
				state = 0
			if char.isalpha() or char == "_":
				state = 1
			if char.isdigit():
				state = 2
			if char == '<':
				state = 3
			if char == '>':
				state = 4
			if char == '#':
				state = 5
			if char in ('+', '-', '*', '/', '=', ',', ';', ':', '{', '}', '(', ')', '[', ']','”'):
				state = final #temp value
		elif state == 1:
			if not char.isalnum() and char != "_":
				state = final
				move_file_pointer = True
		elif state == 2:
			if not char.isdigit():
				state = final
				move_file_pointer = True
		elif state == 3:
			if char not in ('>','='):
				move_file_pointer = True
			state = final
		elif state == 4:
			if char != "=":
				move_file_pointer = True
			state = final
		elif state == 5:
			if char not in ('{','}','$'):
				move_file_pointer = True
			state = final
		if char.isspace():
			del word[-1]
			move_file_pointer = False
			if char == "\n":
				line=line +1
	if move_file_pointer == True:
		del word[-1]
		file.seek(previus_pos)
	if state == final:
			word = ''.join(word)
			create_token(word,line)
	if char != "":
		lex()



def create_token(word,line):

	if word in tokens_dict.keys():
		token = Token(tokens_dict[word], word, line)
	elif word.isdigit():
		token = Token(tokens_dict['number'], word, line)
	else:
		token = Token(tokens_dict['ID'], word, line)
	print(' LINE: %d :: '  %token.line + token.type + ' :: ' + token.value)

def close_files():
	file.close()

def main():
	open_cpy_file()
	lex()
	close_files()



main()