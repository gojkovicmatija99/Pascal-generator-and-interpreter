#include<stdio.h>
void insert(char tmp, char* a, int p)
{
    int i=0;
	int t=0;
	int x,g,s,o;
	char c[100], b[100];
	b[0]=tmp;
	b[1]=' ';
	int	r = strlen(a);
	int n = strlen(b);
   	while(i <= r)
	{
		c[i]=a[i];
		i++;
	}
	s = n+r;
	o = p+n;
	for(i=p;i<s;i++)
	{
		x = c[i];
		if(t<n)
		{
			a[i] = b[t];
			t=t+1;
		}
		a[o]=x;
		o=o+1;
	}
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
