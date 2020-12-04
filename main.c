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
	string s;
	string t;
	char ascii;
	char tmp;
	int i;
	int j;
	int len;
	scanf("%s", &s);
	i = 1;
	j = 1;
	len = strlen(s);
	while(i <= len)	{
		ascii = s[i];
		i++;
		tmp = cifra_stotina(ascii);
		if(tmp != '0' || tmp == '0' && j > 1)
		{
			insert(tmp, t, j);
			j++;
		}
		insert(cifra_desetica(ascii), t, j);
		j++;
		insert(cifra_jedinica(ascii), t, j);
		j++;
	}
	printf("%s", t);
	return 0;
}
