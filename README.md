 program  =>                        (  procedure_declaration  |  function_declaration )*  variable_declaration_part ?   begin_block_end  '.'

 procedure_declaration  =>  		'procedure'  func_proc_header  ';'  func_proc_implementation
 function_declaration  => 			'function'   func_proc_header  ':'  type  ';'  func_proc_implementation

 func_proc_header  =>               identifier  '(' (  variable_declaration  ';' )* ')'
 func_proc_implementation => 	    variable_declaration_part ?  begin_block_end  ';'
 variable_declaration_part =>       'var' ( variable declaration  ';' )*
 variable_declaration  =>  			identifier  ( ','  identifier  )* ':' (  type  |  array_type  )
 begin_block_end  => 				'begin'  block  'end'
 block  => 							( if_statement  |  while_statement  |  for_statement  |  repeat_statement  | 'break'' | 'continue' | 'exit' |  expression  |   func_proc_call  )*

 func_proc_call  => 				identifier  '('  arguments  ')'
 arguments  => 						( expression  )? ( ','  expression  )*

 for_statement  =>  				'for'  expression  'to'  expression  'do'  begin_block_end  ';'
 if_statement  => 					'if'   logic_expression  'then'  begin_block_end  ( ';' | ( 'else'  begin_block_end  ';') )
 while_statement  => 		        'while'  logic_expression  'do'  begin_block_end  ';'
 repeat_statement  => 		        'repeat'  block  'until'  logic_expression  ';'

 logic_expression => 				compare  ( ( 'and' | 'or' | 'xor' )  compare  )?
 compare  => 						expression  ( '==' | '!=' | '<' | '>' | '<=' | '>=' | '<>' )  expression

 expression  =>  					term  ( ( '+' | '-' )  term  )*
 term  =>  							fact  ( ( '*' | 'div' | 'mod' )  fact  )*
 fact  =>  							( '-' | 'not')? (  constant  |  identifier  |  array_element  |  func_proc_call  | '('  expression  ')' )

 type  =>                           simple_type   |  string
 simple_type  =>                    'integer' | 'char' | 'real' | 'boolean'
 string_type  =>                    'string' ( '['  integer_constant  ']' )?
 array_type  => 					'array' '['  integer_constant  '.' '.'  integer_constant  ']' 'of'  simple_type   array_element_declaration ?
 array_element_declaration  => 		'=' '('  constant  ( ','  constant  )* ')
 array_element  =>  				identifier  ( '['  expression  ']' )+

 identifier  => 					letter  (  letter  |  digit  )*
 constant  =>                       integer_constant  |  char_constant  |  real_constant  |  boolean_constant  |  string_constant
 integer_constant  => 				digit   digit *
 char_constant  =>                  letter
 real_constant  =>                  integer_constant  .  integer_constant
 boolean_constant  =>               'true' | 'false'
 string_constant  =>                ''' (  letter  |  digit  )* '''

