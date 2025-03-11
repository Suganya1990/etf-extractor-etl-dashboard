import DataScraperService as ds
import PandaService as ps
import SQLServerService as sql


def main(url, etf):
    #gets the most recent updated sql 
    lastDateUpdatedSQL =sql.get_date(etf)
    
    holdingsTable= ds.scrape_table(url, "holdings-table")
    holdingsDate  = ds.scrape_date(url, "holdings-table")
    if(holdingsDate!=lastDateUpdatedSQL):
        #convert Table into dataframe 
        tableDFrame=ps.create_pd(holdingsTable)
            
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
    else:
       print("NO NEW DATA TO INSERT")

  
   


if __name__=="__main__":
    
   for etf in ds.get_funds():
    url=etf[0]
    etf =etf[1]
    main(url, etf)