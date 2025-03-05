import requests
import pandas as pd
import re
from datetime import datetime
from bs4 import BeautifulSoup


def get_table(url, divClass):
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'html.parser')

    #get div class= holdings-table
    div = soup.find('div', {'class':divClass})
    table = div.find('table')
    return table

def get_date(url, divClass):
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'html.parser')

    #get div class= holdings-table
    div = soup.find('div', {'class':divClass})
    
    #gets content in P Tag
    pTagString = div.find('p', {'class':'update-date'})
    
    #Extracts date from string
    dateString = pTagString.text.strip().split("As of")[1].split()

    #converts dateString into Date Object 
    date_format = '%m/%d/%Y'
    date_time_obj = datetime.strptime(dateString[0], date_format)
    date_obj = date_time_obj.date()
    return date_obj