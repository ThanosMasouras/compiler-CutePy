import sys

# 1. o endiamesos kodikas exei ulopoihthei kai tha ton breite sto arxeio int_code.int
# 2. o pinakas sumbolwn den exei oloklirwthei akoma, tha einai etoimos mazi me ton teliko
# 3. sto print tha deite apla ta basika scopes me ta entities tous.
# 4. leipoun offset parameters ktl.
temporary_states = {0,1,2,3,4,5,6,7,8,9,10}
final = 99
line = 1
skip_char = 0
next_label = 0
quad_list = []
tmpVarsList = []
x = 0
scopes = []
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

class Token():
    def __init__(self, family, value, line):
        self.family = family
        self.value = value
        self.line = line

    def get_token_type(self):
        return self.token_type

class Quad():
    def __init__(self, id, operator, operand1, operand2, operand3):
        self.id = id
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2
        self.operand3 = operand3

class Variable():
    def __init__(self, name, datatype, offset):
        self.name = name
        self.datatype = datatype
        self.offset = offset

class Parameter():
    def __init__(self, name, datatype, mode, offset):
        self.name = name
        self.datatype = datatype
        self.mode = mode
        self.offset = offset

class Function():
    def __init__(self, name, datatype, startingQuad, frameLength, formalParameters):
        self.name = name
        self.datatype = datatype
        self.startingQuad = startingQuad
        self.frameLength = frameLength
        self.formalParameters =  formalParameters

class FormalParameter():
    def __init__(self, name, datatype, mode):
        self.name = name
        self.datatype = datatype
        self.mode = mode

class TemporaryVariable():
    def __init__(self, name, datatype, offset):
        self.name = name
        self.datatype = datatype
        self.offset = offset

class Scope():
    def __init__(self, nested_level):
        self.nested_level = nested_level
        self.entities = list()

    def addEntity(self, entity):
        self.entities.append(entity)

class Entity():
    def __init__(self, name, entity_type):
        self.name = name
        self.entity_type = entity_type 

def add_new_entity(name, class_entity):
    if class_entity == "VAR":
        scopes[-1].addEntity(Variable(name,"int",0))
    if class_entity == "FUNC":
        scopes[-1].addEntity(Function(name,"func",0,0,0))

def add_new_scope():
    if not scopes:
        scopes.append(Scope(0))
    else:
        scopes.append(Scope(scopes[-1].nested_level + 1))

def remove_scope():
    scopes.pop()
#def search_entity():

def gen_quad(operator, operand1, operand2, operand3):
    global next_label
    global quad
    quad = Quad(next_label, operator, operand1, operand2, operand3)
    next_label +=1
    quad_list.append(quad)
    #print(' QUAD: %d :: '  %quad.id + quad.operator  + ', ' + quad.operand1 + ', ' + quad.operand2 + ', ' + quad.operand3)

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

def backpatch(list, label):
    global quad_list
    for quad in quad_list:
        if quad.id in list:
            quad.operand3 = str(label)

def new_temp(): #returns a new temporary variable as T_x where x is an integer
    global tmpVarsList
    global x
    tmpVar = '%_'
    tmpVar += str(x)
    x += 1
    tmpVarsList.append(tmpVar)
    return tmpVar

#backpatch
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
    #print(' LINE: %d :: '  %token.line + token.family + ' :: ' + token.value)


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
            name = token.value
            #add_new_entity(name,"FUNC")
            add_new_scope()
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
                            gen_quad("begin_block", name, "_", "_")
                            statements()
                            gen_quad("end_block", name, "_", "_")
                            print_table()
                            remove_scope()
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
    #if token.family == "TOKEN_id":
    #    add_new_entity(token.value,"VAR")
        id_list()

def def_function():
    while(token.family == "TOKEN_def"):
        lex()
        if token.family == "TOKEN_id":
            name = token.value
            add_new_entity(name,"FUNC")
            add_new_scope()
            lex()
            if token.family == "TOKEN_leftParenthesis":
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
                            gen_quad("begin_block", name, "_", "_")
                            statements()
                            gen_quad("end_block", name, "_", "_")
                            print_table()
                            remove_scope()
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
        assignment_stat(token.value)
    elif token.family == 'TOKEN_print':
        print_stat()
    elif token.family == 'TOKEN_return':
        return_stat()

def structured_statement():
    if token.family == 'TOKEN_if':
        if_stat()
    elif token.family == 'TOKEN_while':
        while_stat()



def assignment_stat(operand3):
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
                                    gen_quad("in", operand3, "_", "_")
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
            operand1 = expression()
            gen_quad("=", operand1,"_", operand3)
            if token.family == "TOKEN_semiColon":
                lex()
            else:
                error(token.line,";")


def print_stat():
        lex()
        if token.family == "TOKEN_leftParenthesis":
            lex()
            operand1 = expression()
            gen_quad("out",operand1, "_","_")
            if token.family == "TOKEN_rightParenthesis":
                lex()
                if token.family == "TOKEN_semiColon":
                    lex()
                else:
                    error(token.line,";")
            else:
                error(token.line,")")
        else:
            error(token.line,"(")
    
