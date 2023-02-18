import sys


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
	print("Lex hi")


def close_files():
	file.close()


def main():
	open_cpi_file()
	lex()
	close_files()



main()