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
void check_arm(int x, int cj, int cd, int cs)
{
	int arm;
	if(x < 0)
	{
		return;
	}
	arm = x == cj * cj * cj + cd * cd * cd + cs * cs * cs;
	if(arm)
	{
		printf("DA");
	}
	else
	{
		printf("NE");
	}
}
int main()
{
	int broj;
	int cj;
	int cd;
	int cs;
	scanf("%d", &broj);
	cj = broj % 10;
	cd = broj / 10 % 10;
	cs = broj / 100 % 10;
	check_arm(broj, cj, cd, cs);
	return 0;
}
