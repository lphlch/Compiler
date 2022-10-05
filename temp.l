
%option noyywrap

%{
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    int lineno = 1;
    void print(char *token_type);
    void yyerror();


    // struct for the symbol table
    struct symbol_table {
        char *name;
        char *type;
        int value;
        struct symbol_table *next;
    };

    // count of inbuilt data types
    int _r_void = 0;
    int _r_char = 0;
    int _r_int = 0;
    int _r_float = 0;
    int _r_double = 0;
    int _r_string = 0;

    // count of loops
    int _r_if = 0;
    int _r_else = 0;
    int _r_while = 0;
    int _r_for = 0;
    int _r_continue = 0;
    int _r_break = 0;

    // count of math operators
    int _r_plus = 0;
    int _r_minus = 0;
    int _r_multiply = 0;
    int _r_divide = 0;
    int _r_increase = 0;
    int _r_decrease = 0;

    // count of relational operators
    int _r_or = 0;
    int _r_and = 0;
    int _r_not = 0;
    int _r_equal = 0;
    int _r_not_equal = 0;

    // count of logical operators
    int _r_less_than = 0;
    int _r_greater_than = 0;
    int _r_less_than_equal = 0;
    int _r_greater_than_equal = 0;

    // count of brackets
    int _r_left_bracket = 0;
    int _r_right_bracket = 0;
    int _r_left_curly_bracket = 0;
    int _r_right_curly_bracket = 0; 
    int _r_left_square_bracket = 0;
    int _r_right_square_bracket = 0;

    // count of other symbols
    int _r_simi_colon = 0;
    int _r_comma = 0;
    int _r_dot = 0;
    int _r_assign = 0;


    int _r_return = 0;





%}

%x ML_COMMENT
preprocessor_directives #.*
alpha       [a-zA-Z]
digit       [0-9]
alnum       {alpha}|{digit}
print       [ -~]
ARRAY       ({alpha}+{alnum}*"[".+"]")|({alpha}+{alnum}*"["+"]")
ID          {alpha}+{alnum}*
ICONST      "0"|[0-9]{digit}*
FCONST      "0"|{digit}*"."{digit}+
CCONST      (\'{print}\')|(\'\\[nftrbv]\')
STRING      \"{print}*\"
%%

"//".*                  { printf("SINGLE_COMMENT at line %d\n", lineno); } 
"/*"                    { printf("MULTY_COMMENT from line %d ", lineno); BEGIN(ML_COMMENT); }
<ML_COMMENT>"*/"        { printf("to line %d\n", lineno); BEGIN(INITIAL); }
<ML_COMMENT>[^*\n]+     
<ML_COMMENT>"*"         
<ML_COMMENT>"\n"        { lineno += 1; }

"char"|"CHAR"           { print("KEYWORD_CHAR"); _r_char += 1; }
"int"|"INT"             { print("KEYWORD_INT"); _r_int += 1; }
"float"|"FLOAT"         { print("KEYWORD_FLOAT"); _r_float += 1; }
"double"|"DOUBLE"       { print("KEYWORD_DOUBLE"); _r_double += 1; }
"void"|"VOID"           { print("KEYWORD_VOID"); _r_void += 1; }

"if"|"IF"               { print("KEYWORD_IF"); _r_if += 1; }
"else"|"ELSE"           { print("KEYWORD_ELSE"); _r_else += 1; }
"while"|"WHILE"         { print("KEYWORD_WHILE"); _r_while += 1; }
"for"|"FOR"             { print("KEYWORD_FOR"); _r_for += 1; }
"continue"|"CONTINUE"   { print("KEYWORD_CONTINUE"); _r_continue += 1; }
"break"|"BREAK"         { print("KEYWORD_BREAK"); _r_break += 1; }

"return"|"RETURN"       { print("KEYWORD_RETURN"); _r_return += 1; }

"+"                     { print("PLUSOP"); _r_plus += 1; }
"-"                     { print("MINUSOP"); _r_minus += 1; }
"*"                     { print("MULOP"); _r_multiply += 1; }
"/"                     { print("DIVOP"); _r_divide += 1; }
"++"                    { print("INCR"); _r_increase += 1; }
"--"                    { print("DECR"); _r_decrease += 1; }

"||"                    { print("OROP"); _r_or += 1; }
"&&"                    { print("ANDOP"); _r_and += 1; }
"!"                     { print("NOTOP"); _r_not += 1; }
"=="                    { print("EQUOP"); _r_equal += 1; }
"!="                    { print("NEQUOP"); _r_not_equal += 1; }

">"                     { print("GREATOP"); _r_greater_than += 1; }
"<"                     { print("LESSOP"); _r_less_than += 1; }
">="                    { print("GREATEOP"); _r_greater_than_equal += 1; }
"<="                    { print("LESSEOP"); _r_less_than_equal += 1; }

"("             { print("LPAREN"); _r_left_bracket += 1; }
")"             { print("RPAREN"); _r_right_bracket += 1; }
"["             { print("LBRACK"); _r_left_square_bracket += 1; }
"]"             { print("RBRACK"); _r_right_square_bracket += 1; }
"{"             { print("LBRACE"); _r_left_curly_bracket += 1; }
"}"             { print("RBRACE"); _r_right_curly_bracket += 1; }

";"             { print("SEMI"); _r_simi_colon += 1; }
","             { print("COMMA"); _r_comma += 1; }
"="             { print("ASSIGN"); _r_assign += 1; }
'#'             { print("END");}

{preprocessor_directives} { print("PREPROCESSOR DIRECTIVES"); }
{ARRAY}         { print("ARRAY"); }
{ID}            { print("ID"); }
{ICONST}        { print("ICONST"); }
{FCONST}        { print("FCONST"); }
{CCONST}        { print("CCONST"); }
{STRING}        { print("STRING"); }
 
 
"\n"            { lineno += 1; }
[ \t\r\f]+          /* eat up whitespace */
 
.               { yyerror("Unrecognized character"); }
 
%%
int a;
void print(char *token_type){
    a++;
    printf("symbol: %s\ttoken: %s\tlineno: %d\n", yytext, token_type, lineno);
}
 
void yyerror(char *message){
    printf("Error: \"%s\" in line %d. Token = %s\n", message, lineno, yytext);
    exit(1);
}
 
int main(int argc, char *argv[]){
    yyin = fopen(argv[1], "r");
    yylex();
    fclose(yyin);
    printf("Total %d", a);
    return 0;
}