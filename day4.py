with open("names.txt", "r") as file:
    for line in file:
        clean_line = line.strip()      # remove hidden \n newline
        print(f"Hello, {clean_line}!")




import csv

total = 0

with open("sales.csv", "r") as file:
    reader = csv.DictReader(file)     # each row becomes a dictionary!
    for row in reader:
        print(row)
        total = total + float(row["amount"])

print(f"Total sales: £{total:.2f}")   # Expected: £2382.00




try:
    with open("missing_file.csv", "r") as file:
        print(file.read())
except FileNotFoundError:
    print("❌ File not found - check the filename and folder")

print("Program kept running ✅")
print("----------------")



# Count how many lines are in names.txt and print the count
with open("names.txt", "r") as file:
    line_count = sum(1 for line in file)
print(f"Number of lines in names.txt: {line_count}")
print("----------------")


# Write names longer than 4 letters into a new file long_names.txt (mode "w")
with open("names.txt", "r") as file:
    with open("long_names.txt", "w") as output_file:
        for line in file:
            clean_line = line.strip()
            if len(clean_line) > 4:
                output_file.write(f"{clean_line}\n")
print("Long names written to long_names.txt")
print("----------------")


 #Using sales.csv: print only rows where category is Electronics
with open("sales.csv", "r") as file:
    reader = csv.DictReader(file)
    print("Electronics sales:")
    for row in reader:
        if row["category"] == "Electronics":
            print(row)
print("----------------")

#Count how many rows are in sales.csv (answer: 10 data rows)
with open("sales.csv", "r") as file:
    reader = csv.DictReader(file)
    row_count = sum(1 for row in reader)
print(f"Number of rows in sales.csv: {row_count}")
print("----------------")


# Wrap your Q3 code in try/except so a wrong filename prints a friendly error
try:
    with open("missing_file.csv", "r") as file:
        print(file.read())
except FileNotFoundError:
    print("❌ File not found - check the filename and folder")

print("Program kept running ✅")



  #Calculate total sales for Furniture only (answer: £495.00)
total_furniture_sales = 0
with open("sales.csv", "r") as file:
      reader = csv.DictReader(file)
      for row in reader:
          if row["category"] == "Furniture":
              total_furniture_sales += float(row["amount"])
print(f"Total sales for Furniture: £{total_furniture_sales:.2f}")


