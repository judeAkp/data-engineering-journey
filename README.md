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
