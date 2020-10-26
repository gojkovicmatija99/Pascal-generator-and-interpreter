var
a, b: boolean;

begin
   a := true;
   b := false;

   if (a and b) then 
    begin
      writeln('Line 1 - Condition is true' );
    end
    else
    begin
      writeln('Line 1 - Condition is not true'); 
    end;
    if  (a or b) then
    begin
      writeln('Line 2 - Condition is true' );  
        a := false;
        b := true;
    end;
    if  (a and b) then
    begin
        writeln('Line 3 - Condition is true' );
    end
    else
    begin
        writeln('Line 3 - Condition is not true' );
    end; 
    if not (a and b) then
    begin
        writeln('Line 4 - Condition is true' );
    end;
end.