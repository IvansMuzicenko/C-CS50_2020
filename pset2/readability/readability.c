#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int main(void)
{
    float letters = 0;
    float words = 1;
    float sentences = 0;

    string text = get_string("Text: ");

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] >= 'a' && text[i] <= 'z')
        {
            letters++;
        }
        if (text[i] >= 'A' && text[i] <= 'Z')
        {
            letters++;
        }
        if (text[i] == ' ')
        {
            words++;
        }
        if (text[i] == '.')
        {
            sentences++;
        }
        if (text[i] == '!')
        {
            sentences++;
        }
        if (text[i] == '?')
        {
            sentences++;
        }
    }

    float avgl = (letters / words) * 100;
    float avgs = (sentences / words) * 100;
    float grade = 0.0588 * avgl - 0.296 * avgs - 15.8;

    if (grade < 1 )
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", (int) round(grade));
    }
}