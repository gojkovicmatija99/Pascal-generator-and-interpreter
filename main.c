#include<stdio.h>
void insert(char a, char *b, int position)
{
   char tmp[100];
   strncpy(tmp, b, position);
   tmp[position] = a;
   tmp[position+1]=' ';
   strcat(tmp, b+position);
   puts(tmp);
   b = tmp;
}
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
