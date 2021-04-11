#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    for(int i = 0; i != 26; i++)
    {
        if (isalpha(argv[1][i]))
        {
        }
        else
        {
            printf("Key must only contain alphabetic characters.\n");
            return 1;
        }
    }

    for(int i = 0; i != 26; i++)
    {
        int z = 0;

        for(int s = 0; s != 26; s++)
        {
            if(argv[1][i] == argv[1][s])
            {
                z++;

                if(z == 2)
                {
                    printf("Characters can only be used once.\n");
                    return 1;
                }
            }

        }
    }


    string ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    string abc = "abcdefghijklmnopqrstuvwxyz";

    string ptext = get_string("plaintext: ");

    printf("ciphertext: ");

    for(int n = 0, l = 0; l != strlen(ptext); n++)
    {
        if(ptext[l] == 'a')
        {
            printf("%c", tolower(argv[1][0]));
            l++;
            n = 0;
        }
        if(ptext[l] == 'A')
        {
            printf("%c", toupper(argv[1][0]));
            l++;
            n = 0;
        }
        if(ptext[l] == ABC[n])
        {
            printf("%c", toupper(argv[1][n]));
            l++;
            n = 0;
        }
        if(ptext[l] == abc[n])
        {
            printf("%c", tolower(argv[1][n]));
            l++;

            n = 0;
        }
        if(ptext[l] >= '0' && ptext[l] <= '9')
        {
            printf("%c", ptext[l]);
            l++;
            n = 0;
        }
        if(ptext[l] == ' ')
        {
            printf("%c", ptext[l]);
            l++;
            n = 0;
        }
    }
    printf("\n");
    return 0;
}