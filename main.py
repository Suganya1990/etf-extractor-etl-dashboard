import DataScraper as ds
import PandaService as ps
import SQLServerService as sql
from etfList import ETF_LIST 

def main(url, etf):
    table= ds.get_table(url, "holdings-table")
    lastUpdateDT = ds.get_date(url, "holdings-table")
    
    #convert Table into dataframe 
    tableDFrame=ps.create_pd(table)
    
    #added date column
    tableDFrame = ps.add_column(tableDFrame, "ETF", etf)
    tableDFrame = ps.add_column(tableDFrame,  "Date", lastUpdateDT)

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