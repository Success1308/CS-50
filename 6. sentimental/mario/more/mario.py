from cs50 import get_int

def main():
    # Prompt user for height of the half-pyramids
    while True:
        height = get_int("Height: ")
        if 1 <= height <= 8:
            break

    # Generate the half-pyramids
    for i in range(1, height + 1):
        # Print left half-pyramid
        print(" " * (height - i) + "#" * i, end=" ")

        # Print gap
        print(" ", end="")

        # Print right half-pyramid
        print("#" * i)

if __name__ == "__main__":
    main()
