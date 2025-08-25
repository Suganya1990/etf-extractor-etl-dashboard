import pandas as pd
import pyodbc 
from datetime import datetime

#bulk insert of 
def insert_into_table(df: pd.DataFrame):
    cnxn = pyodbc.connect(r'Driver=SQL Server;Server=.\SQLEXPRESS;Database=ETFHoldings;Trusted_Connection=yes;')
    try:
        tuples = list(df[["Security","MarketValue","Symbol","SEDOL","Quantity","Weight","ETF","Date"]]
                      .itertuples(index=False, name=None))
        with cnxn.cursor() as cur:
            cur.fast_executemany = True
            cur.executemany("""
                INSERT INTO Holdings(
                    security_str, market_val_int, symbol_str, sedol_str,
                    quantity_int, weight_float, etf_str, update_dt
                ) VALUES (?,?,?,?,?,?,?,?)
            """, tuples)
        cnxn.commit()
    except Exception as e:
        cnxn.rollback()
        print("UNABLE TO INSERT INTO DATABASE:", e)
        raise
    finally:
        cnxn.close()


def get_date(etf):
    cnxn = pyodbc.connect(r'Driver=SQL Server;Server=.\SQLEXPRESS;Database=ETFHoldings;Trusted_Connection=yes;')
    try:
        with cnxn.cursor() as cur:
            cur.execute("EXEC GetLastUpdateDate @ETF=?", etf)
            row = cur.fetchone()
        if not row or row[0] is None:
            return None   
        val = row[0]
        if isinstance(val, (datetime, )):
            return val.date()
        # else assume string
        return datetime.strptime(str(val), '%Y-%m-%d').date()
    except Exception as e:
        print("get_date failed: ", e)
        return None
    finally:
        cnxn.close()

