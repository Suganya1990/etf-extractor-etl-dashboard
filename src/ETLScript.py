import pandas as pd 
import PandaService as ps
import SQLServerService as sql
import sys
import os


#SCRIPT WAS CREATED TO EXTRACT DATA FROM CSV FILE AND LOAD ONTO SQL SERVER 

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

def main(fileDirectory):
    try:
        fileList = os.listdir(fileDirectory)
    except:
        return print("PLEASE SPECIFY A DIRECTORY")
    
    for file in fileList:
        try:
            df = read_file(file)
            df = remove_white_space(df)
            df = convert_data_types(df)
            insert_into_sql(df)       
        except:
            print("COULD NOT INSERT INTO SERVER: ", file)

if __name__ == "__main__":
    main(sys.argv[1])