#include<stdio.h>
int main()
{
	int a[101];
	int b[101];
	int c[101];
	int n;
	int ai;
	int bi;
	int ci;
	int i;
	bi = 1;
	ci = 1;
	scanf("%d", &n);
	for(ai = 1; ai <= n; ai++)
	{
		scanf("%d", &a[ai]);
	}
	for(ai = 1; ai <= n; ai++)
	{
		if(a[ai] % 2 == 0)
		{
			b[bi] = a[ai];
			bi = bi + 1;
		}
		else
		{
			c[ci] = a[ai];
			ci = ci + 1;
		}
	}
	for(i = 1; i <= bi - 1; i++)
	{
		printf("%d ", b[i]);
	}
	printf("\n");
	for(i = 1; i <= ci - 1; i++)
	{
		printf("%d ", c[i]);
	}
	return 0;
}
