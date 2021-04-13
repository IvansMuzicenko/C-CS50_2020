#include "helpers.h"
#include "math.h"
#include "string.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int red = image[i][j].rgbtRed;
            int green = image[i][j].rgbtGreen;
            int blue = image[i][j].rgbtBlue;

            int average = round((red + green + blue) / 3.0);

            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{

    RGBTRIPLE temp;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            temp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = temp;
        }
    }
}
// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    memcpy(temp, image, sizeof(RGBTRIPLE) * height * width);

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float average = 0.0;
            int red = 0;
            int green = 0;
            int blue = 0;
            for (int k = -1; k <= 1; k++)
            {
                for (int l = -1; l <= 1; l++)
                {
                    if (i + k != height && i + k != -1 && j + l != width && j + l != -1)
                    {
                        red += temp[i + k][j + l].rgbtRed;
                        green += temp[i + k][j + l].rgbtGreen;
                        blue += temp[i + k][j + l].rgbtBlue;
                        average++;
                    }
                }
            }
            image[i][j].rgbtRed = round(red / average);
            image[i][j].rgbtGreen = round(green / average);
            image[i][j].rgbtBlue = round(blue / average);
        }
    }
}

// Detect edges
int min (int x, int y);

void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp [height + 2][width + 2];

    for (int i = 0; i < height + 1; i++)
    {
        temp[i][0].rgbtBlue = 0;
        temp[i][0].rgbtGreen = 0;
        temp[i][0].rgbtRed = 0;

        temp[i][width + 1].rgbtBlue = 0;
        temp[i][width + 1].rgbtGreen = 0;
        temp[i][width + 1].rgbtRed = 0;


        for (int j = 0; j < width + 1; j++)
        {
            temp[i + 1][j + 1] = image[i][j];
        }
    }
    for (int i = 0; i < width +1; i++)
    {
        temp[0][i].rgbtBlue = 0;
        temp[0][i].rgbtGreen = 0;
        temp[0][i].rgbtRed = 0;

        temp[height + 1][i].rgbtBlue = 0;
        temp[height + 1][i].rgbtGreen = 0;
        temp[height + 1][i].rgbtRed = 0;
    }

    RGBTRIPLE temp2[height + 2][width + 2];

    for (int i = 0; i < height + 2; i++)
    {
        for (int j = 0; j < width + 2; j++)
        {
            temp2[i][j] = temp[i][j];
        }
    }


    for (int i = 1; i < height + 1; i++)
    {
        for(int j = 1; j < width + 1; j++)
        {
        int numRx = (temp2[i - 1][j - 1].rgbtRed * -1) + (temp2[i - 1][j + 1].rgbtRed * 1) + (temp2[i][j - 1].rgbtRed * -2) + (temp2[i][j + 1].rgbtRed * 2) + (temp2[i + 1][j - 1].rgbtRed * -1) + (temp2[i + 1][j + 1].rgbtRed * 1);
        int numRy = (temp2[i - 1][j - 1].rgbtRed * -1) + (temp2[i - 1][j].rgbtRed * - 2) + (temp2[i - 1][j + 1].rgbtRed * - 1) + (temp2[i + 1][j - 1].rgbtRed * 1) + (temp2[i + 1][j].rgbtRed * 2) +  (temp2[i + 1][j + 1].rgbtRed * 1);
        int numR = round(sqrt(pow(numRx, 2) + pow(numRy, 2)));
        temp[i][j].rgbtRed = min(numR, 255);
        image[i - 1][j - 1].rgbtRed = temp[i][j].rgbtRed;
        int numBx = (temp2[i - 1][j - 1].rgbtBlue * -1) + (temp2[i - 1][j + 1].rgbtBlue * 1) + (temp2[i][j - 1].rgbtBlue * -2) + (temp2[i][j + 1].rgbtBlue * 2) + (temp2[i + 1][j - 1].rgbtBlue * -1) + (temp2[i + 1][j + 1].rgbtBlue * 1);
        int numBy = (temp2[i - 1][j - 1].rgbtBlue * -1) + (temp2[i - 1][j].rgbtBlue * - 2) + (temp2[i - 1][j + 1].rgbtBlue * - 1) + (temp2[i + 1][j - 1].rgbtBlue * 1) + (temp2[i + 1][j].rgbtBlue * 2) +  (temp2[i + 1][j + 1].rgbtBlue * 1);
        int numB = round(sqrt(pow(numBx, 2) + pow(numBy, 2)));
        temp[i][j].rgbtBlue = min(numB, 255);
        image[i - 1][j - 1].rgbtBlue = temp[i][j].rgbtBlue;

        int numGx = (temp2[i - 1][j - 1].rgbtGreen * -1) + (temp2[i - 1][j + 1].rgbtGreen * 1) + (temp2[i][j - 1].rgbtGreen * -2) + (temp2[i][j + 1].rgbtGreen * 2) + (temp2[i + 1][j - 1].rgbtGreen * -1) + (temp2[i + 1][j + 1].rgbtGreen * 1);
        int numGy = (temp2[i - 1][j - 1].rgbtGreen * -1) + (temp2[i - 1][j].rgbtGreen * - 2) + (temp2[i - 1][j + 1].rgbtGreen * - 1) + (temp2[i + 1][j - 1].rgbtGreen * 1) + (temp2[i + 1][j].rgbtGreen * 2) +  (temp2[i + 1][j + 1].rgbtGreen * 1);
        int numG = round(sqrt(pow(numGx, 2) + pow(numGy, 2)));
        temp[i][j].rgbtGreen = min(numG, 255);
        image[i - 1][j - 1].rgbtGreen = temp[i][j].rgbtGreen;

        }
    }

    return;
}

int min (int x, int y)
{
    if (x > y)
    {
        return y;
    }
    else
    {
        return x;
    }
}