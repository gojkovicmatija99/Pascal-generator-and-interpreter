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
int pow_rek(int a, int b)
{
	int pow_rek;
	if(b == 0)
	{
		return(1);
	}
	return(a * pow_rek(a, b - 1));
	return pow_rek;
}
int main()
{
	int a;
	int b;
	scanf("%d", &a); 
	scanf("%d", &b);
	printf("%d\n", pow_rek(a, b));
	return 0;
}
