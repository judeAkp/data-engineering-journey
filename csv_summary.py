import csv


# Write a function read_sales(filename) that opens the CSV with csv.DictReader and returns a list of row dictionaries.


def read_sales(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

#Write summarise(rows) that counts rows, adds up amount, and counts rows per category (hint: a dictionary where you do counts[category] = counts.get(category, 0) + 1).
def summarise(rows):
    total_rows = len(rows)
    total_amount = sum(float(row["amount"]) for row in rows)
    counts = {}
    for row in rows:
        category = row["category"]
        counts[category] = counts.get(category, 0) + 1
    return total_rows, total_amount, counts

# Add a main() that calls both, prints the report nicely with f-strings, and wraps the file reading in try/except.
def main():
    try:
        rows = read_sales("sales.csv")
        total_rows, total_amount, counts = summarise(rows)
        print(f"Total rows: {total_rows}")
        print(f"Total amount: £{total_amount:.2f}")
        print("Counts per category:")
        for category, count in counts.items():
            print(f"  {category}: {count}")
    except FileNotFoundError:
        print("Error: The file 'sales.csv' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()