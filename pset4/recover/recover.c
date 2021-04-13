#include<stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf( "Enter file to open.\n");
        return 1;
    }

    FILE *file = fopen(argv[1],"r");

    if(file == NULL)
    {
        printf("Not a file\n");
    }

    int jpgfound = 0;
    int fcount = 0;
    unsigned char buffer[512];
    FILE *img = NULL;
    char filename[8];

    while(fread(buffer, 512, 1, file) == 1)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if(jpgfound == 1)
            {
                fclose(img);
            }
            else
            {
                jpgfound = 1;
            }

            sprintf(filename,"%03i.jpg", fcount);
            img = fopen(filename,"w");
            fcount++;
        }
        if(jpgfound == 1)
        {
            fwrite(&buffer,512,1,img);
        }
        }
    fclose(file);
    fclose(img);

    return 0;

}