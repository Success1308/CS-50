#include "dictionary.h"
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

node *hashTable[HASH_SIZE];
unsigned int dictionary_size = 0;

unsigned long hash(char *str);

bool check(const char *word)
{
    int n = strlen(word);
    char currentWord[n + 1];

    for (int i = 0; i < n; i++)
        currentWord[i] = tolower(word[i]);

    currentWord[strlen(word)] = '\0';

    int tableIndex = hash(currentWord);

    node *ptrNode = hashTable[tableIndex];

    while (ptrNode != NULL)
    {
        if (strcmp(ptrNode->word, currentWord) == 0)
            return true;

        ptrNode = ptrNode->next;
    }

    return false;
}

bool load(const char *dictionary)
{
    char currentWord[LENGTH + 1];
    int tableIndex;

    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
        return false;

    while (fscanf(dict, "%s", currentWord) == 1)
    {
        tableIndex = hash(currentWord);

        node *newNode = malloc(sizeof(node));
        if (newNode == NULL)
        {
            printf("Error: Out of memory\n");
            return false;
        }
        newNode->word = malloc((strlen(currentWord) + 1) * sizeof(char));
        if (newNode->word == NULL)
        {
            printf("Error: Out of memory\n");
            return false;
        }

        strcpy(newNode->word, currentWord);
        newNode->next = NULL;

        if (hashTable[tableIndex] == NULL)
            hashTable[tableIndex] = newNode;

        else
        {
            node *ptrNode = hashTable[tableIndex];

            while (ptrNode->next != NULL)
                ptrNode = ptrNode->next;

            ptrNode->next = newNode;
        }

        dictionary_size++;
    }
    fclose(dict);
    return true;
}

unsigned int size(void)
{
    return dictionary_size;
}

bool unload(void)
{
    // Iterate through hash table
    for (int i = 0; i < HASH_SIZE; i++)
    {
        node *cursor = hashTable[i];

        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;

            free(temp->word);
            free(temp);
        }
    }
    return true;
}

unsigned long hash(char *str)
{
    unsigned long hash = 5381;
    int c;
    while ((c = *str++) != 0)
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
    return hash % HASH_SIZE;
}
