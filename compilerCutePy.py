import sys
## GLOBAL DECLERATIONS ##


# 1. na kanw tin anadromi
# 2. na kanw function gia ta error
# 3. na balw kapoia break, logo anadromis
temporary_states = {0,1,2,3,4,5,6,7,8,9,10}
final = 99
line = 1
skip_char = 0
next_label = 0
quad_list = []
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
    '//' : 'TOKEN_divide',
    '<' : 'TOKEN_less',
    '>' : 'TOKEN_greater',
    '=' : 'TOKEN_assignment',
    '==': 'TOKEN_equal',
    '!=': 'TOKEN_nonEqual',
    '<=' : 'TOKEN_lessEqual',
    '>=' : 'TOKEN_greaterEqual',
    '(' : 'TOKEN_leftParenthesis',
    ')' : 'TOKEN_rightParenthesis',
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
    '#}' : 'TOKEN_right_hashbracket',
    '#' : 'TOKEN_hashtag'
}

class Token:
    def __init__(self, family, value, line):
        self.family = family
        self.value = value
        self.line = line

    def get_token_type(self):
        return self.token_type

class Quad():
	def __init__(self, id, op, x, y, z):
		self.id = id
		self.op = op
		self.x = x
		self.y = y
		self.z = z

def gen_quad(id, op, x, y, z):
	global next_label
	next_label +=1
	quad_list.append(Quad(id, op, x, y, z))

def next_quad():
	return next_label

def empty_list():
    return list()


def make_list(label):
    newlist = list()
    newlist.append(label)
    return newlist


def merge(list1, list2):
    return list1 + list2

#backpatch
#newTemp()
def open_cpy_file():
	global file

	if len(sys.argv) < 2:
		print("Error: There is no input file")
		sys.exit()
	if sys.argv[1][-3:] != "cpy":
		print("Error: Input file is not a CutePy file")
		sys.exit()
		
	file = open(sys.argv[1], "r")


def error(line, missing_token):
    print(f"Error: line {line} - {missing_token} is missing")
    exit()

def parser():
	global token
	lex()
	start_rule()

def lex():
	word = []
	state = 0
	global line
	global skip_char
	move_file_pointer = False
	while state in temporary_states:
		previus_pos = file.tell()
		char = file.read(1)
		word.append(char)

		if state == 0:
			if char == "":
				create_token("EOF",line)
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
			if char in ('+', '-', '*', ',', ';', ':', '{', '}', '(', ')', '[', ']'):
				state = final #temp value
			if char == '!':
				state = 6
			if char == '/':
				state = 9
			if char == '=':
				state = 10
		elif state == 1:
			if not char.isalnum() and char != "_" and char != '"' and char != "”":
				state = final
				move_file_pointer = True
		elif state == 2:
			if not char.isdigit():
				state = final
				move_file_pointer = True
		elif state == 3:
			if char != '=':
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
			if char == '$':
				state = 7
		elif state == 6:
			if char != "=":
				move_file_pointer = True
			state = final
		elif state == 7:
			if char == "#":
				state = 8
		elif state == 8:
			if char == "$":
				state = 0
				del word[:]
		elif state == 9:
			if char != "/":
				move_file_pointer = True
			state = final
		elif state == 10:
			if char != "=":
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
	if state == final :
			word = ''.join(word)
			create_token(word,line)



def create_token(word,line):
	global token
	if word in tokens_dict.keys():
		token = Token(tokens_dict[word], word, line)
	elif word.isdigit():
		token = Token(tokens_dict['number'], word, line)
	else:
		token = Token(tokens_dict['ID'], word, line)
	print(' LINE: %d :: '  %token.line + token.family + ' :: ' + token.value)


def start_rule():
	def_main_part()
	call_main_part()

def def_main_part():
	while( token.family == "TOKEN_def"):
		def_main_function()
	

