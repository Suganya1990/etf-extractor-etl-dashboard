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
    cursor = cnxn.cursor()
    sql = """\
    EXEC GetLastUpdateDate @ETF=?
    """
    try:
        cursor.execute(sql, etf)
        result = cursor.fetchone()
        cnxn.close()
        return datetime.strptime(result[0], '%Y-%m-%d').date()
    except:
        return 

