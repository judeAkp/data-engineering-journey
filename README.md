# Data Engineering Journey

Python practice projects covering fundamentals, file handling, CSV data, and
Pandas.

## Week 1

- `python.py`, `day2.py`, and `day3.py` practice Python basics, loops, lists,
  dictionaries, and functions.
- `day4.py` reads and writes text files and processes `sales.csv`.
- `day5.py` explores the sales data with Pandas.
- `csv_summary.py` reports sales totals and counts by category using Python's
  built-in `csv` module.

## Week 2

The weather pipeline looks up postcodes, fetches daily weather, and saves the
combined data to CSV and SQL Server:

```text
postcodes.csv -> postcodes.io (lat/lon) -> Open-Meteo (weather)
              -> pandas (clean) -> weather_birmingham.csv -> SQL Server
```

- `w2_day1.py` through `w2_day5.py` cover Pandas, data cleaning, aggregation,
  joins, and API responses.
- `w2_pipeline.py` combines postcode lookups and weather data, writes
  `weather_birmingham.csv`, and loads it into SQL Server.

## Week 3

Week 3 practices SQL against the `DE_Learning` database. `queries.sql` organizes
37 exercises across filtering, aggregation, joins, CTEs, and window functions.
`week3_star_schema.sql` builds and loads the star schema, records pipeline audit
counts and run time, and includes the reporting queries.

```text
dim_customer ----\
                  \
dim_product ------ fact_orders ------ dim_date
                         |
                         +-- monthly target report -- targets
```

`fact_orders` is at the order grain and stores quantity and sales amount.
`dim_customer`, `dim_product`, and `dim_date` provide reporting attributes.
Monthly targets are joined by month; the `All` category represents the
whole-month target.

Example monthly revenue vs target output:

```text
month_start  revenue  target_revenue  variance  variance_pct
2026-09-01   2760.00       2500.00    +260.00       +10.40
2026-10-01   1558.50       2500.00    -941.50       -37.66
```

Run `load_sql.py` first, then open `week3_star_schema.sql` in VS Code connected
to SQL Server and execute it against `DE_Learning`.

## Setup

From the project directory in PowerShell, create and activate a virtual
environment, then install the dependencies:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run a script from the project directory:

```powershell
python csv_summary.py
python day5.py
```
