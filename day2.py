from ast import Store


name = " jude "
age = "40"
salary = " 100000 "
is_learning = True


print (type(name))
print (type(age))
print (type(salary))
print (type(is_learning))


age_next_year = int(age) + 1
monthly_salary = float(salary) / 12


print(f"Next year, I will be {age_next_year} years old and my monthly salary will be £{monthly_salary:.2f}")




row_loaded = 950
if row_loaded == 1000:
    print("perfect, all rows loaded successfully")
elif row_loaded > 0:
    print("partial load, some rows are missing")
else:
    print("no rows loaded, please check the source data")


    # for loop - repeat for each item / a known number of times

for i in range(1,6):
     print(f"Processing file {i} of 5")


     # Loop over text
for letter in "data":
    print(letter)


     # Loop over a list 
for fruit in ["apple", "banana", "cherry"]:
    print(fruit)


     # Loop over a dictionary   
#for key, value in {"name": "John", "age": 30, "city": "New York"}.items():
    #print(f"{key}: {value}")     


    # while loop - repeat until a condition changes
    count = 3
    while count > 0:
        print(f"Processing in {count}---")
        count = count-1
        print("Done")


#Print your name, city, and target job using one f-string     


name = " Jude "
city = " Birmingham "
job = " Data Engineer "


print (f"My name is {name.strip()}, I live in {city.strip()}, and my target job is {job.strip()}.")


 #Store your age. Print how old you'll be in 10 years

age = 40
age_in_10_years = age + 10
print(f"In 10 years, I will be {age_in_10_years} years old.")


 #Ask for a number with num = int(input("Enter a number: ")) — print "Even" or "Odd" (hint: num % 2)

num = int(input("Enter a number: "))
if num % 2 == 0:
    print("Even")       
else:
    print("Odd")

#Grade checker: score 70+ = "Pass", 50–69 = "Retry", below 50 = "Fail"  
#score = int(input("Enter your score: "))
#if score >= 70:
    #print("Pass")
#elif score >= 50:
    #print("Retry")
#else:
    #print(f"Fail advanced, your score is {score}. Please try again.")

#Print numbers 1 to 20, but only the even ones
#for i in range(1, 21):
    if i % 2 == 0:
        print(i)


# Use a loop to calculate 1 + 2 + 3 ... + 100 and print the total
total = 0
for i in range(1, 101):
    total += i
print(f"The total is {total}.") 


#. Print the word "pipeline" one letter per line

for letter in "pipeline":
    print(letter)
print("--------------")

#. FizzBuzz-lite: numbers 1–15, print "Data" if divisible by 3
for i in range(1, 16):
    if i % 3 == 0:
        print("Data")
    else:
        print(i)


    