#ifndef DICTIONARY_H
#define DICTIONARY_H

#include <stdbool.h>

#define LENGTH 45

#define HASH_SIZE 2000

typedef struct node
{
    char* word;
    struct node* next;
}
node;


bool check(const char* word);

bool load(const char* dictionary);


unsigned int size(void);

bool unload(void);

#endif
