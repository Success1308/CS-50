#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

bool is_key_valid(string key);
string encrypt(string plaintext, string key);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: %s key\n", argv[0]);
        return 1;
    }

    if (!is_key_valid(argv[1]))
    {
        printf("Key must contain 26 unique alphabetic characters.\n");
        return 1;
    }

    string plaintext = get_string("plaintext: ");

    string ciphertext = encrypt(plaintext, argv[1]);

    printf("ciphertext: %s\n", ciphertext);

    return 0;
}

bool is_key_valid(string key)
{
    if (strlen(key) != 26)
    {
        return false;
    }

    bool seen[26] = {false};
    for (int i = 0, n = strlen(key); i < n; i++)
    {
        if (!isalpha(key[i]))
        {
            return false;
        }
        int index = tolower(key[i]) - 'a';
        if (seen[index])
        {
            return false;
        }
        seen[index] = true;
    }

    return true;
}

string encrypt(string plaintext, string key)
{
    string ciphertext = plaintext;

    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        if (isalpha(plaintext[i]))
        {
            char base = isupper(plaintext[i]) ? 'A' : 'a';
            int index = tolower(plaintext[i]) - 'a';
            ciphertext[i] = isupper(plaintext[i]) ? toupper(key[index]) : tolower(key[index]);
        }
    }

    return ciphertext;
}
