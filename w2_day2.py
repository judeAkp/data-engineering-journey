import pandas as pd

df = pd.read_csv("messy_customers.csv")

print(df.shape)              # (11, 7)
print(df.dtypes)             # note: customer_id and age are floats, spend is text
print(df.isna().sum())       # how many missing per column
print(df.duplicated().sum()) # how many exact duplicate rows

print("------------ ")

df = df.dropna(how="all")     # removes the empty comma-only row  -> 10 rows
df = df.drop_duplicates()     # removes the two copies of TOM BAKER -> 8 rows
print(df.shape)

print("------------ ")

df["name"] = df["name"].str.strip().str.title()
df["name"] = df["name"].str.replace(r"\s+", " ", regex=True)   # collapse double spaces

df["city"] = df["city"].str.strip().str.title()
df["city"] = df["city"].replace({"Bham": "Birmingham"})

print(df["name"].unique())
print(df["city"].value_counts())

print("------------ ")

df["spend"] = (df["spend"]
               .str.replace("£", "", regex=False)
               .str.replace(",", "", regex=False))
df["spend"] = pd.to_numeric(df["spend"], errors="coerce")

print(df["spend"].sum())    # 4316.5
print(df["spend"].dtype)    # float64

print("------------ ")

df["signup_date"] = pd.to_datetime(df["signup_date"], format="mixed", dayfirst=True)
print(df["signup_date"].dtype)      # datetime64[ns]
print(df["signup_date"].dt.month)   # .dt unlocks day/month/year
print(df["signup_date"].min(), df["signup_date"].max())

print("------------ ")

df["customer_id"] = df["customer_id"].astype(int)

print(df.dtypes)
print(df.isna().sum())
print(df.shape)                 # (8, 7)

df.to_csv("customers_clean.csv", index=False)
print("Saved customers_clean.csv")


#ow many rows and columns before cleaning? (11, 7)
print(df.shape)              # (11, 7)


#How many values are missing in age? (5)
print(df["age"].isna().sum())

#. After dropping the empty row and duplicates, how many rows are left? (8)
print(df.dropna(how="all").drop_duplicates().shape)     # removes the empty comma-only row  -> 10 rows

# What is the total spend after converting to numbers? (£4316.50)
print(df["spend"].str.replace("£", "", regex=False).str.replace(",", "", regex=False).astype(float).sum())    # 4316.5


#What is the average age? (36.83 — and explain why only 6 rows count)
print(int(df["age"].mean()))  # 36.833333333333336

# Count how many customers are in each city after standardising (Birmingham 5, others 1 each)
print(df["city"].value_counts())

#Fill the missing email with "unknown" using .fillna(). Should you fill the missing ages with the average? Write down why or why not — don't guess silently.
df["email"] = df["email"].fillna("unknown")
# Should you fill the missing ages with the average? Write down why or why not — don't guess silently.
# No, because filling missing ages with the average might not be representative of the actual age distribution.

#Create a spend_band column: "High" ≥ 1000, "Medium" 100–999, "Low" < 100
df["spend_band"] = df["spend"].str.replace("£", "", regex=False).str.replace(",", "", regex=False).astype(float).apply(lambda x: "High" if x >= 1000 else "Medium" if x >= 100 else "Low")

#Save the cleaned file and open it in VS Code to confirm it looks right
df.to_csv("customers_clean.csv", index=False)
