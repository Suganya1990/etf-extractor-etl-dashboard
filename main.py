import DataScraperService as ds
import PandaService as ps
import SQLServerService as sql
from ETFList import ETF_LIST
from datetime import datetime

def main(url, etf):
    #gets the most recent updated sql 
    lastDateUpdatedSQL =sql.get_date(etf)
    
    table= ds.get_table(url, "holdings-table")
    holdingsDate  = ds.get_date(url, "holdings-table")
    if(holdingsDate!=lastDateUpdatedSQL):
        print("inside if statement")
        #convert Table into dataframe 
        tableDFrame=ps.create_pd(table)
            
        #added date column
        tableDFrame = ps.add_column(tableDFrame, "ETF", etf)
        tableDFrame = ps.add_column(tableDFrame,  "Date", holdingsDate)

        #convert strings into numbers 
        tableDFrame = ps.change_data_type(tableDFrame, "MarketValue", "currency")
        tableDFrame = ps.change_data_type(tableDFrame, "Quantity", "quantity")
        tableDFrame = ps.change_data_type(tableDFrame, "Weight", "percentage")
        tableDFrame = ps.change_data_type(tableDFrame, "Date", "Date")

        #write to SQL 
        sql.insert_into_table(tableDFrame)

  
   


if __name__=="__main__":
    
   for etf in ETF_LIST:
    url=etf[0]
    etf =etf[1]
    main(url, etf)