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
int jeProst(int n)
{
	int i;
	int jeProst;
	if(n <= 1)
	{
		return(0);
	}
	for(i = n / 2; i >= 2; i--)
	{
		if(n % i == 0)
		{
			return(0);
		}
	}
	return(1);
	return jeProst;
}
int main()
{
	int n;
	int i;
	int s;
	scanf("%d", &n);
	i = 0;
	s = 1;
	do	{
		if(jeProst(s))
		{
			i = i + 1;
			if(i == n)
			{
				break;
			}
		}
		s = s + 1;
	}
	while(!(0));
	printf("%d\n", s);
	return 0;
}
