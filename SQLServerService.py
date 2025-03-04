import pandas as pd
import pyodbc 


#create connection
cnxn = pyodbc.connect(r'Driver=SQL Server;Server=.\SQLEXPRESS;Database=ETFHoldings;Trusted_Connection=yes;')
cursor = cnxn.cursor()


def insert_into_table( pd):

    df = pd
    for index, row in df.iterrows():
        cursor.execute("INSERT INTO Holdings(security_str, market_val_int, symbol_str, sedol_str, quantity_int, weight_float, etf_str, update_dt) values(?,?,?,?,?,?,?,?)", row.Security, row.MarketValue, row.Symbol, row.SEDOL, row.Quantity, row.Weight, row.ETF, row.Date)
    cnxn.commit()

def getDate():
    cursor.execute("SELECT MAX(update_dt) FROM Holdings")
    result = cursor.fetchone()
    return result[0]

def closeConnection():
    cnxn.close()