#include <cs50.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>

int count_digits(long long n);
bool is_valid_length(int count);
bool luhn_algorithm(long long card_number);
void print_card_type(long long card_number);

int main(void)
{
    long long card_number;
    do
    {
        card_number = get_long_long("Number: ");
    }
    while (card_number <= 0);

    if (luhn_algorithm(card_number))
    {
        print_card_type(card_number);
    }
    else
    {
        printf("INVALID\n");
    }

    return 0;
}

int count_digits(long long n)
{
    int count = 0;
    while (n != 0)
    {
        n /= 10;
        count++;
    }
    return count;
}

bool is_valid_length(int count)
{
    return (count == 13 || count == 15 || count == 16);
}

bool luhn_algorithm(long long card_number)
{
    int sum = 0;
    bool multiply = false;
    while (card_number > 0)
    {
        int digit = card_number % 10;
        if (multiply)
        {
            digit *= 2;
            while (digit > 0)
            {
                sum += digit % 10;
                digit /= 10;
            }
        }
        else
        {
            sum += digit;
        }
        card_number /= 10;
        multiply = !multiply;
    }
    return (sum % 10 == 0);
}
void print_card_type(long long card_number)
{
    int count = count_digits(card_number);
    if (is_valid_length(count))
    {
        int first_two_digits = card_number / (long long) (pow(10, count - 2));
        if ((count == 15 && (first_two_digits == 34 || first_two_digits == 37)))
        {
            printf("AMEX\n");
        }
        else if (count == 16 && (first_two_digits >= 51 && first_two_digits <= 55))
        {
            printf("MASTERCARD\n");
        }
        else if ((count == 13 || count == 16) && (first_two_digits / 10 == 4))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}
