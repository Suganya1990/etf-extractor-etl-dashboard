Python ETF Scraper V2 

Objective/Requirements:
    I wanted a solution to track the securities bought and sold.
    I would like to access the data and view the changes in quantity and market value over time. 
    I also want to get an email every Friday telling me the 
        Most bought security during the week
        Most sold security during the week 
        Cash on hand 

Solution -
    Python Script will scrape the data from the web
    Insert into SQL Server
    Power BI will pull and present the data requested
    Script to analyze weekly data and  email users about changes 


Pseudocode 
    Run ETF Scraper daily M-F at 9pm 
    Scrape data from the following websites
            https://sprottetfs.com/urnm-sprott-uranium-miners-etf, URNM
            https://sprottetfs.com/urnj-sprott-junior-uranium-miners-etf, URNJ
            https://sprottetfs.com/copp-sprott-copper-miners-etf, COPP
            https://sprottetfs.com/copj-sprott-junior-copper-miners-etf, COPJ
            https://sprottetfs.com/litp-sprott-lithium-miners-etf, LITP
            https://sprottetfs.com/nikl-sprott-nickel-miners-etf, NIKL
            https://sprottetfs.com/gbug-sprott-active-gold-silver-miners-etf, GBUG
            https://sprottetfs.com/sgdm-sprott-gold-miners-etf, SGDM 
            https://sprottetfs.com/sgdj-sprott-junior-gold-miners-etf, SGDJ
            https://sprottetfs.com/slvr-sprott-silver-miners-physical-silver-etf, SLVR
    Push on to the server 
    Grab the data from the server and load it onto Power BI 
    Schedule a daily refresh on Power BI service 
    
Other Things To Do: 
    Update documentation 
    Transfer existing data ontothe  server 

