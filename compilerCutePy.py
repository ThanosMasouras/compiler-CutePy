import sys
## GLOBAL DECLERATIONS ##
temporary_states = {0,1,2,3,4,5,6}
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

final = 99
line = 1

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
	flag = False
	while state in temporary_states:
		
		previus_pos = file.tell()
		char = file.read(1)
		word.append(char)

		if state == 0:
			if char.isspace():
				state = 0
			if char.isalpha():
				state = 1
			if char.isdigit():
				state = 2
			if char == '<':
				state = 3
			if char == '>':
				state = 4
			if char == '#':
				state = 6
			if char in ('+', '-', '*', '/', '=', ',', ';', ':', '{', '}', '(', ')', '[', ']'):
				state = final #temp value
		
		elif state == 1:
			if not char.isalnum():
				state = final
				flag = True
				
		elif state == 2:
			if not char.isdigit():
				state = final
				flag = True


		elif state == 3:
			if char != '>' and char != '=':
				flag = True
			state = final
		elif state == 4:
			if char == "=":
				print(word)
			print(word)
			break
		elif state == 5:
			state = final
		if char.isspace():
			#del word[-1]
			if char == "\n":
				line=line +1
	
	

	if flag == True:
		if len(word) > 1: 
			del word[-1]
		file.seek(previus_pos)

	if state == final:
			print(word)






def close_files():
	file.close()


def main():
	open_cpy_file()
	for i in range(1,22):
		lex()
	close_files()



main()