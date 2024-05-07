from cs50 import get_string

def main():
    # Prompt user for their name
    name = get_string("What is your name? ")

    # Print greeting
    print(f"hello, {name}")

if __name__ == "__main__":
    main()
