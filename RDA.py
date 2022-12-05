'''
Parse Table Rules

s-> GO <stmt> 
<stmt> -> <switch>
<stmt> -> <loop>
<stmt> -> <block>
<block> -> { <stmt> ; }
<switch> -> SW <boolexpr> <block> BJ <block>
<loop> -> LP <boolexpr> <block>
<var> -> id <type>
<var> -> id <assign>
<type> -> byte1 
<type> -> byte2 
<type> ->  byte4 
<type> -> byte8
<assign> -> = <expr>
<expr> -> <term> * <term>
<expr> -> <term> / <term>
<expr> -> <term> % <term>
<factor> -> id
<factor> -> int_lit
<factor> -> <expr> 
<boolexpr> -> AND <bor>
<boolexpr> -> <bor> 
<bor> -> <beq> OR <beq>
<bor> -> OR <beq>
<beq> -> <brel> != <brel>
<beq> -> <brel> == <brel>
<brel> -> <bexpr> <= <bexpr>
<brel> -> <bexpr> >= <bexpr>
<brel> -> <bexpr> > <bexpr>
<brel> -> <bexpr> < <bexpr>
<bexpr> -> <bterm> * <bterm>
<bexpr> -> <bterm> / <bterm>
<bexpr> -> <bterm> % <bterm>
<bterm> -> <bfactor> + <bfactor>
<bterm> -> <bfactor> - <bfactor>
<bfactor> -> id
<bfactor> -> int_lit
<bfactor> -> bool_lit

------------------------------------------------------

s--> 'GO' <stmt> 
<stmt> --> <switch>|<loop>|<block>|<var>
<block> --> '{' <stmt> ';' '}'
<switch> --> 'SW' <boolexpr> <block> ['BJ'<block>]
<loop> --> 'LP' <boolexpr> <block>
<var> --> 'id' (<type>|<assign>)
<type> --> 'byte1'|'byte2'|'byte4'|'byte8'
<assign> --> '=' <expr>
<expr> --> <term> {('*'|'/'|'%') <term>}
<term> --> <factor> {('+'|'-') <factor>}
<factor> --> 'id'|'int_lit'|'(' <expr> ')'
<boolexpr> --> <bor>{'AND' <bor>}
<bor> --> <beq> {'OR' <beq>}
<beq> --> <brel> {('!='|'==') <brel>}
<brel> --> <bexpr> {('<='|'>='|'>'|'<') <bexpr>}
<bexpr> --> <bterm> {('*'|'/'|'%') <bterm>}
<bterm> --> <bfactor> {('+'|'-') <bfactor>}
<bfactor> --> 'id'|'int_lit'|'bool_lit'

'''

import re

#RDA class is Syntax Analyzer class. parses tokens to check for format

