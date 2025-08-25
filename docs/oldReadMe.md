
Core modules:

- `ETLScript.py` — entry point to load **CSV → SQL Server**.
- `SQLServerService.py` — connection + insert helpers, last-update lookup.
- `PandaService.py` — HTML table → DataFrame and datatype conversions.
- `DataScraperService.py` — HTML scraping utilities (Sprott ETF pages as example).

---

## Project Structure

```
.
├─ ETLScript.py                # CLI to process a directory of CSVs → SQL Server
├─ SQLServerService.py         # DB insert + last-update helpers
├─ PandaService.py             # DataFrame helpers (headers/rows, conversions)
├─ DataScraperService.py       # Web scraping utilities
└─ README.md                   # This file
```

---

## Requirements

- **Python** 3.9+
- **SQL Server** (tested with SQL Server Express / local `SQLEXPRESS`)
- **ODBC Driver** for SQL Server (17 or 18)

Python packages:

```
pandas
pyodbc
requests
beautifulsoup4
```

Install:

```bash
pip install -r requirements.txt
# or
pip install pandas pyodbc requests beautifulsoup4
```

> **Windows note:** Install the Microsoft ODBC Driver for SQL Server (e.g., 17 or 18) if not present. Connection string can be updated accordingly.

---

## Database Setup

Create database (once):

```sql
CREATE DATABASE ETFHoldings;
GO
```

Create target table (example schema — adjust types/precision as needed):

```sql
USE ETFHoldings;
GO
CREATE TABLE dbo.Holdings (
  id              INT IDENTITY(1,1) PRIMARY KEY,
  security_str    NVARCHAR(255)   NOT NULL,
  market_val_int  DECIMAL(18,2)   NULL,     -- monetary value
  symbol_str      NVARCHAR(64)    NULL,
  sedol_str       NVARCHAR(16)    NULL,
  quantity_int    DECIMAL(18,4)   NULL,
  weight_float    FLOAT           NULL,     -- percentage (e.g., 3.45)
  etf_str         NVARCHAR(64)    NOT NULL,
  update_dt       DATE            NOT NULL
);
GO

-- Optional: prevent duplicates per ETF/Symbol/Date
CREATE UNIQUE INDEX UX_Holdings_Etf_Symbol_Date
  ON dbo.Holdings(etf_str, symbol_str, update_dt);
```

Optional stored procedure used by the code to get last update date:

```sql
CREATE OR ALTER PROCEDURE dbo.GetLastUpdateDate
  @ETF NVARCHAR(64)
AS
BEGIN
  SET NOCOUNT ON;
  SELECT CONVERT(VARCHAR(10), MAX(update_dt), 23) AS LastDate
  FROM dbo.Holdings
  WHERE etf_str = @ETF;
END
```

---

## Configuration

The default connection in `SQLServerService.py` is:

```
Driver=SQL Server;Server=.\SQLEXPRESS;Database=ETFHoldings;Trusted_Connection=yes;
```

If you have ODBC Driver 17/18 installed, you can switch to:

```
Driver={ODBC Driver 17 for SQL Server};Server=.\SQLEXPRESS;Database=ETFHoldings;Trusted_Connection=yes;
```

Consider moving the connection string to an environment variable, e.g., `ETFHOLDINGS_CONN_STR`.

---

## Running the CSV → SQL Load

1. Prepare a folder with CSV files. Each file should include columns (case-insensitive, spaces allowed before cleanup):

   - `Security`, `Market Value`, `Symbol`, `SEDOL`, `Quantity`, `Weight`, `ETF`, `Date`

2. Run the loader and pass the **directory path** containing CSVs:

```bash
python ETLScript.py "C:\\path\\to\\your\\csv-folder"
```

### What the script does

- `read_file`: reads each CSV.
- `remove_white_space`: trims spaces from column names.
- `convert_data_types`: applies rules:
  - **MarketValue** → numeric (keeps decimals)
  - **Quantity** → numeric (int or decimal)
  - **Weight** → percentage string (e.g., `3.45%`) → float `3.45`
  - **Date** → `datetime.date`
- `insert_into_sql`: bulk inserts into `dbo.Holdings` using `pyodbc`.

> Missing/NaN values are converted to `None` for database insertion.

---

## (Optional) Scraping Flow

`DataScraperService.py` includes helpers tailored to Sprott ETF pages:

- `scrape_table(url, css_selector)` → returns `<table>` element for holdings.
- `scrape_date(url, css_selector)` → extracts the “As of MM/DD/YYYY” date.
- `get_funds()` → sample function that finds ETF fund URLs from a Sprott page.

These can be combined with `PandaService.create_pd(table)` to build a DataFrame, then apply the same type conversions and insert using `SQLServerService.insert_into_table(df)`.

---

## Column Mapping

The loader maps DataFrame columns → SQL columns as follows:

| DataFrame column | SQL column       |
| ---------------- | ---------------- |
| `Security`       | `security_str`   |
| `MarketValue`    | `market_val_int` |
| `Symbol`         | `symbol_str`     |
| `SEDOL`          | `sedol_str`      |
| `Quantity`       | `quantity_int`   |
| `Weight`         | `weight_float`   |
| `ETF`            | `etf_str`        |
| `Date`           | `update_dt`      |

> Ensure your CSV headers match these names **after** whitespace is removed (e.g., `Market Value` → `MarketValue`).

---

## Performance Notes

- Prefer **bulk insert** with `cursor.fast_executemany = True` and `executemany(...)`.
- Use proper numeric types (`DECIMAL` for money/quantity when appropriate).
- Consider loading to a staging table and `MERGE` into `dbo.Holdings` to update existing rows and avoid duplicates.

MERGE pattern (example):

```sql
MERGE dbo.Holdings AS T
USING dbo.Holdings_Staging AS S
  ON (T.etf_str = S.etf_str AND T.symbol_str = S.symbol_str AND T.update_dt = S.update_dt)
WHEN MATCHED THEN
  UPDATE SET
    market_val_int = S.market_val_int,
    quantity_int   = S.quantity_int,
    weight_float   = S.weight_float
WHEN NOT MATCHED THEN
  INSERT (security_str, market_val_int, symbol_str, sedol_str, quantity_int, weight_float, etf_str, update_dt)
  VALUES (S.security_str, S.market_val_int, S.symbol_str, S.sedol_str, S.quantity_int, S.weight_float, S.etf_str, S.update_dt);
```

---

## Troubleshooting

- ``\*\* / driver not found\*\*: Install Microsoft ODBC Driver for SQL Server 17/18 and update the connection string.
- ``\*\* / auth issues\*\*: Verify `Trusted_Connection=yes` (Windows auth) or supply `UID`/`PWD` for SQL auth.
- **Datatype conversion errors**: Confirm CSV columns align with the expected names and formats; review the regex cleaning in `PandaService.change_data_type`.
- **Duplicate key errors**: Check the unique index; either remove duplicates from source, or implement staging + MERGE.
- **Timeouts / scraping failures**: Site structure may have changed; update selectors and add `requests` timeouts.

---

## Development Tips

- Add logging (e.g., `logging` module) instead of `print` for better observability.
- Externalize config (connection strings, selectors) via environment variables or a `config.toml`/`.env` file.
- Write unit tests for type conversion helpers.
- Consider adding a simple CLI with `argparse` (e.g., `--dir`, `--dsn`, `--dry-run`).

---

##
