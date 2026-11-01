import pandas as pd

df = pd.read_csv("sales.csv")     # df = DataFrame = a table in Python

print(df.head())        # first 5 rows
print(df.shape)         # (rows, columns) - expect (10, 4)
print(df.columns)       # column names
print(df.info())        # column types at a glance

print(df["amount"].sum())                    # total - £2382.0
print(df.groupby("category")["amount"].sum())  # totals per category





#Day 5 Practice

# df.head(3) — print only the first 3 rows
print(df.head(3))

# 2. Print the average (.mean()) and maximum (.max()) of the amount column
print(df["amount"].mean())
print(df["amount"].max())

# Filter: df[df["category"] == "Electronics"] — print it
print(df[df["category"] == "Electronics"])

# Count rows per category: df["category"].value_counts() (Electronics should be 5)
print(df["category"].value_counts())

# Activate/deactivate your venv twice so the commands become automatic the terminal. Then run the following commands in the terminal:
