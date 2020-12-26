#include<stdio.h>
char cifra_stotina(char s)
{
	char cifra_stotina;
	if(s < 100)
	{
		return('0');
	}
	else
	{
		return('0' + s / 100);
	}
	return cifra_stotina;
}
char cifra_desetica(char s)
{
	char cifra_desetica;
	if(s < 10)
	{
		return('0');
	}
	else
	{
		return('0' + s / 10 % 10);
	}
	return cifra_desetica;
}
char cifra_jedinica(char s)
{
	char cifra_jedinica;
	return('0' + s % 10);
	return cifra_jedinica;
}
int main()
{
	char s[100];
	char t[100];
	char ascii;
	char tmp;
	int i;
	int j;
	int len;
	scanf("%s", s);
	i = 1;
	j = 1;
	len = strlen(s);
	while(i <= len)	{
		ascii = s[i - 1];
		i++;
		tmp = cifra_stotina(ascii);
		if(tmp != '0' || tmp == '0' && j > 1)
		{
			t[j - 1] = tmp;
			j++;
		}
		t[j - 1] = cifra_desetica(ascii);
		j++;
		t[j - 1] = cifra_jedinica(ascii);
		j++;
	}
	printf("%s", t);
	return 0;
}
