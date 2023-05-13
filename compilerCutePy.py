import sys


#-min +max for int
temporary_states = {0,1,2,3,4,5,6,7,8,9,10}
final = 99
line = 1
skip_char = 0
next_label = 0
number_of_parameters = 0
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
    '#' : 'TOKEN_hashtag',
    '__name__': 'TOKEN_main_name',
    '”__main__”': 'TOKEN_main'
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
        self.frameLength = None
        self.formalParameters =  list()

    def set_startingQuad(self, Quad):
        self.startingQuad = Quad

    def set_frameLength(self, frameLength):
        self.frameLength = frameLength

    def add_formalParameter(self, fParameter):
        self.formalParameters.append(fParameter)

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
        self.offset = 12

    def add_entity(self, entity):
        self.entities.append(entity)

    def get_offset(self):
        returning_offset = self.offset
        self.offset += 4
        return returning_offset

    def get_nested_level(self):
        return self.nested_level


#class Entity():
#    def __init__(self, name, entity_type):
#        self.name = name
#        self.entity_type = entity_type 

def add_func_formalParameter(name, func_name):
    formal_parameter = FormalParameter(name,"int", "CV")
    func, level = search_entity(func_name)
    func.add_formalParameter(formal_parameter) 

def add_var_entity(name):
    offset = scopes[-1].get_offset()
    scopes[-1].add_entity(Variable(name,"int", offset))

def add_parameter_entity(name):
    offset = scopes[-1].get_offset()
    scopes[-1].add_entity(Parameter(name,"int","CV",offset))

def add_func_entity(name):
    scopes[-1].add_entity(Function(name,"func", 0, 0, 0))

def search_entity(name):
    if scopes == list():
        return
    sc = scopes[-1]
    i = -1
    while sc != None:
        for entity in sc.entities:
            if entity.name == name:
                return entity, sc.get_nested_level()
        i = i - 1
        if len(scopes) >= abs(i):
            sc = scopes[i]
        else:
            return

def update_func_startingQuad(name):
    quad = next_quad()
    func, level = search_entity(name)
    func.set_startingQuad(quad)

def update_func_frameLenght(name, frameLength):
    func, level = search_entity(name)
    func.set_frameLength(frameLength)


def add_new_scope():
    if not scopes:
        scopes.append(Scope(0))
    else:
        scopes.append(Scope(scopes[-1].nested_level + 1))

def remove_scope():
    scopes.pop()

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

def new_temp():
    global tmpVarsList
    global x
    tmpVar = '%_'
    tmpVar += str(x)
    x += 1
    offset = scopes[-1].get_offset()
    scopes[-1].add_entity(TemporaryVariable(tmpVar, "int",offset))
    tmpVarsList.append(tmpVar)
    return tmpVar

def open_cpy_file():
    global file

    if len(sys.argv) < 2:
        print("Error: There is no input file")
        sys.exit()
    if sys.argv[1][-3:] != "cpy":
        print("Error: Input file is not a CutePy file")
        sys.exit()
        
    file = open(sys.argv[1], "r")

def open_asm_file():
    global file_asm
    file_asm = open("final_code.asm", "w")

def gen_asm_code(id):
    for quad in quad_list[id:]:
        quad_to_asm(quad)

