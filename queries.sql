/* =========================================================
   WEEK 3 — SQL PRACTICE
   Write your answer under each question, then run it (F5).
   Commit this file: it is portfolio evidence of SQL skill.
   Database: DE_Learning   Tables: dbo.orders, dbo.customers
   ========================================================= */

/* ---------- DAY 1: SELECT, WHERE, ORDER BY ---------- */

-- Q1. Show every column for the first 5 orders.
-- Q2. Show order_id, product and revenue (quantity * unit_price) with the
--     column named revenue. Expected total across all 18 = 4318.50.
-- Q3. List each distinct category once. (3 rows)
-- Q4. All orders in the Electronics category. (8 rows)
-- Q5. Orders where revenue is over 300. (3 rows)
-- Q6. Orders where the product starts with 'Lap'. (3 rows)
-- Q7. Orders where the product is Pen or Notebook. (4 rows)
-- Q8. Orders placed in October 2026. (6 rows)
-- Q9. All orders sorted by revenue, biggest first.
-- Q10. All orders sorted by category A-Z, then revenue biggest first.


/* ---------- DAY 2: AGGREGATES, GROUP BY, HAVING ---------- */

-- Q11. How many orders in total? How many distinct customers ordered?
-- Q12. Total revenue, average revenue, smallest and largest order.
--      Expected: 4318.50 / 239.92 / 13.50 / 820.00
-- Q13. Order count, total revenue and average order value per category. (3 rows)
-- Q14. Only categories whose total revenue is over 1000. (2 rows) - use HAVING
-- Q15. Orders and revenue per city per category. (6 rows)
-- Q16. Revenue per month. (2026-09 = 2760.00, 2026-10 = 1558.50)
-- Q17. Using a LEFT JOIN, show total orders and the count of
--      customers that matched. Why do the two numbers differ?


/* ---------- DAY 3: JOINS ---------- */

-- Q18. Join orders to customers. How many rows, and what is total revenue?
--      Expected: 17 rows / 4253.50. Where did the missing money go?
-- Q19. Same join but keep all 18 orders. What is the revenue now?
-- Q20. Revenue per city (Birmingham 3562.50, Solihull 471.00, Coventry 220.00).
-- Q21. Which customer has never placed an order? (anti-join)
-- Q22. Which order has no matching customer? (order_id and product)
-- Q23. Show Birmingham revenue using INNER JOIN, then again using
--      LEFT JOIN with WHERE c.city = 'Birmingham'. Explain the result.
-- Q24. Top 3 customers by revenue, showing names not IDs.


/* ---------- DAY 4: CTEs, SUBQUERIES, CASE, UNION ---------- */

-- Q25. Each category's revenue as a percentage of total revenue.
--      Expected: 73.46 / 24.31 / 2.22
-- Q26. Bucket every order as Small (< 100), Medium (100-499) or Large (>= 500)
--      and count how many are in each bucket. (7 / 8 / 3)
-- Q27. Stack September and October orders with UNION ALL, flagging each row's
--      source month, then count rows per month.
-- Q28. Rewrite Q21 using NOT EXISTS.
-- Q29. Using a CTE, find customers whose spend is above the average
--      customer spend.


/* ---------- DAY 5: WINDOW FUNCTIONS + FUNCTIONS ---------- */

-- Q30. Number the customers 1..n by total revenue, highest first (ROW_NUMBER).
-- Q31. Rank products by revenue. Compare RANK vs DENSE_RANK.
--      Expected order: Laptop 2320, Monitor 660, Desk 570, Chair 480,
--      Mouse 127.50, Keyboard 65, Pen 60, Notebook 36.
-- Q32. Running total of revenue by order date. Final value must be 4318.50.
-- Q33. Month-over-month revenue change using LAG (Oct = -1201.50).
-- Q34. Each category's share of total revenue using SUM() OVER ().
-- Q35. Which day of the week earns the most revenue? (Monday, 1140.00)
-- Q36. Show each order with its customer name, and show 'Unknown customer'
--      when there is no match (ISNULL or COALESCE).
-- Q37. Convert the order_date of every order to 'Mon YYYY' format.


/* ---------- DAY 6: MINI PROJECT - STAR SCHEMA ---------- */
/* Build in a new file: week3_star_schema.sql
   dbo.dim_customer, dbo.dim_product, dbo.dim_date, dbo.fact_orders, dbo.targets
   Then write the 8 report queries listed in the tutorial. */
