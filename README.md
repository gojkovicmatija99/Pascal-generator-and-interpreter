# Pascal-interpreter
Interpreter that runs Pascal code and generates C code

## Pascal code

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

## Generated C code
    
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
