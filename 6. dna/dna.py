import csv
import sys


def main():
    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py database.csv sequence.txt")
        sys.exit(1)

    # Read database file into a variable
    database_file = sys.argv[1]
    database = read_database(database_file)

    # Read DNA sequence file into a variable
    sequence_file = sys.argv[2]
    with open(sequence_file, "r") as file:
        sequence = file.read().strip()

    # Find longest match of each STR in DNA sequence
    longest_matches = {}
    for key in database[0].keys():
        if key != "name":
            longest_matches[key] = longest_match(sequence, key)

    # Check database for matching profiles
    matching_profile = None
    for row in database:
        if all(row[key] == str(longest_matches[key]) for key in longest_matches.keys()):
            matching_profile = row["name"]
            break

    if matching_profile:
        print(matching_profile)
    else:
        print("No match")


def read_database(database_file):
    """Reads a CSV database file and returns its contents as a list of dictionaries."""
    database = []
    with open(database_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            database.append(row)
    return database


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    for i in range(sequence_length):
        count = 0
        while True:
            start = i + count * subsequence_length
            end = start + subsequence_length
            if sequence[start:end] == subsequence:
                count += 1
            else:
                break
        longest_run = max(longest_run, count)

    return longest_run


if __name__ == "__main__":
    main()
