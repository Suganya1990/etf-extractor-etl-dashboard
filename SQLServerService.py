import pandas as pd
import pyodbc 
from datetime import datetime

#create connection


def insert_into_table( pd):
    cnxn = pyodbc.connect(r'Driver=SQL Server;Server=.\SQLEXPRESS;Database=ETFHoldings;Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    
    df = pd
    try:
        for index, row in df.iterrows():
            cursor.execute("INSERT INTO Holdings(security_str, market_val_int, symbol_str, sedol_str, quantity_int, weight_float, etf_str , update_dt) values(?,?,?,?,?,?,?,?)", row.Security, row.MarketValue, row.Symbol, row.SEDOL, row.Quantity, row.Weight, row.ETF, row.Date)

        cnxn.commit()
        cnxn.close()
    except:
        print( "UNABLE TO INSERT INTO DATABASE")
        cnxn.commit()
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

