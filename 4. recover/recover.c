#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Could not open %s\n", argv[1]);
        return 1;
    }

    // Create a buffer for a block of data
    uint8_t buffer[512];

    // Counter for JPEG file names
    int jpeg_count = 0;

    // Output file pointer
    FILE *jpeg = NULL;

    // Read data from the memory card
    while (fread(buffer, 1, 512, card) == 512)
    {
        // Check for JPEG signature
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // If a JPEG file is already open, close it
            if (jpeg != NULL)
            {
                fclose(jpeg);
            }

            // Create a new JPEG file
            char filename[8];
            sprintf(filename, "%03i.jpg", jpeg_count++);
            jpeg = fopen(filename, "w");
            if (jpeg == NULL)
            {
                fprintf(stderr, "Could not create %s\n", filename);
                fclose(card);
                return 2;
            }

            // Write the current block to the JPEG file
            fwrite(buffer, 1, 512, jpeg);
        }
        else
        {
            // Continue writing to the current JPEG file
            if (jpeg != NULL)
            {
                fwrite(buffer, 1, 512, jpeg);
            }
        }
    }

    // Close any opened files
    fclose(card);
    if (jpeg != NULL)
    {
        fclose(jpeg);
    }

    return 0;
}
