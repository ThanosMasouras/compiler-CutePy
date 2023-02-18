import sys
## GLOBAL DECLERATIONS ##
temporary_states = {0,1,2,3,4,5,6}

class Token:
    def __init__(self, category, value, line):
        self.type = category
        self.value = value
        self.line = line

    def get_token(self):
        return self.token_type

def open_cpi_file():
	global file
	if len(sys.argv) < 2:
		print("Error: There is no input file")
		sys.exit()
	if sys.argv[1][-3:] != "cpi":
		print("Error: Input file is not a CutePy file")
		sys.exit()
	file = open(sys.argv[1], "r")

def lex():

	
	word = []
	state = 0

	while state in temporary_states:
		
		char = file.read(1)
		word.append(char)

		if 1==1:
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
			if char == ':':
				state = 5
			if char == '#':
				state = 6
			if char in ('+', '-', '*', '/', '=', ',', ';', '{', '}', '(', ')', '[', ']'):
				state = 0 #temp value
			
		if char == '':
			sys.exit()
		print ("Char is: " + char + " and State is: ", state)




def close_files():
	file.close()


def main():
	open_cpi_file()
	lex()
	close_files()



main()