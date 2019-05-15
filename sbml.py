import re

class Node:
    def __init__(self):
        print("init node")

    def evaluate(self):
        return 0

    def execute(self):
        return self.evaluate()


class NumberNode(Node):
    def __init__(self, v):
        if ('.' in v):
            self.value = float(v)
        else:
            self.value = int(v)

    def evaluate(self):
        return self.value


class StringNode(Node):
    def __init__(self, v):
        v = re.sub(r'\'', r"'", v)
        v = re.sub(r'\"', r'"', v)
        v = v[1:-1]
        self.value = str(v)

    def evaluate(self):
        return self.value


class BoolNode(Node):
    def __init__(self, v):
        if v == 'true' or v == 'True':
            self.value = True
        elif v == 'false' or v == 'False':
            self.value = False


    def evaluate(self):
        return self.value


class WordGetNode(Node):
    def __init__(self, v1, v2):
        self.v1 = v1.evaluate()
        self.v2 = v2.evaluate()

    def evaluate(self):
        self.value = self.v1[self.v2+1]
        return self.value


class ListNode(Node):
    def __init__(self):
        self.value = []

    def __init__(self, v):
        if v != '':
            self.value = [v.evaluate()]
        else:
            self.value = [v]

    def concat(self, v):
        self.value.insert(0, v.value)

    def add(self, v):
        self.value.append(v.evaluate())

    def evaluate(self):
        count = 0
        for i in self.value:
            if i != '' and (not isinstance(i, int) and not isinstance(i, float)) and i[0] == '\'':
                self.value[count] = i.replace("\'", "")
            elif i != '' and (not isinstance(i, int) and not isinstance(i, float)) and i[0] == '\"':
                self.value[count] = i.replace("\"", "")
            count += 1
        return self.value


class ListGetNode(Node):
    def __init__(self, v1, v2):
        self.v1 = v1.evaluate()
        self.v2 = v2.evaluate()

    def evaluate(self):
        if self.v2 <= self.v1[0].__len__():
            self.value = self.v1[0][self.v2]
        else:
            raise ValueError()
        return self.value

class TupleNode(Node):
    def __init__(self):
        self.value = ()

    def add(self, v):
        if isinstance(v, NumberNode) or isinstance(v, StringNode) or isinstance(v, BoolNode):
            self.value += (v.evaluate(),)
        elif isinstance(v, ListNode):
            self.value += (v.evaluate(),)
        elif isinstance(v, TupleNode):
            self.value += (v.value,)
        else:
            for x in v:
                self.value += (x,)

    def get(self, v):
        if isinstance(v, BopNode):
            if v.evaluate() <= self.value.__len__():
                self.value = self.value[v.evaluate()-1]
        elif v.value <= self.value.__len__():
                self.value = self.value[v.value - 1]
        else:
            raise ValueError()

    def evaluate(self):
        return self.value


class UminusNode(Node):
    def __init__(self, op, v):
        self.v = v
        self.op = op

    def evaluate(self):
        tmp = self.v.evaluate()
        if self.op == '-':
            tmp = -tmp
        return tmp


class NotNode(Node):
    def __init__(self, v):
        self.v = v

    def evaluate(self):
        return not self.v.evaluate()


