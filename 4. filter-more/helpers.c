#include "helpers.h"
#include <stdio.h>
#include <math.h>
#include <string.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int avg = (image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3;
            image[i][j].rgbtRed = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtBlue = avg;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = temp;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    memcpy(temp, image, sizeof(RGBTRIPLE) * height * width); // Create a copy of the original image

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sumRed = 0, sumGreen = 0, sumBlue = 0;
            int count = 0;

            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    int newi = i + di;
                    int newj = j + dj;

                    if (newi >= 0 && newi < height && newj >= 0 && newj < width)
                    {
                        sumRed += temp[newi][newj].rgbtRed;
                        sumGreen += temp[newi][newj].rgbtGreen;
                        sumBlue += temp[newi][newj].rgbtBlue;
                        count++;
                    }
                }
            }

            image[i][j].rgbtRed = round((float)sumRed / count);
            image[i][j].rgbtGreen = round((float)sumGreen / count);
            image[i][j].rgbtBlue = round((float)sumBlue / count);
        }
    }
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    memcpy(temp, image, sizeof(RGBTRIPLE) * height * width); // Create a copy of the original image

    int gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int Gx_red = 0, Gx_green = 0, Gx_blue = 0;
            int Gy_red = 0, Gy_green = 0, Gy_blue = 0;

            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    int newi = i + di;
                    int newj = j + dj;

                    if (newi >= 0 && newi < height && newj >= 0 && newj < width)
                    {
                        int k = di + 1;
                        int l = dj + 1;

                        Gx_red += gx[k][l] * temp[newi][newj].rgbtRed;
                        Gx_green += gx[k][l] * temp[newi][newj].rgbtGreen;
                        Gx_blue += gx[k][l] * temp[newi][newj].rgbtBlue;

                        Gy_red += gy[k][l] * temp[newi][newj].rgbtRed;
                        Gy_green += gy[k][l] * temp[newi][newj].rgbtGreen;
                        Gy_blue += gy[k][l] * temp[newi][newj].rgbtBlue;
                    }
                }
            }

            int final_red = round(sqrt(Gx_red * Gx_red + Gy_red * Gy_red));
            int final_green = round(sqrt(Gx_green * Gx_green + Gy_green * Gy_green));
            int final_blue = round(sqrt(Gx_blue * Gx_blue + Gy_blue * Gy_blue));

            final_red = final_red > 255 ? 255 : final_red;
            final_green = final_green > 255 ? 255 : final_green;
            final_blue = final_blue > 255 ? 255 : final_blue;

            image[i][j].rgbtRed = final_red;
            image[i][j].rgbtGreen = final_green;
            image[i][j].rgbtBlue = final_blue;
        }
    }
}
