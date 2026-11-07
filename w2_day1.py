import pandas as pd  # pyright: ignore[reportMissingModuleSource]

df = pd.read_csv("sales.csv")

# Print the shape and dtypes of sales.csv — what type is the date column?
print(df.shape)
print(df.dtypes)
print(df["date"].dtype)  # Check the data type of the date column


#Print only the product and amount columns
print(df[["product", "amount"]])



 #Show all rows where category is Furniture (answer: 3 rows)

print(df[df["category"] == "Furniture"])


 #Show rows where amount is over 200 (answer: 3 rows: Laptop 750, Monitor 220, Laptop 820)
print(df[df["amount"] > 200])

#Total of the amount column (answer: 2382.0)
print(df["amount"].sum())

# Average and maximum amount (answer: 238.20 and 820.0)
print(df["amount"].mean())
print(df["amount"].max())

#. Sort by amount, biggest first, and show the top 3
print(df.sort_values("amount", ascending=False).head(3))

# Show rows in Furniture or Stationery (answer: 5 rows)
print(df[df["category"].isin(["Furniture", "Stationery"])])

# Add a price_band column: "High" if amount ≥ 200, else "Low" (hint: df["amount"].apply(lambda x: "High" if x >= 200 else "Low"))
df["price_band"] = df["amount"].apply(lambda x: "High" if x >= 200 else "Low")


# Save only the Electronics rows to electronics.csv
df[df["category"] == "Electronics"].to_csv("electronics.csv", index=False)