def def_main_function():
	if token.family == "TOKEN_def":
		lex()
		if token.family == "TOKEN_id":
			lex()
			if token.family == "TOKEN_leftParenthesis":
				lex()
				if token.family == "TOKEN_rightParenthesis":
					lex()
					if token.family == "TOKEN_colon":
						lex()
						if token.family == "TOKEN_left_hashbracket":
							lex()
							declarations()
							def_function()
							statements()
							if token.family == "TOKEN_right_hashbracket":
								lex()
							else:
								error(token.line, "#}")
						else:
							error(token.line, "#{")
					else:
						error(token.line, ":")
				else:
					error(token.line, ")")
			else:
				error(token.line, "(")
		else:
			error(token.line, "id")
	else:
		error(token.line, "def")


def declarations():
	while(token.family == "TOKEN_hashtag"):
		lex()
		if token.family == "TOKEN_declare":
			lex()
			declaration_line()
		else:
			error(token.line, "declare")

def declaration_line():
	if token.family == "TOKEN_id":
		lex()
		id_list()

def def_function():
	while(token.family == "TOKEN_def"):
		lex()
		if token.family == "TOKEN_id":
			lex()
			if token.family == "TOKEN_leftParenthesis":
				lex()
				if token.family == "TOKEN_id":
					lex()
					id_list()
					if token.family == "TOKEN_rightParenthesis":
						lex()
						if token.family == "TOKEN_colon":
							lex()
							if token.family == "TOKEN_left_hashbracket":
								lex()
								declarations()
								def_function()
								statements()
								if token.family == "TOKEN_right_hashbracket":
									lex()
								else:
									error(token.line,"#}")
							else:
								error(token.line,"#{")
						else:
							error(token.line,":")
					else:
						error(token.line,")")
				else:
					error(token.line,"id")
			else:
				error(token.line,"(")
		else:
			error(token.line,"id")


def statements():
	while( token.family in ('TOKEN_id', 'TOKEN_print', 'TOKEN_return', 'TOKEN_if', 'TOKEN_while')):
		statement()

def statement():
	if token.family in ('TOKEN_id', 'TOKEN_print', 'TOKEN_return'):
		simple_statement()
	elif token.family in ("TOKEN_if", "TOKEN_while"):
		structured_statement()

def simple_statement():
	if token.family == 'TOKEN_id':
		assignment_stat()
	elif token.family == 'TOKEN_print':
		print_stat()
	elif token.family == 'TOKEN_return':
		return_stat()

def structured_statement():
	if token.family == 'TOKEN_if':
		if_stat()
	elif token.family == 'TOKEN_while':
		while_stat()



def assignment_stat():
	lex()
	if token.family == "TOKEN_assignment":
		lex()
		if token.value == "int":
			lex()
			if token.family == "TOKEN_leftParenthesis":
				lex()
				if token.family == "TOKEN_input":
					lex()
					if token.family == "TOKEN_leftParenthesis":
						lex()
						if token.family == "TOKEN_rightParenthesis":
							lex()
							if token.family == "TOKEN_rightParenthesis":
								lex()
								if token.family == "TOKEN_semiColon":
									lex()
								else:
									error(token.line,";")
							else:
								error(token.line,")")
						else:
							error(token.line,")")
					else:
						error(token.line,"(")
				else:
					error(token.line,"iput")
			else:
				error(token.line,"(")
		else:
			expression()
			if token.family == "TOKEN_semiColon":
				lex()
			else:
				error(token.line,";")


def print_stat():
		lex()
		if token.family == "TOKEN_leftParenthesis":
			lex()
			expression()
			if token.family == "TOKEN_rightParenthesis":
				lex()
				if token.family == "TOKEN_semiColon":
					lex()
				else:
					error(token.line,":")
			else:
				error(token.line,")")
		else:
			error(token.line,"(")
	
