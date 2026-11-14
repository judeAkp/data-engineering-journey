/*
    Week 3 - Star schema mini project
    Run against the DE_Learning SQL Server database after load_sql.py has
    created dbo.customers and dbo.orders.

    The build is additive and safe to rerun: existing rows are retained and
    only missing dimension members, orders, and targets are inserted.
    The category value 'All' in dbo.targets represents a whole-month target.
*/

USE [DE_Learning];
GO

IF OBJECT_ID(N'dbo.customers', N'U') IS NULL
    THROW 50001, 'Source table dbo.customers is missing. Run load_sql.py first.', 1;
IF OBJECT_ID(N'dbo.orders', N'U') IS NULL
    THROW 50002, 'Source table dbo.orders is missing. Run load_sql.py first.', 1;
GO

IF OBJECT_ID(N'dbo.dim_customer', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.dim_customer (
        customer_key  INT IDENTITY(1,1) NOT NULL
            CONSTRAINT PK_dim_customer PRIMARY KEY,
        customer_id   INT NOT NULL
            CONSTRAINT UQ_dim_customer_customer_id UNIQUE,
        customer_name NVARCHAR(100) NOT NULL,
        city          NVARCHAR(50) NOT NULL
    );
END;
GO

IF OBJECT_ID(N'dbo.dim_product', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.dim_product (
        product_key  INT IDENTITY(1,1) NOT NULL
            CONSTRAINT PK_dim_product PRIMARY KEY,
        product_name NVARCHAR(50) NOT NULL,
        category     NVARCHAR(50) NOT NULL,
        CONSTRAINT UQ_dim_product_name_category UNIQUE (product_name, category)
    );
END;
GO

IF OBJECT_ID(N'dbo.dim_date', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.dim_date (
        date_key    INT NOT NULL
            CONSTRAINT PK_dim_date PRIMARY KEY,
        full_date   DATE NOT NULL
            CONSTRAINT UQ_dim_date_full_date UNIQUE,
        year_number SMALLINT NOT NULL,
        quarter_number TINYINT NOT NULL,
        month_number TINYINT NOT NULL,
        month_name  NVARCHAR(20) NOT NULL,
        month_start DATE NOT NULL,
        weekday_number TINYINT NOT NULL,
        weekday_name NVARCHAR(20) NOT NULL,
        is_weekend BIT NOT NULL
    );
END;
GO

IF COL_LENGTH(N'dbo.dim_date', N'is_weekend') IS NULL
    ALTER TABLE dbo.dim_date ADD is_weekend BIT NULL;
GO

UPDATE dbo.dim_date
SET is_weekend = CASE WHEN weekday_number IN (6, 7) THEN 1 ELSE 0 END
WHERE is_weekend IS NULL;

ALTER TABLE dbo.dim_date ALTER COLUMN is_weekend BIT NOT NULL;
GO

IF OBJECT_ID(N'dbo.fact_orders', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.fact_orders (
        order_id     INT NOT NULL
            CONSTRAINT PK_fact_orders PRIMARY KEY,
        customer_key INT NOT NULL,
        product_key  INT NOT NULL,
        date_key     INT NOT NULL,
        quantity     INT NOT NULL,
        unit_price   DECIMAL(10,2) NOT NULL,
        sales_amount DECIMAL(12,2) NOT NULL,
        CONSTRAINT FK_fact_orders_dim_customer
            FOREIGN KEY (customer_key) REFERENCES dbo.dim_customer(customer_key),
        CONSTRAINT FK_fact_orders_dim_product
            FOREIGN KEY (product_key) REFERENCES dbo.dim_product(product_key),
        CONSTRAINT FK_fact_orders_dim_date
            FOREIGN KEY (date_key) REFERENCES dbo.dim_date(date_key),
        CONSTRAINT CK_fact_orders_quantity CHECK (quantity > 0),
        CONSTRAINT CK_fact_orders_unit_price CHECK (unit_price >= 0)
    );
END;
GO

IF OBJECT_ID(N'dbo.targets', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.targets (
        target_month   DATE NOT NULL,
        category       NVARCHAR(50) NOT NULL,
        target_revenue DECIMAL(12,2) NOT NULL,
        CONSTRAINT PK_targets PRIMARY KEY (target_month, category),
        CONSTRAINT CK_targets_first_of_month CHECK (DAY(target_month) = 1),
        CONSTRAINT CK_targets_nonnegative CHECK (target_revenue >= 0)
    );
END;
GO

IF OBJECT_ID(N'dbo.pipeline_audit', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.pipeline_audit (
        audit_id BIGINT IDENTITY(1,1) NOT NULL
            CONSTRAINT PK_pipeline_audit PRIMARY KEY,
        pipeline_name NVARCHAR(100) NOT NULL,
        started_at_utc DATETIME2(3) NOT NULL,
        completed_at_utc DATETIME2(3) NOT NULL,
        duration_ms BIGINT NOT NULL,
        source_customer_rows BIGINT NOT NULL,
        source_order_rows BIGINT NOT NULL,
        dim_customer_rows BIGINT NOT NULL,
        dim_product_rows BIGINT NOT NULL,
        dim_date_rows BIGINT NOT NULL,
        fact_order_rows BIGINT NOT NULL
    );
END;
GO

SET XACT_ABORT ON;
DECLARE @run_started_at DATETIME2(3) = SYSUTCDATETIME();

BEGIN TRY
    BEGIN TRANSACTION;

    -- Reserve customer_id -1 as the unknown member for unmatched source rows.
    IF NOT EXISTS (
        SELECT 1
        FROM dbo.dim_customer
        WHERE customer_id = -1
    )
    BEGIN
        INSERT INTO dbo.dim_customer (customer_id, customer_name, city)
        VALUES (-1, N'Unknown customer', N'Unknown');
    END;

    INSERT INTO dbo.dim_customer (customer_id, customer_name, city)
    SELECT c.customer_id, c.customer_name, c.city
    FROM dbo.customers AS c
    WHERE NOT EXISTS (
        SELECT 1
        FROM dbo.dim_customer AS d
        WHERE d.customer_id = c.customer_id
    );

    INSERT INTO dbo.dim_product (product_name, category)
    SELECT DISTINCT o.product, o.category
    FROM dbo.orders AS o
    WHERE NOT EXISTS (
        SELECT 1
        FROM dbo.dim_product AS p
        WHERE p.product_name = o.product
          AND p.category = o.category
    );

    ;WITH date_bounds AS (
        SELECT MIN(order_date) AS first_date, MAX(order_date) AS last_date
        FROM dbo.orders
    ),
    calendar AS (
        SELECT first_date AS full_date
        FROM date_bounds
        WHERE first_date IS NOT NULL

        UNION ALL

        SELECT DATEADD(day, 1, c.full_date)
        FROM calendar AS c
        CROSS JOIN date_bounds AS b
        WHERE c.full_date < b.last_date
    )
    INSERT INTO dbo.dim_date (
        date_key, full_date, year_number, quarter_number, month_number,
        month_name, month_start, weekday_number, weekday_name, is_weekend
    )
    SELECT
        CONVERT(INT, CONVERT(CHAR(8), c.full_date, 112)),
        c.full_date,
        YEAR(c.full_date),
        DATEPART(quarter, c.full_date),
        MONTH(c.full_date),
        DATENAME(month, c.full_date),
        DATEFROMPARTS(YEAR(c.full_date), MONTH(c.full_date), 1),
        DATEDIFF(day, CONVERT(date, '19000101', 112), c.full_date) % 7 + 1,
        DATENAME(weekday, c.full_date),
        CONVERT(BIT, CASE
            WHEN (DATEDIFF(day, CONVERT(date, '19000101', 112), c.full_date) % 7 + 1)
                IN (6, 7) THEN 1
            ELSE 0
        END)
    FROM calendar AS c
    WHERE NOT EXISTS (
        SELECT 1
        FROM dbo.dim_date AS d
        WHERE d.full_date = c.full_date
    )
    OPTION (MAXRECURSION 0);

    INSERT INTO dbo.fact_orders (
        order_id, customer_key, product_key, date_key,
        quantity, unit_price, sales_amount
    )
    SELECT
        o.order_id,
        COALESCE(c.customer_key, unknown_customer.customer_key),
        p.product_key,
        d.date_key,
        o.quantity,
        o.unit_price,
        CONVERT(DECIMAL(12,2), o.quantity * o.unit_price)
    FROM dbo.orders AS o
    LEFT JOIN dbo.dim_customer AS c
        ON c.customer_id = o.customer_id
       AND c.customer_id <> -1
    CROSS JOIN dbo.dim_customer AS unknown_customer
    JOIN dbo.dim_product AS p
        ON p.product_name = o.product
       AND p.category = o.category
    JOIN dbo.dim_date AS d
        ON d.full_date = o.order_date
    WHERE unknown_customer.customer_id = -1
      AND NOT EXISTS (
          SELECT 1
          FROM dbo.fact_orders AS f
          WHERE f.order_id = o.order_id
      );

    INSERT INTO dbo.targets (target_month, category, target_revenue)
    SELECT target.target_month, N'All', target.target_revenue
    FROM (VALUES
        (CONVERT(DATE, '20260901', 112), CONVERT(DECIMAL(12,2), 2500.00)),
        (CONVERT(DATE, '20261001', 112), CONVERT(DECIMAL(12,2), 2500.00))
    ) AS target(target_month, target_revenue)
    WHERE NOT EXISTS (
        SELECT 1
        FROM dbo.targets AS existing_target
        WHERE existing_target.target_month = target.target_month
          AND existing_target.category = N'All'
    );

    DECLARE @run_completed_at DATETIME2(3) = SYSUTCDATETIME();

    INSERT INTO dbo.pipeline_audit (
        pipeline_name, started_at_utc, completed_at_utc, duration_ms,
        source_customer_rows, source_order_rows,
        dim_customer_rows, dim_product_rows, dim_date_rows, fact_order_rows
    )
    SELECT
        N'week3_star_schema',
        @run_started_at,
        @run_completed_at,
        DATEDIFF_BIG(MILLISECOND, @run_started_at, @run_completed_at),
        (SELECT COUNT_BIG(*) FROM dbo.customers),
        (SELECT COUNT_BIG(*) FROM dbo.orders),
        (SELECT COUNT_BIG(*) FROM dbo.dim_customer),
        (SELECT COUNT_BIG(*) FROM dbo.dim_product),
        (SELECT COUNT_BIG(*) FROM dbo.dim_date),
        (SELECT COUNT_BIG(*) FROM dbo.fact_orders);

    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF XACT_STATE() <> 0
        ROLLBACK TRANSACTION;
    THROW;
END CATCH;
GO

/* ---------- REPORT 1: Monthly revenue vs target ---------- */
;WITH monthly_sales AS (
    SELECT
        date_dim.month_start,
        SUM(fact.sales_amount) AS revenue
    FROM dbo.fact_orders AS fact
    JOIN dbo.dim_date AS date_dim
        ON date_dim.date_key = fact.date_key
    GROUP BY date_dim.month_start
)
SELECT
    sales.month_start,
    sales.revenue,
    target.target_revenue,
    sales.revenue - target.target_revenue AS variance,
    CONVERT(DECIMAL(9,2),
        100.0 * (sales.revenue - target.target_revenue)
        / NULLIF(target.target_revenue, 0)
    ) AS variance_pct
FROM monthly_sales AS sales
JOIN dbo.targets AS target
    ON target.target_month = sales.month_start
   AND target.category = N'All'
ORDER BY sales.month_start;
GO

/* ---------- REPORT 1 ALTERNATIVE: Monthly revenue vs target, no CTE ---------- */
SELECT
    sales.month_start,
    sales.revenue,
    target.target_revenue,
    sales.revenue - target.target_revenue AS variance,
    CONVERT(DECIMAL(9,2),
        100.0 * (sales.revenue - target.target_revenue)
        / NULLIF(target.target_revenue, 0)
    ) AS variance_pct
FROM (
    SELECT
        date_dim.month_start,
        SUM(fact.sales_amount) AS revenue
    FROM dbo.fact_orders AS fact
    JOIN dbo.dim_date AS date_dim
        ON date_dim.date_key = fact.date_key
    GROUP BY date_dim.month_start
) AS sales
JOIN (
    SELECT target_month, target_revenue
    FROM dbo.targets
    WHERE category = N'All'
) AS target
    ON target.target_month = sales.month_start
ORDER BY sales.month_start;
GO

/*
    Prefer the CTE version above for readability: the monthly aggregation
    has a clear name and is easier to extend. The derived-table version nests
    the same steps; it is not inherently faster, since SQL Server can optimize
    both forms into the same plan.
*/

/* ---------- REPORT 2: Top five products ---------- */
SELECT TOP (5)
    product.product_name,
    product.category,
    SUM(fact.quantity) AS units_sold,
    SUM(fact.sales_amount) AS total_revenue
FROM dbo.fact_orders AS fact
JOIN dbo.dim_product AS product
    ON product.product_key = fact.product_key
GROUP BY product.product_key, product.product_name, product.category
ORDER BY total_revenue DESC, product.product_name;
GO

/* ---------- REPORT 3: Customer league table and running total ---------- */
;WITH customer_sales AS (
    SELECT
        customer.customer_key,
        customer.customer_name,
        SUM(fact.sales_amount) AS revenue
    FROM dbo.fact_orders AS fact
    JOIN dbo.dim_customer AS customer
        ON customer.customer_key = fact.customer_key
    WHERE customer.customer_id <> -1
    GROUP BY customer.customer_key, customer.customer_name
)
SELECT
    customer_name,
    revenue,
    ROW_NUMBER() OVER (ORDER BY revenue DESC, customer_name) AS customer_rank,
    SUM(revenue) OVER (
        ORDER BY revenue DESC, customer_name
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM customer_sales
ORDER BY customer_rank;
GO

/* ---------- REPORT 4: Month-over-month revenue change using LAG ---------- */
;WITH monthly_sales AS (
    SELECT
        date_dim.month_start,
        SUM(fact.sales_amount) AS revenue
    FROM dbo.fact_orders AS fact
    JOIN dbo.dim_date AS date_dim
        ON date_dim.date_key = fact.date_key
    GROUP BY date_dim.month_start
),
monthly_changes AS (
    SELECT
        month_start,
        revenue,
        LAG(revenue) OVER (ORDER BY month_start) AS previous_month_revenue
    FROM monthly_sales
)
SELECT
    month_start,
    revenue,
    previous_month_revenue,
    revenue - previous_month_revenue AS revenue_change,
    CONVERT(DECIMAL(9,2),
        100.0 * (revenue - previous_month_revenue)
        / NULLIF(previous_month_revenue, 0)
    ) AS growth_pct
FROM monthly_changes
ORDER BY month_start;
GO

/* ---------- REPORT 5: Customers with no orders (anti-join) ---------- */
SELECT
    customer.customer_id,
    customer.customer_name,
    customer.city
FROM dbo.dim_customer AS customer
WHERE customer.customer_id <> -1
  AND NOT EXISTS (
      SELECT 1
      FROM dbo.fact_orders AS fact
      WHERE fact.customer_key = customer.customer_key
  )
ORDER BY customer.customer_name;
GO

/* ---------- REPORT 6: Category share of total revenue ---------- */
;WITH category_sales AS (
    SELECT
        product.category,
        SUM(fact.sales_amount) AS revenue
    FROM dbo.fact_orders AS fact
    JOIN dbo.dim_product AS product
        ON product.product_key = fact.product_key
    GROUP BY product.category
)
SELECT
    category,
    revenue,
    CONVERT(DECIMAL(5,2),
        100.0 * revenue / NULLIF(SUM(revenue) OVER (), 0)
    ) AS revenue_share_pct
FROM category_sales
ORDER BY revenue DESC;
GO

/* ---------- REPORT 7: Revenue by weekday and weekend flag ---------- */
SELECT
    date_dim.weekday_number,
    date_dim.weekday_name,
    date_dim.is_weekend,
    SUM(fact.sales_amount) AS total_revenue
FROM dbo.fact_orders AS fact
JOIN dbo.dim_date AS date_dim
    ON date_dim.date_key = fact.date_key
GROUP BY
    date_dim.weekday_number,
    date_dim.weekday_name,
    date_dim.is_weekend
ORDER BY total_revenue DESC;
GO

/* ---------- REPORT 8: Orders assigned to the unknown customer ---------- */
SELECT
    fact.order_id,
    customer.customer_name AS customer_dimension_member
FROM dbo.fact_orders AS fact
JOIN dbo.dim_customer AS customer
    ON customer.customer_key = fact.customer_key
WHERE customer.customer_id = -1
ORDER BY fact.order_id;
GO

/* ---------- REPORT 9: Weekend vs weekday revenue per calendar day ---------- */
;WITH daily_revenue AS (
    SELECT
        date_dim.full_date,
        date_dim.is_weekend,
        COALESCE(SUM(fact.sales_amount), 0) AS revenue
    FROM dbo.dim_date AS date_dim
    LEFT JOIN dbo.fact_orders AS fact
        ON fact.date_key = date_dim.date_key
    GROUP BY date_dim.full_date, date_dim.is_weekend
)
SELECT
    CASE WHEN is_weekend = 1 THEN N'Weekend' ELSE N'Weekday' END AS day_type,
    COUNT_BIG(*) AS calendar_days,
    SUM(revenue) AS total_revenue,
    AVG(revenue) AS average_revenue_per_day
FROM daily_revenue
GROUP BY is_weekend
ORDER BY is_weekend;
GO

/* ---------- REPORT 10: First order date and days since per customer ---------- */
SELECT
    customer.customer_id,
    customer.customer_name,
    MIN(date_dim.full_date) AS first_order_date,
    DATEDIFF(
        day,
        MIN(date_dim.full_date),
        CONVERT(DATE, GETDATE())
    ) AS days_since_first_order
FROM dbo.dim_customer AS customer
LEFT JOIN dbo.fact_orders AS fact
    ON fact.customer_key = customer.customer_key
LEFT JOIN dbo.dim_date AS date_dim
    ON date_dim.date_key = fact.date_key
WHERE customer.customer_id <> -1
GROUP BY customer.customer_id, customer.customer_name
ORDER BY customer.customer_name;
GO

/* ---------- REPORT 11: Recent pipeline audit runs ---------- */
SELECT TOP (10)
    audit_id,
    pipeline_name,
    started_at_utc,
    completed_at_utc,
    duration_ms,
    source_customer_rows,
    source_order_rows,
    dim_customer_rows,
    dim_product_rows,
    dim_date_rows,
    fact_order_rows
FROM dbo.pipeline_audit
ORDER BY audit_id DESC;
GO
