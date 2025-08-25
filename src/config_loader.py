import json, os
from dotenv import load_dotenv

load_dotenv()  # loads .env at project root

def load_config(path: str = "config.json") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_conn_str(cfg: dict | None = None) -> str:
    # Prefer a full connection string in .env
    full = os.getenv("SQLSERVER_CONN_STR")
    if full:
        return full

    # Or build from parts
    driver = os.getenv("SQLSERVER_DRIVER", "{ODBC Driver 17 for SQL Server}")
    server = os.getenv("SQLSERVER_SERVER", r".\SQLEXPRESS")
    db = os.getenv("SQLSERVER_DB", "ETFHoldings")
    trusted = os.getenv("SQLSERVER_TRUSTED_CONNECTION", "yes")
    return f"Driver={driver};Server={server};Database={db};Trusted_Connection={trusted};"

def fast_executemany_enabled() -> bool:
    return os.getenv("SQL_FAST_EXECUTEMANY", "true").lower() in ("1", "true", "yes")
