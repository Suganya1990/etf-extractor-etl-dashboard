import requests
from datetime import datetime
from bs4 import BeautifulSoup

#gets table inside of specified div from website 
def scrape_table(url, divClass):
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'html.parser')

    #get div class= holdings-table
    section = soup.find('section', {'id':'secHoldings'})
    table = section.find('table')
    return table

#scrapes date inside of specified div from website 
def scrape_date(url, divClass):
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'html.parser')

    #get div class= holdings-table
    section = soup.find('section', {'id':'secHoldings'})
    
    #gets content in P Tag
    pTagString = section.find('p')
    
    #Extracts date from string
    dateString = pTagString.text.strip().split("As of")[1].split()

    #converts dateString into Date Object 
    date_format = '%m/%d/%Y'
    date_time_obj = datetime.strptime(dateString[0], date_format)
    date_obj = date_time_obj.date()
    return date_obj

def get_funds():
    data = requests.get("https://sprottetfs.com/urnm-sprott-uranium-miners-etf").text
    soup = BeautifulSoup(data, 'html.parser')
    div = soup.find('div', {'class':'fund-list-nav'})
    fund_list= [["https://sprottetfs.com"+i['href'], i.text] for i in div.find_all('a', href=True)]
    return fund_list
 
