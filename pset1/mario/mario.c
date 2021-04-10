#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1 || n > 8);
    for (int i = 0; i < n; i++)
    {
        for (int s = n - 1; s > i; s--)
        {
             printf(" ");
        }
        for (int l = -1; l < i; l++)
        {
            printf("#");
        }
        printf("  ");
        for (int l = -1; l < i; l++)
        {
            printf("#");
        }
        printf("\n");
    }
}