class RDA:
    def __init__(self, tokens) :
        self.tokens = tokens
        self.current = 0
        self.currentToken = tokens[self.current]

    def beginProg(self):
        if self.currentToken == 'GO':
            self.getNextToken()
            self.stmt()
        else:
            self.error()

    def getNextToken(self):
        if self.current < len(self.tokens):
            self.current +=1
        self.currentToken = self.tokens[self.current]
    
    #<stmt> --> <switch>|<loop>|<block>|<var>
    def stmt(self):
        match self.currentToken:
            case 'SW':
                self.switch()
            case 'LP':
                self.loop()
            case 'id':
                self.var()
            case '{':
                self.block()
            case _:
                self.error()

    #<block> --> '{' <stmt> ';' '}'
    def block(self):
        if self.currentToken == '{':
            self.getNextToken()
            while self.currentToken == 'SW' or self.currentToken == 'LP' or self.currentToken == 'id' or self.currentToken == '{':
                self.stmt()
                if self.currentToken == ';':
                    self.getNextToken()
                    self.stmt()
                else:
                    self.error()
            if self.currentToken == '}':
                self.getNextToken()
            else:
                self.error()
        else:
            self.error()

    #<loop> --> 'LP' <boolexpr> <block>
    def loop(self):
        if self.currentToken == 'LP':
            self.getNextToken()
            if self.currentToken == '(':
                self.getNextToken()
                self.boolexpr()
                if self.currentToken == ')':
                    self.getNextToken()
                    self.block()
                else:
                    self.error()
            elif self.currentToken == 'int_lit':
                self.getNextToken()
                self.block()
            else:
                self.error()
            pass
        else:
            self.error()

    #<switch> --> 'SW' '(' <boolexpr> ')' <block>
    def switch(self):
        if self.currentToken == 'SW':
            self.getNextToken()
            if self.currentToken == '(':
                self.getNextToken()
                self.boolexpr()
                if self.currentToken == ')':
                    self.getNextToken()
                    self.block()
                    if self.currentToken == 'BJ':
                        self.getNextToken()
                        self.block()
                else:
                    self.error()
            else:
                self.error()
        else:
            self.error()

    #<var> --> 'id' (<type>|<assign>)
    def var(self):
        if self.currentToken == 'id':
            self.getNextToken()
            #<type> --> 'byte1'|'byte2'|'byte4'|'byte8'
            if self.currentToken == 'byte1'or self.currentToken =='byte2'or self.currentToken =='byte4'or self.currentToken =='byte8':
                self.getNextToken()
            #<assign> --> '=' <expr>
            elif self.currentToken == '=':
                self.getNextToken()
                self.expr()
            else:
                self.error()    
    
    #<expr> --> <term> {('*'|'/'|'%') <term>}
    def expr(self):
        self.term()
        while self.currentToken == '*' or self.currentToken == '/'or self.currentToken == '%':
            self.getNextToken()
            self.term()

    #<term> --> <factor> {('+'|'-') <factor>}
    def term(self):
        self.factor()
        while self.currentToken == '+' or self.currentToken == '-' :
            self.getNextToken()
            self.factor()

    #<factor> --> 'id'|'int_lit'|'(' <expr> ')'
    def factor(self):
        if self.currentToken == 'id' or self.currentToken == 'int_lit':
            self.getNextToken()
        elif self.currentToken == '(':
            self.getNextToken()
            self.expr()
            if self.currentToken == ')':
                self.getNextToken()
            else:
                self.error()
        else:
            self.error()
    
    #<boolexpr> --> <bor>{'AND' <bor>}
    def boolexpr(self):
        self.bor()
        while self.currentToken == '&':
            self.getNextToken()
            self.bor()

    #<bor> --> <beq> {'OR' <beq>}
    def bor(self):
        self.beq()
        while self.currentToken == '|':
            self.getNextToken()
            self.beq()

    #<beq> --> <brel> {('!='|'==') <brel>}
    def beq(self):
        self.brel()
        while self.currentToken == '!=' or self.currentToken == '==':
            self.getNextToken()
        self.brel()

    #<brel> --> <bexpr> {('<='|'>='|'>'|'<') <bexpr>}
    def brel(self):
        self.bexpr()
        while self.currentToken == '<=' or self.currentToken == '>=' or self.currentToken == '>' or self.currentToken == '<':
            self.getNextToken()
            self.bexpr()

    #<bexpr> --> <bterm> {('*'|'/'|'%') <bterm>}
    def bexpr(self):
        self.bterm()
        while self.currentToken == '*' or self.currentToken == '/' or self.currentToken == '%':
            self.getNextToken()
            self.bterm()

    

    #<bterm> --> <bfactor> {('+'|'-') <bfactor>}
    def bfactor(self):
        if self.currentToken == 'id' or self.currentToken == 'int_lit':
            self.getNextToken()
        elif self.currentToken == '(':
            self.getNextToken()
            self.bexpr()
            if self.currentToken == ')':
                self.getNextToken()
            else:
                self.error()
        else:
            self.error()
    #<bfactor> --> 'id'|'int_lit'|'bool_lit'
    def bterm(self):
        self.bfactor()
        while self.currentToken == '+' or self.currentToken == '-' :
            self.getNextToken()
            self.bfactor()

    
    
    #Error in syntax causes this method to run
    def error(self):
        print("Syntax Error in code")
        StopIteration

#regex for variable declaration
def isVariable(str):
    return re.search("[a-z]|[A-Z]|_ {6,8}", str)

#Lex class is lexical analyzer, checks if tokens are valid tokens
class LEX:
    def __init__(self, str):
        self.str = str
    def error(self):
        print("lexical error in code")
        exit()
    def lexChecker(self):
        lexemes = []
        for i in self.str:
            if i == "GO":
                lexemes.append('GO')
            elif i == "LP":
                lexemes.append('LP')
            elif i == "SW":
                lexemes.append('SW')
            elif i == "byte1":
                lexemes.append('byte1')
            elif i == "byte2":
                lexemes.append('byte2')
            elif i == "byte4":
                lexemes.append('byte4')
            elif i == "byte8":
                lexemes.append('byte8')
            elif i == "BJ":
                lexemes.append('BJ')
            elif i == "+":
                lexemes.append('+')
            elif i == "-":
                lexemes.append('-')
            elif i == "*":
                lexemes.append('*')
            elif i == "/":
                lexemes.append('/')
            elif i == "%":
                lexemes.append('%')
            elif i == ">":
                lexemes.append('>')
            elif i == ">=":
                lexemes.append('>=')
            elif i == "<":
                lexemes.append('<')
            elif i == "<=":
                lexemes.append('<=')
            elif i == "==":
                lexemes.append('==')
            elif i == "!=":
                lexemes.append('!=')
            elif i == "{":
                lexemes.append('{')
            elif i == "}":
                lexemes.append('}')
            elif i == "=":
                lexemes.append('=')
            elif i == ";":
                 lexemes.append(';')
            elif i == "STOP":
                lexemes.append('STOP')
            elif i == "(":
                lexemes.append('(')
            elif i == ")":
                lexemes.append(')')
            elif i == "&":
                lexemes.append('&')
            elif i == "true":
                lexemes.append('true')
            elif i == "|":
                lexemes.append('|')
            elif i.isnumeric():
                lexemes.append('int_lit')
            elif isVariable(i):
                lexemes.append('id')
            else:
                self.error()
        return lexemes


f = open("/Users/musungedietongwe/Desktop/CODE/P3Test2/lexx4.txt", 'r')
text = f.read()
lexer = text.split()
stringLex = LEX(lexer)
sL1 = stringLex.lexChecker()
print(sL1)
rdaT = RDA(sL1)
rdaT.beginProg()




