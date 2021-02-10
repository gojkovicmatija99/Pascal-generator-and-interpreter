# Pascal-generator-and-interpreter
Compiler writen in Python that uses Pascal code, generates C code and interprets it. It is divided into few modules:
- Lexer
- Parser
- Grapher
- Symbolizer
- Generator
- Interpreter

## My Pascal grammer

     program  =>                        (  procedure_declaration  |  function_declaration )*  variable_declaration_part ?   begin_block_end  '.'

     procedure_declaration  =>          'procedure'  func_proc_header  ';'  func_proc_implementation
     function_declaration  =>           'function'   func_proc_header  ':'  type  ';'  func_proc_implementation

     func_proc_header  =>               identifier  '(' (  variable_declaration  ';' )* ')'
     func_proc_implementation =>        variable_declaration_part ?  begin_block_end  ';'
     variable_declaration_part =>       'var' ( variable declaration  ';' )*
     variable_declaration  =>           identifier  ( ','  identifier  )* ':' (  type  |  array_type  )
     begin_block_end  =>                'begin'  block  'end'
     block  =>                          ( if_statement  |  while_statement  |  for_statement  |  repeat_statement  | 'break'' | 'continue' | 'exit' |  expression  |   func_proc_call  )*

     func_proc_call  =>                 identifier  '('  arguments  ')'
     arguments  =>                      ( expression  )? ( ','  expression  )*
     exit =>                            'exit' + ( '(' expressions ')' )?

     for_statement  =>                  'for'  expression  'to'  expression  'do'  begin_block_end  ';'
     if_statement  =>                   'if'   logic_expression  'then'  begin_block_end  ( ';' | ( 'else'  begin_block_end  ';') )
     while_statement  =>                'while'  logic_expression  'do'  begin_block_end  ';'
     repeat_statement  =>               'repeat'  block  'until'  logic_expression  ';'

     logic_expression =>                logic_term  ( ( 'or' )  logic_term )*
     logic_term =>                      compare ( ( 'and' | 'xor' ) compare )*
     compare  =>                        expression  ( '==' | '!=' | '<' | '>' | '<=' | '>=' | '<>' )  expression

     expression  =>                     term  ( ( '+' | '-' )  term  )*
     term  =>                           fact  ( ( '*' | 'div' | 'mod' )  fact  )*
     fact  =>                           ( '-' | 'not')? (  constant  |  identifier  |  array_element  |  func_proc_call  | '('  expression  ')' )
     assign =>                          identifier '=' ( expressions | login_expression ) ';'

     type  =>                           simple_type   |  string
     simple_type  =>                    'integer' | 'char' | 'real' | 'boolean'
     string_type  =>                    'string' ( '['  integer_constant  ']' )?
     array_type  =>                     'array' '['  integer_constant  '.' '.'  integer_constant  ']' 'of'  simple_type   array_element_declaration ?
     array_element_declaration  =>      '=' '('  constant  ( ','  constant  )* ')
     array_element  =>                  identifier  ( '['  expression  ']' )+

     identifier  =>                     letter  (  letter  |  digit  )*
     constant  =>                       integer_constant  |  char_constant  |  real_constant  |  boolean_constant  |  string_constant
     integer_constant  =>               digit   digit *
     char_constant  =>                  letter
     real_constant  =>                  integer_constant  .  integer_constant
     boolean_constant  =>               'true' | 'false'
     string_constant  =>                ''' (  letter  |  digit  )* '''

## Example

### Input

    var
        niz : array[1..100] of integer;
        i, j, n, temp: integer;

    begin
        readln(n);

        for i := 1 to n do
        begin
            read(niz[i]);
        end;

        for i := 1 to n do
        begin
            for j := i + 1 to n do
            begin
                if niz[i] <= niz[j] then
                begin
                    continue;
                end
                else
                begin
                    temp := niz[i];
                    niz[i] := niz[j];
                    niz[j] := temp;
                end;
            end;
        end;

        for i := 1 to n do
        begin
            write(niz[i], ' ');
        end;
    end.
    
### Grapher

![alt text](https://github.com/gojkovicmatija99/Pascal-generator-and-interpreter/blob/master/graph.png)

### Generator
    
    #include<stdio.h>
    int main()
    {
        int niz[100];
        int i;
        int j;
        int n;
        int temp;
        scanf("%d", &n);
        for(i = 1; i <= n; i++)
        {
            scanf("%d", &niz[i]);
        }
        for(i = 1; i <= n; i++)
        {
            for(j = i + 1; j <= n; j++)
            {
                if(niz[i] <= niz[j])
                {
                    continue;
                }
                else
                {
                    temp = niz[i];
                    niz[i] = niz[j];
                    niz[j] = temp;
                }
            }
        }
        for(i = 1; i <= n; i++)
        {
            printf("%d ", niz[i]);
        }
        return 0;
    }
    
## Interpreter

     5
     34
     12
     54
     90
     232
     12 34 54 90 232 
    
## Future additions

- Support for recursion calls and recursive stacks
