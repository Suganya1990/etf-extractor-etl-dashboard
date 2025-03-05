import pandas as pd 
from pathlib import Path
import glob
import PandaService as ps
import SQLServerService as sql
import sys
import os


#Read CSV File 
def read_file(filePath):
    filePath = "C:\\Users\\smahe\\Documents\\DataSets\\ETF_UDatasets\\" + filePath
    return  pd.read_csv(filePath)

#remove white space from df
def remove_white_space(df):
    df.columns = df.columns.str.replace(' ', '')
    return df

def convert_data_types(df):
    df = ps.change_data_type(df, "MarketValue", "currency")
    df = ps.change_data_type(df, "Quantity", "quantity")
    df = ps.change_data_type(df, "Weight", "percentage")
    df = ps.change_data_type(df, "Date", "Date")
    df = df.astype(object).where(pd.notnull(df), None)
    return df

def insert_into_sql(df):
    sql.insert_into_table(df)
    print("INSERTED INTO SERVER")

def main(fileDirectory):
    fileList = os.listdir(fileDirectory)
    for file in fileList:
        df = read_file(file)
        df = remove_white_space(df)
        df = convert_data_types(df)
        insert_into_sql(df)       

if __name__ == "__main__":
    main(sys.argv[1])