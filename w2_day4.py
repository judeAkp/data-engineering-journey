import pandas as pd

o = pd.read_csv("orders.csv")
c = pd.read_csv("customers.csv")

o["revenue"] = o["quantity"] * o["unit_price"]

inner = o.merge(c, on="customer_id", how="inner")
left  = o.merge(c, on="customer_id", how="left", indicator=True)

print(o.shape, inner.shape, left.shape)     # (18, 8) (17, 10) (18, 10)
print(left["_merge"].value_counts())
print(left[left["_merge"] == "left_only"])  # the orphan order


merged = o.merge(c, on="customer_id", how="inner")

print(merged.groupby("city")["revenue"].sum().round(2).sort_values(ascending=False))
print(merged.groupby("customer_name")["revenue"].sum().round(2).sort_values(ascending=False).head(3))

# Which customers never ordered? join the other way round
cust_orders = c.merge(o, on="customer_id", how="left")
print(cust_orders[cust_orders["order_id"].isna()]["customer_name"])   # Nina Kaur


sept = o[o["order_date"].str.startswith("2026-09")]
oct_ = o[o["order_date"].str.startswith("2026-10")]

all_orders = pd.concat([sept, oct_], ignore_index=True)
print(all_orders.shape)     # (18, 8) - back to the full set

# A second use: add a "source" flag when combining files from different systems
sept = sept.assign(source="september_file")
oct_ = oct_.assign(source="october_file")
print(pd.concat([sept, oct_], ignore_index=True)["source"].value_counts())



# Day 4 Practice
# ⭐ 1. How many rows does an inner join give? (17) A left join? (18) Why the difference?
print(o.shape, inner.shape, left.shape)     # (18, 8) (17, 10) (18, 10)
# ⭐ 2. Find the orphan order — which order_id and why is it orphaned? (1010, customer_id 999 doesn't exist)
print(left[left["_merge"] == "left_only"])
# ⭐ 3. Revenue per city (Birmingham 3562.50, Solihull 471.00, Coventry 220.00)
print(merged.groupby("city")["revenue"].sum().round(2).sort_values(ascending=False))
# ⭐ 4. Which customer never placed an order? (Nina Kaur)
print(cust_orders[cust_orders["order_id"].isna()]["customer_name"])   # Nina Kaur
# 5. Top 3 customers by revenue, with their names not IDs (customer_id 1, 8, 2)
print(merged.groupby("customer_name")["revenue"].sum().round(2).sort_values(ascending=False).head(3))   
# 6. Which category sells best in each city? (hint: groupby(["city","category"])["revenue"].sum())
print(merged.groupby(["city", "category"])["revenue"].sum().round(2).sort_values(ascending=False))
# 7. Do the same as Q3 using how="left" — does the total revenue change? Why?
print(left.groupby("city")["revenue"].sum().round(2).sort_values(ascending=False))   # same answer, because the orphan order has no city
# 8. Add a customer_type column: "Unknown" where the name is missing after the left join; otherwise "Known"
left["customer_type"] = left["customer_name"].apply(lambda x: "Unknown" if pd.isna(x) else "Known")
print(left["customer_type"].value_counts())