def quad_to_asm(quad):
    global number_of_parameters
    if quad.id == 0:
        file_asm.write(f".data\n")
        file_asm.write(f"str_nl: .asciz '\\n' \n")
        file_asm.write(f".text\n")
    file_asm.write(f"Label_{quad.id}:\n")
    if quad.operator == 'jump':
        file_asm.write(f"b Label_{quad.operand3}\n")
    elif quad.operator == '=':
        loadvr(quad.operand1,'1')
        storerv('1', quad.operand3)
    elif quad.operator == 'in':
        file_asm.write(f"li a7, 5\n")
        file_asm.write(f"ecall\n")
        loadvr(quad.operand1, '1')
        file_asm.write(f"mv t1, a0\n")
    elif quad.operator == 'out':
        loadvr(quad.operand1, '1')
        file_asm.write(f"li a0,t1\n")
        file_asm.write(f"li a7,1\n")
    elif quad.operator == 'ret':
        loadvr(quad.operand3, '1')
        file_asm.write("lw t0, -8(sp)\n")
        file_asm.write("sw t1, 0(t0)\n")
    elif quad.operator == '==':
        loadvr(quad.operand1,'1')
        loadvr(quad.operand2,'2')
        file_asm.write(f"beq t1, t2, Label_{quad.operand3}\n")
    elif quad.operator == '>=':
        loadvr(quad.operand1,'1')
        loadvr(quad.operand2,'2')
        file_asm.write(f"bge t1, t2, Label_{quad.operand3}\n")
    elif quad.operator == '<=':
        loadvr(quad.operand1,'1')
        loadvr(quad.operand2,'2')
        file_asm.write(f"ble t1, t2, Label_{quad.operand3}\n")
    elif quad.operator == '!=':
        loadvr(quad.operand1,'1')
        loadvr(quad.operand2,'2')
        file_asm.write(f"bne t1, t2, Label_{quad.operand3}\n")
    elif quad.operator == '>':
        loadvr(quad.operand1,'1')
        loadvr(quad.operand2,'2')
        file_asm.write(f"bgt t1, t2, Label_{quad.operand3}\n")
    elif quad.operator == '<':
        loadvr(quad.operand1,'1')
        loadvr(quad.operand2,'2')
        file_asm.write(f"blt t1, t2, Label_{quad.operand3}\n")
    elif quad.operator == '+':
        loadvr(quad.operand1,'1')
        loadvr(quad.operand2,'2')
        file_asm.write(f"add t1, t1, t2\n")
        storerv('1',quad.operand3)
    elif quad.operator == '-':
        loadvr(quad.operand1,'1')
        loadvr(quad.operand2,'2')
        file_asm.write(f"sub t1, t1, t2\n")
        storerv('1',quad.operand3)
    elif quad.operator == '/':
        loadvr(quad.operand1,'1')
        loadvr(quad.operand2,'2')
        file_asm.write(f"div t1, t1, t2\n")
        storerv('1',quad.operand3)
    elif quad.operator == '*':
        loadvr(quad.operand1,'1')
        loadvr(quad.operand2,'2')
        file_asm.write(f"mul t1, t1, t2\n")
        storerv('1',quad.operand3)
    elif quad.operator == 'begin_block':
        file_asm.write(f"sw ra, 0(sp)\n")
    elif quad.operator == 'end_block':
        file_asm.write(f"lw ra, 0(sp)\n")
        file_asm.write(f"jr ra\n")
    elif quad.operator == 'halt':
        file_asm.write(f"li a0, 0\n")
        file_asm.write(f"li a7, 93\n")
        file_asm.write(f"ecall \n")
    elif quad.operator == 'call':
        number_of_parameters = 0
        called_function, called_level = search_entity(quad.operand1)
        block_function = get_block_function_name()
        if block_function.startswith("main_"):
            calling_level = 0
            calling_framelength = scopes[-1].offset
        else:
            calling_function, calling_level = search_entity(block_function)
            calling_framelength = calling_function.frameLength

        if calling_level == called_level:
            file_asm.write(f"lw t0, -4(sp)\n")
            file_asm.write(f"sw t0, -4(sp)\n")
        else:
            file_asm.write(f"sw sp, -4(fp)\n")

        file_asm.write(f"addi sp, sp, {calling_framelength}\n")
        file_asm.write(f"jal {called_function.startingQuad}\n")
        file_asm.write(f"addi sp, sp, -{calling_framelength}\n")
    elif quad.operator == 'par':
        if quad.operand2 == 'ret':
            entity, entity_level = search_entity(quad.operand1)
            file_asm.write(f"addi t0, sp, -{entity.offset}\n")
            file_asm.write(f"sw t0, -8(fp)\n")
        elif quad.operand2 == 'cv':
            block_function = get_block_function_name()
            if block_function.startswith("main_"):
                calling_framelength = scopes[-1].offset
            else:
                calling_function, calling_level = search_entity(block_function)
                calling_framelength = calling_function.frameLength
            if number_of_parameters == 0:
                file_asm.write(f" addi fp, sp, {calling_framelength}\n")
            number_of_parameters += 1
            loadvr(quad.operand1, '0')
            file_asm.write(f"sw t0, -{12+4*number_of_parameters}(fp)\n")