def return_stat():
        lex()
        if token.family == "TOKEN_leftParenthesis":
            lex()
            operand1 = expression()
            gen_quad("ret", "_","_", operand1)
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
        (b_true, b_false) = condition()
        if token.family == "TOKEN_rightParenthesis":
            lex()
            if token.family == "TOKEN_colon":
                lex()
                if token.family == "TOKEN_left_hashbracket":
                    lex()
                    backpatch(b_true, next_quad())
                    statements()
                    skip_list = make_list(next_quad())
                    gen_quad("jump", "_", "_", str(next_quad()+1))
                    backpatch(b_false, next_quad()) 
                    if token.family == "TOKEN_right_hashbracket":
                        lex()   
                    else:
                        error(token.line,"#}")
                else:
                    backpatch(b_true, next_quad())
                    statement()
                    skip_list = make_list(next_quad())
                    gen_quad("jump", "_", "_", str(next_quad()+1))
                    backpatch(b_false, next_quad())          
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
                    backpatch(skip_list, next_quad())
            else:
                error(token.line,":")

def while_stat():
    lex()
    b_quad = next_quad()
    if token.family == "TOKEN_leftParenthesis":
        lex()
        (b_true, b_false) = condition()
        if token.family == "TOKEN_rightParenthesis":
            lex()
            if token.family == "TOKEN_colon":
                lex()
                if token.family == "TOKEN_left_hashbracket":
                    lex()
                    backpatch(b_true, next_quad())
                    statements()
                    gen_quad('jump','_','_',str(b_quad))
                    backpatch(b_false, next_quad())
                    if token.family == "TOKEN_right_hashbracket":
                        lex()   
                    else:
                        error(token.line,"#}")
                else:
                    backpatch(b_true, next_quad())
                    statement()
                    gen_quad('jump','_','_',str(b_quad))
                    backpatch(b_false, next_quad())
            else:
                error(token.line,":")
        else:
            error(token.line,")")
    else:
        error(token.line,"(")

def condition():
    (b_true, b_false) = (q1_true, q1_false) = bool_term()
    while(token.value == 'or'):
        backpatch(b_false, next_quad())
        lex()
        (q2_true, q2_false) = bool_term()
        b_true  = merge(b_true, q2_true)
        b_false = q2_false

    return (b_true, b_false)

def bool_term():
    (q_true, q_false) = (r1_true, r1_false) = bool_factor()
    while(token.value == 'and'):
        backpatch(q_true, next_quad())
        lex()
        (r2_true, r2_false) = bool_factor()
        q_false = merge(q_false, r2_false)
        q_true  = r2_true
    return (q_true, q_false)

def bool_factor():
    if token.value == "not":
        lex()
        if token.family == 'TOKEN_leftBracket':
            lex()
            retval = condition()
            if token.family == 'TOKEN_rightBracket':
                lex()
    elif token.family == 'TOKEN_leftBracket':
            lex()
            retval = condition()
            if token.family == 'TOKEN_rightBracket':
                lex()
    else:
        exp1 = expression()
        if token.value in ['==','<','>','!=','<=','>=']:
            op = token.value
            lex()
            exp2 = expression()
            r_true = make_list(next_quad())
            gen_quad(op, exp1, exp2, "_")
            r_false = make_list(next_quad())
            gen_quad('jump', "_", "_", "_")
            retval = (r_true, r_false)
    return retval


def expression():
    optional_sign()
    term1 = term()
    while(token.value == "+" or token.value == "-"):
        op = token.value
        lex()
        term2 = term()
        temp_var = new_temp()
        gen_quad(op, term1, term2, temp_var)
        term1 = temp_var

    return term1

def optional_sign():
    if token.value == "+" or token.value == "-":
        lex()

def term():
    factor1 = factor()
    while(token.value == "*" or token.value == '//'):
        op = token.value
        lex()
        factor2 = factor()
        temp_var = new_temp()
        gen_quad(op, factor1, factor2, temp_var)
        factor1 = temp_var
    return factor1

def factor():
    factor_value = 0
    if token.family == "TOKEN_number":
        factor_value = token.value
        lex()
    elif token.family == "TOKEN_leftParenthesis":
        lex()
        factor_value = expression()
        if token.family == "TOKEN_rightParenthesis":
            lex()
    elif token.family == "TOKEN_id":
        factor_value = token.value
        lex()
        tail = idtail()
        if tail:
            temp_var = new_temp()
            gen_quad("par", temp_var, "ret", "_")
            gen_quad("call", factor_value, "_", "_")
            factor_value = temp_var
    return factor_value

def idtail():
    if token.family == "TOKEN_leftParenthesis":
        lex()
        actual_par_list()
        if token.family == "TOKEN_rightParenthesis":
            lex()
        return True

def actual_par_list():
    operand1 = expression()
    gen_quad("par", operand1, "cv", "_")
    while(token.family == "TOKEN_comma"):
        lex()
        operand1 = expression()
        gen_quad("par", operand1, "cv", "_")




def id_list():
    if token.family == "TOKEN_id":
        add_new_entity(token.value,"VAR")
        lex()
        while(token.family == "TOKEN_comma"):
            lex()
            if token.family == "TOKEN_id":
                add_new_entity(token.value,"VAR")
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

def print_quads():
    for quad in quad_list:
        print(' QUAD: %d :: '  %quad.id + quad.operator  + ', ' + quad.operand1 + ', ' + quad.operand2 + ', ' + quad.operand3)

def print_table():
    for scope in scopes:
        print(f"scope level: {scope.nested_level}")
        print(f" entities:", end ='')
        for entity in scope.entities:
            print(f" {entity.name}, ", end = '')
        print(" ")
    print("=============================================")

def close_files():
    file.close()

def create_int_code_file():
    with open("int_code.int", "w") as f:
        for quad in quad_list:
            f.write(f"QUAD: {quad.id} :: {quad.operator}, {quad.operand1}, {quad.operand2}, {quad.operand3}\n")

def main():
    print(f"############# SYMBOL TABLE #############")
    open_cpy_file()
    parser()
    close_files()
    print_quads()
    create_int_code_file()




main()