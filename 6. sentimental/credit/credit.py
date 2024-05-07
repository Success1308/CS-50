from cs50 import get_string

def main():
    # Prompt user for input
    card_number = get_string("Number: ")

    # Validate input
    if not card_number.isdigit() or not (13 <= len(card_number) <= 16):
        print("INVALID")
        return

    # Check if the card number is valid using Luhn's algorithm
    if not luhn_check(card_number):
        print("INVALID")
        return

    # Determine card type
    card_type = get_card_type(card_number)

    # Print result
    print(card_type)

def luhn_check(card_number):
    # Reverse the card number
    card_number = card_number[::-1]

    # Initialize variables
    total = 0

    # Iterate over every other digit, starting with the second-to-last digit
    for i in range(1, len(card_number), 2):
        digit = int(card_number[i])
        # Double the digit and add the digits of the product
        total += digit * 2 % 10 + digit * 2 // 10

    # Add the sum of the digits that were not doubled
    total += sum(int(card_number[i]) for i in range(0, len(card_number), 2))

    # Check if the total modulo 10 is zero
    return total % 10 == 0

def get_card_type(card_number):
    # Determine card type based on the starting digits and length
    if card_number[:2] in ["34", "37"] and len(card_number) == 15:
        return "AMEX"
    elif card_number[:2] in [str(i) for i in range(51, 56)] and len(card_number) == 16:
        return "MASTERCARD"
    elif card_number[0] == "4" and (len(card_number) == 13 or len(card_number) == 16):
        return "VISA"
    else:
        return "INVALID"

if __name__ == "__main__":
    main()