def get_block_function_name():
    for i in reversed(quad_list):
        if i.operator == 'begin_block':
            return i.operand1

def loadvr(v,r):
    if str(v).isdigit():
        file_asm.write(f"li t{r}\n")
    else:
        entity, entity_level = search_entity(v)
        current_level = scopes[-1].nested_level
        
        if isinstance(entity, Variable) and entity_level == current_level:
            file_asm.write(f"lw t{r} -{entity.offset}(sp)\n")
        elif isinstance(entity, TemporaryVariable) and entity_level == current_level:
            file_asm.write(f"lw t{r} -{entity.offset}(sp)\n")
        elif isinstance(entity, Parameter) and entity_level == current_level:
            file_asm.write(f"lw t{r} -{entity.offset}(sp)\n")
        elif isinstance(entity, Variable) and entity_level < current_level:
            gnvlcode(v)
            file_asm.write(f'lw t{r}, 0(t0)\n')
        elif isinstance(entity, Parameter) and entity_level < current_level:
            gnvlcode(v)
            file_asm.write(f'lw t{r}, 0(t0)\n')

def storerv(r,v):
    entity, entity_level = search_entity(v)
    current_level = scopes[-1].nested_level

    if isinstance(entity, Variable) and entity_level == current_level:
        file_asm.write(f"sw t{r} -{entity.offset}(sp)\n")
    elif isinstance(entity, TemporaryVariable) and entity_level == current_level:
        file_asm.write(f"sw t{r} -{entity.offset}(sp)\n")
    elif isinstance(entity, Parameter) and entity_level == current_level:
        file_asm.write(f"sw t{r} -{entity.offset}(sp)\n")
    elif isinstance(entity, Variable) and entity_level < current_level:
        gnvlcode(v)
        file_asm.write(f'sw t{r}, 0(t0)\n')
    elif isinstance(entity, Parameter) and entity_level < current_level:
        gnvlcode(v)
        file_asm.write(f'sw t{r}, 0(t0)\n')

def gnvlcode(v):
    entity, entity_level = search_entity(v)
    current_level = scopes[-1].nested_level

    file_asm.write(f"lw t0,-4(sp)\n")
    level_difference = current_level - entity_level - 1
    for i in range(level_difference):
        file_asm.write('lw t0, -4(t0)\n')
    file_asm.write(f"addi t0, t0, -{entity.offset}\n")

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
        check_id(word, line)

    #print(' LINE: %d :: '  %token.line + token.family + ' :: ' + token.value)


def check_id(word, line):
    allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_')
    if word in reserved_words_list:
        print(f"Error: line {line} - reserved words cant be used as id")
    if len(word) > 30:
        print(f"Error: line {line} - id {word} is too long (max length is 30)")
        sys.exit()
    elif not word.isidentifier():
        print(f"Error: line {line} - id {word} contains characters other than letters, numbers, and '_', or starts with a number")
        sys.exit()
    elif set(word).issubset(allowed_chars):
        return None
    else:
        print(f"Error: line {line} - id {word} contains characters other than letters, numbers, and '_'")
        sys.exit()

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
                            start_quad_id2 = quad_list[-1].id
                            statements()
                            gen_quad("end_block", name, "_", "_")
                            print_table()
                            gen_asm_code(start_quad_id2)
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
        id_list("declare")

