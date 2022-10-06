
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
    int _r_const = 0;

    // count of loops
    int _r_if = 0;
    int _r_else = 0;
    int _r_while = 0;
    int _r_for = 0;
    int _r_continue = 0;
    int _r_break = 0;
    int _r_do = 0;

    // count of math operators
    int _r_plus = 0;
    int _r_minus = 0;
    int _r_multiply = 0;
    int _r_divide = 0;
    int _r_increase = 0;
    int _r_decrease = 0;
    int _r_mod = 0;
    int _r_plus_equal = 0;
    int _r_minus_equal = 0;
    int _r_multiply_equal = 0;
    int _r_divide_equal = 0;
    int _r_mod_equal = 0;


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
    int _r_pointer = 0;
    int _r_quote = 0;


    int _r_return = 0;





%}

%x ML_COMMENT
preprocessor_directives #.*
alpha       [a-zA-Z]
digit       [0-9]
alnum       {alpha}|{digit}
sign        "+"|"-"
print       [ -~]
ARRAY       ({alpha}+{alnum}*"[".+"]")|({alpha}+{alnum}*"["+"]")
ID          {alpha}+{alnum}*
dec_INTEGER {sign}?("0"|[1-9]{digit}*)  
bin_INTEGER {sign}?0b(0|1[0-1]*)
oct_INTEGER {sign}?0(0|[1-7][0-7]*)
hex         ([1-9]|[a-f]|[A-F])([0-9]|[a-f]|[A-F})*
hex_INTEGER {sign}?(0x|0X)(0|hex)
INTEGER     {dec_INTEGER}|{bin_INTEGER}|{oct_INTEGER}|{hex_INTEGER}
FCONST      {dec_INTEGER}+"."+{dec_INTEGER}
EXPFCONST   {dec_INTEGER}+("E"|"e")+{dec_INTEGER}
CCONST      (\'{print}\')|(\'\\[nftrbv]\')
STRING      \"{print}*\"
%%

"//".*                  { printf("SINGLE_COMMENT at line %d\n", lineno); } 
"/*"                    { printf("MULTY_COMMENT from line %d ", lineno); BEGIN(ML_COMMENT); }  //if you read any "/*",you will still in ML_COMMENT state
<ML_COMMENT>"*/"        { printf("to line %d\n", lineno); BEGIN(INITIAL); }  //if in ML_COMMENT state now and read */,that mean you will in initial state,the two rules are match
<ML_COMMENT>[^*\n]+     
<ML_COMMENT>"*"         
<ML_COMMENT>"\n"        { lineno += 1; }//in ML_COMMENT,just update the lineno

  /*inbuilt data types*/
"char"|"CHAR"           { print("KEYWORD_char"); _r_char += 1; }
"int"|"INT"             { print("KEYWORD_int"); _r_int += 1; }
"float"|"FLOAT"         { print("KEYWORD_float"); _r_float += 1; }
"double"|"DOUBLE"       { print("KEYWORD_double"); _r_double += 1; }
"void"|"VOID"           { print("KEYWORD_void"); _r_void += 1; }
"string"|"STRING"       { print("KEYWORD_string");_r_string += 1; }
"const"|"CONST"         { print("KEYWORD_const"); _r_const += 1; }

  /*loops or condition*/
"if"|"IF"               { print("KEYWORD_if"); _r_if += 1; }
"else"|"ELSE"           { print("KEYWORD_else"); _r_else += 1; }
"while"|"WHILE"         { print("KEYWORD_while"); _r_while += 1; }
"for"|"FOR"             { print("KEYWORD_for"); _r_for += 1; }
"continue"|"CONTINUE"   { print("KEYWORD_continue"); _r_continue += 1; }
"break"|"BREAK"         { print("KEYWORD_break"); _r_break += 1; }
"do"|"DO"               { print("KEYWORD_do"); _r_do += 1;}

  /*return*/
"return"|"RETURN"       { print("KEYWORD_return"); _r_return += 1; }

"->"                    { print("pointer"); _r_pointer +=1;}

  /* math operators*/
"+"                     { print("plus_OP"); _r_plus += 1; }
"-"                     { print("minus_OP"); _r_minus += 1; }
"*"                     { print("mul_OP"); _r_multiply += 1; }
"/"                     { print("div_OP"); _r_divide += 1; }
"%"                     { print("mod_OP"); _r_mod += 1;}
"++"                    { print("inc_OP"); _r_increase += 1; }
"--"                    { print("dec_OP"); _r_decrease += 1; }
"+="                    { print("plus_equal_OP"); _r_plus_equal += 1; }
"-="                    { print("minus_equal_OP"); _r_minus_equal += 1; }
"*="                    { print("mul_equal_OP"); _r_multiply_equal += 1; }
"/="                    { print("div_equal_OP"); _r_divide_equal += 1; }
"%="                    { print("mod_equal_OP"); _r_mod_equal += 1; }
 
  /*relational operators*/
"||"                    { print("or_OP"); _r_or += 1; }
"&&"                    { print("and_OP"); _r_and += 1; }
"!"                     { print("not_OP"); _r_not += 1; }
"=="                    { print("equ_OP"); _r_equal += 1; }
"!="                    { print("nequ_OP"); _r_not_equal += 1; }

    /*logical operators*/
">"                     { print("great_OP"); _r_greater_than += 1; }
"<"                     { print("less_OP"); _r_less_than += 1; }
">="                    { print("greate_OP"); _r_greater_than_equal += 1; }
"<="                    { print("lesse_OP"); _r_less_than_equal += 1; }

    /*brackets*/
"("             { print("lparen"); _r_left_bracket += 1; }
")"             { print("rparen"); _r_right_bracket += 1; }
"["             { print("lbrack"); _r_left_square_bracket += 1; }
"]"             { print("rbrack"); _r_right_square_bracket += 1; }
"{"             { print("lbrace"); _r_left_curly_bracket += 1; }
"}"             { print("rbrace"); _r_right_curly_bracket += 1; }

    /*other symbols*/
";"             { print("semi"); _r_simi_colon += 1; }
","             { print("comma"); _r_comma += 1; }
"="             { print("assign"); _r_assign += 1; }
"."             { print("dot"); _r_dot +=1;}
"&"             { print("quote_or_address"); _r_quote += 1; }
'#'             { print("end");}

{preprocessor_directives} { print("Preprocessor Directives"); }
{ARRAY}         { print("array"); }
{ID}            { print("ID"); }
{INTEGER}        { print("integer"); }
{FCONST}        { print("decimal"); }
{EXPFCONST}    { print("exponential"); }
{CCONST}        { print("CCONST"); }
{STRING}        { print("STRING"); }
 
 
"\n"            { lineno += 1; }
[ \t\r\f]+          /* eat up whitespace */
 
.               { yyerror("Unrecognized character"); }
 
%%
int a;
void print(char *token_type){
    a++;
    printf("【%s\t%s\t%d】\n", yytext, token_type, lineno);
    /*printf("【%-*s",30,yytext);
    printf("%-*s",30,token_type);
    printf("%5d】\n",lineno);*/
}
 
void yyerror(char *message){
    printf("Error: \"%s\" in line %d. content = %s\n", message, lineno, yytext);
    exit(1);
}
 
int main(int argc, char *argv[]){
    yyin = fopen(argv[1], "r");
    printf("【yytext\ttoken\tlineno】\n");
    yylex();
    fclose(yyin);
    printf("Total %d", a);
    return 0;
}
