files = ["sales.csv", "notes.txt", "customers.csv", "logo.png"]

print(files[0])        # first item (counting starts at 0!)
print(files[-1])       # last item
print(len(files))      # how many items

files.append("orders.csv")   # add to the end
print(files)

for file in files:
     if file.endswith(".csv"):
        print(f"Data file found: {file}")



customer = {
    "name": "Sarah",
    "city": "Birmingham",
    "age": 34,
    "total_spent": 1250.75
}

print(customer["name"])
print(customer.get("email", "No email"))   # safe way - no crash if missing

customer["email"] = "sarah@example.com"    # add a new key

for key, value in customer.items():
    print(f"{key}: {value}")



def clean_name(name):
    """Tidy up a messy name."""          # docstring - explains the function
    return name.strip().title()

def calculate_total(prices):
    total = 0
    for price in prices:
        total = total + price
    return total

print(clean_name("   john smith  "))
print(calculate_total([10.50, 25.00, 4.99]))



 # Day 3 Practice
 #---------------------------------------------


for file in files:
    if file.endswith(".csv"):
        print(file)
print("----------------")

product = {
    "name": "Laptop",
    "price": 750,
    "category": "Electronics"
}
print(f"{product['name']} costs £{product['price']} ({product['category']})")


print("----------------")

def greet(name):
    return f"Hello, {name}!" 

print(greet("jude"))


print("----------------")


def average(numbers):
    if not numbers:  # Check for empty list to avoid division by zero
        return 0
    return sum(numbers) / len(numbers)

print(average([10, 20, 30]))  # Output: 20.0

print("----------------")


def is_adult(age):
    return age >= 18

print(is_adult(20))  # Output: True
print(is_adult(17))  # Output: False



  

for key, value in customer.items():
    if isinstance(value, (int, float)):
        print(f"{key}: {value}")

print("----------------")
 # List of prices [100, 250, 75] — add 10% VAT to each using a loop, print results

prices = [100, 250, 75]
for price in prices:
    total = price * 1.10
    print(f"£{price} + 10% VAT = £{total:.2f}")


print("----------------")
# Write clean_filename(name) that returns the name lowercased with spaces replaced by _. E.g. "My Sales File.CSV" → "my_sales_file.csv"


def clean_filename(name):
    return name.strip().lower().replace(" ", "_")

print(clean_filename("My Sales File.CSV"))  # Output: my_sales_file.csv 