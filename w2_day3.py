import pandas as pd

o = pd.read_csv("orders.csv")
print(o.head(3))

o["revenue"] = o["quantity"] * o["unit_price"]     # no revenue in the source - we calculate it
o["order_date"] = pd.to_datetime(o["order_date"])
o["month"] = o["order_date"].dt.strftime("%Y-%m")  # "2026-09"

print(o.shape)               # (18, 9)
print(o["revenue"].sum())    # 4318.5


# total revenue per category, biggest first
print(o.groupby("category")["revenue"].sum().sort_values(ascending=False))

# how many orders per category
print(o["category"].value_counts())

# several stats at once, with nice column names
summary = o.groupby("category").agg(
    orders=("order_id", "count"),
    revenue=("revenue", "sum"),
    units=("quantity", "sum"),
    avg_qty=("quantity", "mean"),
)
print(summary.round(2))


print(o.groupby("product")["revenue"].sum().idxmax())        # Laptop
print(o.groupby("product")["revenue"].sum().sort_values(ascending=False).head(3))
print(o.nlargest(3, "revenue")[["order_id", "product", "revenue"]])
print(o.groupby("customer_id")["revenue"].sum().sort_values(ascending=False).head(3))


pivot = pd.pivot_table(
    o,
    values="revenue",
    index="category",
    columns="month",
    aggfunc="sum",
    fill_value=0,
)
print(pivot.round(2))
pivot.round(2).to_csv("revenue_by_category_month.csv")

print("------------ ")


#  Day 3 Practice
#  1. Total revenue across all 18 orders (£4318.50)
print(o["revenue"].sum())    # 4318.5
print("------------ ")
#  2. Revenue per category, highest first (Electronics 3172.5, Furniture 1050.0, Stationery 96.0)
print(o.groupby("category")["revenue"].sum().sort_values(ascending=False))
print("------------ ")
#  3. Number of orders per category (8, 6, 4)
print(o["category"].value_counts())
print("------------ ")
#  4. Which product earned the most? (Laptop, £2320.00)
print(o.groupby("product")["revenue"].sum().idxmax())
print("------------ ")
#  5. Which 3 customers spent the most? (1390.0, 1055.0, 921.0)
print(o.groupby("customer_id")["revenue"].sum().sort_values(ascending=False).head(3))
print("------------ ")
#  6. Average quantity per order for each category (Electronics 1.50, Furniture 1.17, Stationery 9.50)
print(o.groupby("category")["quantity"].mean().round(2))
print("------------ ")
#  7. Revenue per month (2026-09: 2760.0, 2026-10: 1558.5) — how much did it drop?
print(o.groupby("month")["revenue"].sum())
print("------------ ")
#  8. Build the pivot table of category × month and save it as a CSV
pivot = pd.pivot_table(
    o,
    values="revenue",
    index="category",
    columns="month",
    aggfunc="sum",
    fill_value=0,
)
pivot.round(2).to_csv("revenue_by_category_month.csv")
print("------------ ")
# 9. Which day of the week gets the most orders? (hint: o["order_date"].dt.day_name().value_counts())
print(o["order_date"].dt.day_name().value_counts())
print("------------ ")
# 10. Which category has the highest average revenue per order? Note how it differs from total — that distinction matters in interviews
print(o.groupby("category")["revenue"].mean().sort_values(ascending=False))