def def_function():
    while(token.family == "TOKEN_def"):
        lex()
        if token.family == "TOKEN_id":
            name = token.value
            add_func_entity(name)
            add_new_scope()
            lex()
            if token.family == "TOKEN_leftParenthesis":
                lex()
                id_list(name)
                if token.family == "TOKEN_rightParenthesis":
                    lex()
                    if token.family == "TOKEN_colon":
                        lex()
                        if token.family == "TOKEN_left_hashbracket":
                            lex()
                            declarations()
                            def_function()
                            update_func_startingQuad(name)
                            gen_quad("begin_block", name, "_", "_")
                            start_quad_id = quad_list[-1].id
                            statements()
                            gen_quad("end_block", name, "_", "_")
                            update_func_frameLenght(name,scopes[-1].offset)
                            print_table()
                            gen_asm_code(start_quad_id)
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
        elif token.value not in ('*', '/'):
            operand1 = expression()
            gen_quad("=", operand1,"_", operand3)
            if token.family == "TOKEN_semiColon":
                lex()
            else:
                error(token.line,";")
        else:
            print(f"Error: line {line} - id or number is expected")
            sys.exit()


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
                error(token.line,")")
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
    else:
        error(token.line,"(")

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
            else:
                error(token.line,"}")
        else:
            error(token.line,"{")
    elif token.family == 'TOKEN_leftBracket':
            lex()
            retval = condition()
            if token.family == 'TOKEN_rightBracket':
                lex()
            else:
                error(token.line,"}")
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
    op_sign = optional_sign()
    term1 = term()
    if op_sign != None:
        temp_sign = new_temp()
        gen_quad(op_sign, 0, term1, temp_sign)
        term1 = temp_sign
    while(token.value == "+" or token.value == "-"):
        op = token.value
        lex()
        if token.value not in ("+", "-", "*", "/"):
            term2 = term()
            temp_var = new_temp()
            gen_quad(op, term1, term2, temp_var)
            term1 = temp_var
        else:
            print(f"Error: line {line} - id or number is expected")
            sys.exit()

    return term1

def optional_sign():
    if token.value == "+" or token.value == "-":
        sign = token.value
        lex()
        return sign

def term():
    factor1 = factor()
    while(token.value == "*" or token.value == '//'):
        op = token.value
        lex()
        if token.value not in ("+", "-", "*", "/"):
            factor2 = factor()
            temp_var = new_temp()
            gen_quad(op, factor1, factor2, temp_var)
            factor1 = temp_var
        else:
            print(f"Error: line {line} - id or number is expected")
            sys.exit()

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
        else:
            error(token.line,")")
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




def id_list(type):
    if token.family == "TOKEN_id":
        if type == "declare":
            add_var_entity(token.value)
        else:
            add_func_formalParameter(token.value,type)
            add_parameter_entity(token.value)
        lex()
        while(token.family == "TOKEN_comma"):
            lex()
            if token.family == "TOKEN_id":
                if type == "declare":
                    add_var_entity(token.value)
                else:
                    add_func_formalParameter(token.value,type)
                    add_parameter_entity(token.value)
                lex()
            else:
                error(token.line,"id")




def call_main_part():
    if token.family == "TOKEN_if":
        lex()
        if token.family == "TOKEN_main_name":
            lex()
            if token.family == "TOKEN_equal":
                lex()
                if token.family == "TOKEN_main":
                    lex()
                    gen_quad("begin_block", "main", "_", "_")
                    if token.family == 'TOKEN_colon':
                        lex()
                        while(token.family == "TOKEN_id"):
                            main_function_call()
                            if token.family != "TOKEN_eof":
                                gen_quad("call", token.value, "_", "_")
                        gen_quad("halt", "_", "_", "_")
                        gen_quad("end_block", "main", "_", "_")
                    else:
                        error(token.line,":")
                else:
                    error(token.line,"'”__main__”")
            else:
                error(token.line,"==")
        else:
            error(token.line,"__name__")



def main_function_call():
    lex()
    if token.family == "TOKEN_leftParenthesis":
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
        error(token.line,"(")

def print_quads():
    for quad in quad_list:
        print(' QUAD: %d :: '  %quad.id + quad.operator  + ', ' + quad.operand1 + ', ' + quad.operand2 + ', ' + quad.operand3)

def print_table():
    print(f"############# SYMBOL TABLE #############")
    for scope in scopes:
        print(f"scope level: {scope.nested_level}")
        print(f" entities:", end ='')
        for entity in scope.entities:
            if isinstance(entity, Function):
                print(f" {entity.name}/{entity.frameLength}, ", end = '')
            else:
                print(f" {entity.name}/{entity.offset}, ", end = '')
        print(" ")
    print("=============================================")

def close_files():
    file.close()

def create_int_code_file():
    with open("int_code.int", "w") as f:
        for quad in quad_list:
            f.write(f"QUAD: {quad.id} :: {quad.operator}, {quad.operand1}, {quad.operand2}, {quad.operand3}\n")

def main():
    open_cpy_file()
    open_asm_file()
    parser()
    close_files()
    #print_quads()
    create_int_code_file()




main()