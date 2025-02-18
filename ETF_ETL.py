from bs4 import BeautifulSoup as bs
import requests


#SCRAPE TABLE FROM WEBSITE 
#sending an HTTP request to the website's server to tretrive the webpage's content
ETF_URL = 'https://sprottetfs.com/urnm-sprott-uranium-miners-etf'
response = requests.get(ETF_URL)


#Create a soup object
soup = bs(response.text)

#Find div named holdings-table and extract table 
holdings_data = soup.find('div', class_='holdings-table')

holdings_table = holdings_data.find('table')


#CONVERT TABLE INTO SQL FORMAT 



#connect to sql sever 

#write each row into sql sever with date and etf name  and index

#close connection 

