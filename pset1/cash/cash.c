#include <cs50.h>
#include <math.h>
#include <stdio.h>

int main(void)
{
    float dollars;

    do
    {
        dollars = get_float("Change owed: $");
    }
    while(dollars < 0);

    int cents = round(dollars * 100);
    int coins = 0;

    int c1 = cents/25;
    int c11 = cents%25;

    int c2 = c11/10;
    int c22 = c11%10;

    int c3 = c22/5;
    int c33 = c22%5;

    int c4 = c33/1;


    coins = c1 + c2 + c3 + c4;
    printf("%i\n", coins);
}