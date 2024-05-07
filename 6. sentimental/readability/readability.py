from cs50 import get_string


def main():
    # Prompt user for input
    text = get_string("Text: ")

    # Count letters, words, and sentences
    letters = sum(1 for char in text if char.isalpha())
    words = len(text.split())
    sentences = text.count(".") + text.count("!") + text.count("?")

    # Calculate L and S
    L = (letters / words) * 100
    S = (sentences / words) * 100

    # Calculate Coleman-Liau index
    index = 0.0588 * L - 0.296 * S - 15.8

    # Round index to nearest integer
    grade = round(index)

    # Print grade level
    if grade < 1:
        print("Before Grade 1")
    elif grade >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {grade}")


if __name__ == "__main__":
    main()
