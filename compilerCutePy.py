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

class Token:
    def __init__(self, category, value, line):
        self.type = category
        self.value = value
        self.line = line

    def get_token(self):
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
			print(word)
	if char != "":
		lex()






def close_files():
	file.close()

def main():
	open_cpy_file()
	lex()
	close_files()



main()