def return_stat():
		lex()
		if token.family == "TOKEN_leftParenthesis":
			lex()
			expression()
			if token.family == "TOKEN_rightParenthesis":
				lex()
				if token.family == "TOKEN_semiColon":
					lex()
				else:
					error(token.line,";")
			else:
				error(token.line,"dd)")
		else:
			error(token.line,"(")
	

def if_stat():
	lex()
	if token.family == "TOKEN_leftParenthesis":
		lex()
		condition()
		if token.family == "TOKEN_rightParenthesis":
			lex()
			if token.family == "TOKEN_colon":
				lex()
				if token.family == "TOKEN_left_hashbracket":
					lex()
					statements()
					if token.family == "TOKEN_right_hashbracket":
						lex()	
					else:
						error(token.line,"#}")
				else:
					statement()
			else:
				error(token.line,":")
		else:
			error(token.line,")")

		if token.family =="TOKEN_else":
			lex()
			if token.family =="TOKEN_colon":
				lex()
				if token.family =="TOKEN_left_hashbracket":
					lex()
					statements()
					if token.family == "TOKEN_right_hashbracket":
						lex()
					else:
						error(token.line,"#}")
				else:
					statement()
			else:
				error(token.line,":")

def while_stat():
	lex()
	if token.family == "TOKEN_leftParenthesis":
		lex()
		condition()
		if token.family == "TOKEN_rightParenthesis":
			lex()
			if token.family == "TOKEN_colon":
				lex()
				if token.family == "TOKEN_left_hashbracket":
					lex()
					statements()
					if token.family == "TOKEN_right_hashbracket":
						lex()	
					else:
						error(token.line,"#}")
				else:
					statement()
			else:
				error(token.line,":")
		else:
			error(token.line,")")
	else:
		error(token.line,"(")

def condition():
	bool_term()
	while(token.value == 'or'):
		lex()
		bool_term()

def bool_term():
	bool_factor()
	while(token.value == 'and'):
		lex()
		bool_factor()

def bool_factor():
	if token.value == "not":
		lex()
		if token.family == 'TOKEN_leftBracket':
			condition()
			lex()
			if token.family == 'TOKEN_rightBracket':
				lex()
	elif token.family == 'TOKEN_leftBracket':
			condition()
			lex()
			if token.family == 'TOKEN_rightBracket':
				lex()
	else:
		expression()
		if token.value in ['==','<','>','!=','<=','>=']:
			lex()
			expression()



def expression():
	optional_sign()
	term()
	while(token.value == "+" or token.value == "-"):
		lex()
		expression()

def optional_sign():
	if token.value == "+":
		lex()

def term():
	factor()
	while(token.value == "*" or token.value == '//'):
		lex()
		term()

def factor():

	if token.family == "TOKEN_number":
		lex()
	elif token.family == "TOKEN_leftParenthesis":
		lex()
		expression()
		if token.family == "TOKEN_rightParenthesis":
			lex()
	elif token.family == "TOKEN_id":
		lex()
		idtail()

def idtail():
	if token.family == "TOKEN_leftParenthesis":
		lex()
		actual_par_list()
		if token.family == "TOKEN_rightParenthesis":
			lex()
def actual_par_list():
	expression()
	while(token.family == "TOKEN_comma"):
		lex()
		expression()




def id_list():
	while(token.family == "TOKEN_comma"):
		lex()
		if token.family == "TOKEN_id":
			lex()




def call_main_part():
	if token.family == "TOKEN_if":
		lex()
		if token.value == '__name__':
			lex()
			if token.family == "TOKEN_equal":
				lex()
				if token.value == '”__main__”':
					lex()
					if token.family == 'TOKEN_colon':
						lex()
						while(token.family == "TOKEN_id"):
							main_function_call()


def main_function_call():
	lex()
	if token.family == "TOKEN_leftParenthesis":
		lex()
		if token.family == "TOKEN_rightParenthesis":
			lex()
			if token.family == "TOKEN_semiColon":
				lex()


def close_files():
	file.close()

def main():
	open_cpy_file()
	parser()
	close_files()



main()