#include <stdio.h>
#include <cs50.h>

int calculate_coins(int value, int coin_value);





int main(void)
{
    int cents;
    do
    {
        cents = get_int("Change owed: ");
    }
    while (cents < 0);

    int quarters = calculate_coins(cents, 25);
    cents -= quarters * 25;

    int dimes = calculate_coins(cents, 10);
    cents -= dimes * 10;

    int nickels = calculate_coins(cents, 5);
    cents -= nickels * 5;

    int pennies = cents;

    int total_coins = quarters + dimes + nickels + pennies;
    printf("%d\n", total_coins);

}

int calculate_coins(int value, int coin_value)
{
    int count = 0;
    while (value >= coin_value)
    {
        count++;
        value -= coin_value;
    }
    return count;
}
