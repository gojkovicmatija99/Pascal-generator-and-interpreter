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
	char c;
	int lo;
	int hi;
	int d;
	scanf("%c", &c);
	lo = c >= 'A';
	hi = c <= 'Z';
	if(lo && hi)
	{
		d = c + 32;
	}
	else
	{
		d = c - 32;
	}
	printf("%c", d);
	return 0;
}
