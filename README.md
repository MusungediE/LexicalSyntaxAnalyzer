# LexicalSyntaxAnalyzer

Lexical rules (regular expression): 
special symbol, left_paran: ( 
special symbol, right_paran: ) 
special symbol, end of statement: ; 
special symbol, begin of code block: { 
special symbol, end of code block: } 
special symbol, add: + 
special symbol, minor: - 
special symbol, multiply: * 
special symbol, divide: / 
special symbol, modul: % 
special symbol, assign: = 
special symbol, not equal: != 
special symbol, equal: = 
special symbol, less than: < 
special symbol, less or equal: < = 
special symbol, greater than: > 
special symbol, greater or equal: >=
keyword, loop: LP 
keyword, switch statement: SW 
keyword, else: BJ 
keyword, start: GO 
keyword, end: STOP
keyword, store byte1: byte1 
keyword, store byte2: byte2 
keyword, store byte4: byte4 
keyword, store byte8: byte8 
keyword, true: true 
keyword, and: & 
keyword, or: |  
int_lit: [0-9]+ 
identifier: ([a-zA-Z]|_){6,8}
 
PAIRWISE DISJOINT TESt:
syntax rules: s--> 'START' --> |||<var> --> '{' ';' '}' --> 'GO' ['BJ'] --> 'LP' <var> --> 'id' (|) --> 'byte1'|'byte2'|'byte4'|'byte8' --> '=' --> {('*'|'/'|'%') } --> {('+'|'-') } --> 'id'|'int_lit'|'(' ')'
--> {'AND' } --> {'OR' } --> {('!='|'==') } --> {('<='|'>='|'<'|'<') } --> {('*'|'/'|'%') } --> {('+'|'-') } --> 'id'|'int_lit'|'bool_lit'
every rule set in this language conforms to the standard of an LL Grammar and there's no lefthand recursion.