class inString(Node):
    def __init__(self, op, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.op = op

    def evaluate(self):
        if self.op == 'in':
            return self.v1.evaluate() in self.v2.evaluate()


class BopNode(Node):
    def __init__(self, op, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.op = op

    def evaluate(self):
        if self.op in ['+', '-', '*', '/', 'div', 'mod', '**']:
            return self.bop()
        elif self.op in ['<', '<=', '==', '<>', '>', '>=', 'andalso', 'orelse', 'in']:
            return self.boolop()

    def boolop(self):
        if self.op == '<':
            return self.v1.evaluate() < self.v2.evaluate()
        elif self.op == '>':
            return self.v1.evaluate() > self.v2.evaluate()
        elif self.op == '==':
            return self.v1.evaluate() == self.v2.evaluate()
        elif self.op == '<=':
            return self.v1.evaluate() <= self.v2.evaluate()
        elif self.op == '>=':
            return self.v1.evaluate() >= self.v2.evaluate()
        elif self.op == '<>':
            return self.v1.evaluate() != self.v2.evaluate()
        elif self.op == 'andalso':
            return self.v1.evaluate() and self.v2.evaluate()
        elif self.op == 'orelse':
            return self.v1.evaluate() or self.v2.evaluate()
        elif self.op == 'in':
            return self.v1.evaluate() in self.v2.evaluate()

    def bop(self):
        if type(self.v1.evaluate()) == bool or type(self.v2.evaluate()) == bool:
            raise TypeError()
        elif self.op == '+':
            if type(self.v1.evaluate()) == type(self.v2.evaluate()) and type(self.v1.evaluate()) == str:
                return "\'" + self.v1.evaluate()[1:-1] + self.v2.evaluate()[1:-1] + "\'"
            else:
                return self.v1.evaluate() + self.v2.evaluate()
        elif self.op == '-':
            return self.v1.evaluate() - self.v2.evaluate()
        elif self.op == '*':
            return self.v1.evaluate() * self.v2.evaluate()
        elif self.op == '/' or self.op == 'div':
            return self.v1.evaluate() // self.v2.evaluate()
        elif self.op == 'mod':
            if (type(self.v1.evaluate()) == type(self.v2.evaluate()) and type(self.v1.evaluate()) == int) or (type(self.v1.evaluate()) == type(self.v2.evaluate()) and type(self.v1.evaluate()) == float):
                return self.v1.evaluate() % self.v2.evaluate()
            else:
                raise TypeError()
        elif self.op == '**':
            return self.v1.evaluate() ** self.v2.evaluate()


tokens = (
    'PRINT', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET',
    'NUMBER', 'STRING', 'STRINGS', 'NAME', 'EQUALS', 'BOOLEAN',
    'PLUS', 'MINUS', 'TIMES', 'DIV', 'DIVIDE', 'MOD', 'EXPONENT',
    'LESSTHAN', 'LESSEQUAL', 'ISEQUAL', 'NOTEQUAL', 'GREATERTHAN', 'GREATEREQUAL',
    'ANDALSO', 'ORELSE', 'NOT', 'IN', 'NO',
    'COMMA', 'SEMICOLON', 'CONCAT', 'TRUE', 'TTRUE', 'FFALSE', 'FALSE', 'UMINUS', 'ID'
)

reserved = {
    'andalso': 'ANDALSO',
    'orelse': 'ORELSE',
    'not': 'NOT',
    'in': 'IN',
    'print': 'PRINT',
    'div': 'DIV',
    'mod': 'MOD',

}

# Tokens definition
t_NO = r'\#'
t_TRUE = 'true'
t_FALSE = 'false'
t_TTRUE = 'True'
t_FFALSE = 'False'
t_CONCAT = r'::'
t_COMMA = r','
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EXPONENT = r'\*\*'
t_LESSTHAN = r'<'
t_LESSEQUAL = r'<='
t_ISEQUAL = r'=='
t_NOTEQUAL = r'<>'
t_GREATERTHAN = r'>'
t_GREATEREQUAL = r'>='


def t_NUMBER(t):
    r'\d*(\d\.|\.\d)\d*(e-?\d+)?|\d+'
    try:
        t.value = NumberNode(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_STRING(t):
    r'"([^"\\] | (\\[\\\'\"]))*" | \'([^\'\\]|(\\[\\\'\"]))*\' | "([^"] | ([\'\"]))*" | \'([^\']|([\'\"]))*\''
    t.value = StringNode(t.value)
    return t

def t_BOOLEAN(t):
    r'true | false | True | False'
    t.value = BoolNode(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

# Ignored characters
t_ignore = " \t"


def t_error(t):
    raise ValueError()


# Build the lexer
import ply.lex as lex

lex.lex(debug=0)

# Parsing rules
precedence = (
    ('left', 'ORELSE'),
    ('left', 'ANDALSO'),
    ('right', 'NOT'),
    ('left', 'GREATERTHAN', 'GREATEREQUAL', 'ISEQUAL', 'NOTEQUAL', 'LESSTHAN', 'LESSEQUAL'),
    ('left', 'IN'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'DIV', 'MOD'),
    ('right', 'UMINUS'),
    ('right', 'EXPONENT'),
    ('right', 'CONCAT'),
    ('left', 'NO')
)


def p_print_smt(t):
    """
    print_smt : expression SEMICOLON
    """
    t[0] = t[1]


def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression DIV expression
                  | expression MOD expression
                  | expression EXPONENT expression
                  | expression LESSTHAN expression
                  | expression GREATERTHAN expression
                  | expression ISEQUAL expression
                  | expression NOTEQUAL expression
                  | expression GREATEREQUAL expression
                  | expression LESSEQUAL expression
                  | expression ANDALSO expression
                  | expression ORELSE expression
                  | expression IN expression'''
    t[0] = BopNode(t[2], t[1], t[3])

def p_expression_uminus(t):
    '''expression : MINUS expression %prec UMINUS'''
    t[0] = UminusNode(t[1], t[2])


def p_expression_not(t):
    '''expression : NOT expression'''
    t[0] = NotNode(t[2])


def p_expression_expression(t):
    '''expression : LPAREN expression RPAREN'''
    t[0] = t[2]


def p_expression_factor(t):
    'expression : factor'
    t[0] = t[1]


def p_expression_tuple(t):
    'expression : LPAREN tuple RPAREN'
    t[0] = t[2]


def p_expression_tuple_empty(t):
    'expression : LPAREN RPAREN'
    t[0] = TupleNode()


def p_tuple(t):
    '''tuple : expression COMMA content
            | content COMMA content'''
    a = TupleNode()
    a.add(t[1])
    a.add(t[3])
    t[0] = a


def p_get_value_of_tuple(t):
    '''expression : NO expression expression'''
    if type(t[3]) != ListGetNode:
        t[3].get(t[2])
        t[0] = t[3]
    else:
        t[0] = t[3].execute()


def p_expression_list(t):
    '''expression : LBRACKET list RBRACKET'''
    t[0] = t[2]


def p_expression_empty_list(t):
    '''expression : LBRACKET RBRACKET'''
    # empty list
    t[0] = ListNode("")


def p_list(t):
    'list : list COMMA expression'
    t[1].add(t[3])
    t[0] = t[1]


def p_concat_list(t):
    '''expression : expression CONCAT expression'''
    t[3].concat(t[1])
    t[0] = t[3]


def p_list_single(t):
    'list : expression'
    t[0] = ListNode(t[1])


def p_list_content(t):
    'content : expression'
    t[0] = [t[1].evaluate()]


def p_list_repeat(t):
    'content : expression COMMA content'
    t[0] = [t[1].evaluate()] + t[3]

def p_list_get(t):
    '''expression : list LBRACKET NUMBER RBRACKET'''
    t[0] = ListGetNode(t[1], t[3])


def p_string_get(t):
    '''expression : word LBRACKET NUMBER RBRACKET'''
    t[0] = WordGetNode(t[1], t[3])


def p_expression_string(t):
    '''expression : word'''
    t[0] = t[1]


def p_word_string(t):
    '''word : STRING
            | STRINGS'''
    t[0] = t[1]


def p_factor(t):
    '''factor : NUMBER
              | STRING
              | BOOLEAN'''
    t[0] = t[1]


def p_error(t):
    raise SyntaxError()


import ply.yacc as yacc

yacc.yacc(debug=0)

import sys

if len(sys.argv) != 2:
    sys.exit("invalid arguments")
fd = open(sys.argv[1], 'r')
code = ""

for line in fd:
    code = line.strip()
    try:
        lex.input(code)
        while True:
            token = lex.token()
            if not token:
                break
            #print(token)
        ast = yacc.parse(code)

        print(ast.execute())
    except SyntaxError:
        print("SYNTAX ERROR")
        continue
    except ValueError:
        print("SEMANTIC ERROR")
        continue
    except TypeError:
        print("SEMANTIC ERROR")
        continue
