import pandas as pd

def get_table_headers(table):

    """Given a tabe soup, returns all the headers"""
    headers = []
    for th in table.find("tr").find_all("th"):
        headers.append(th.text.replace(" ", ""))

    return headers    

def get_table_rows(table):
    """Given a table, returns all its rows"""
    rows=[]
    for tr in table.find_all("tr")[1:]:
        cells=[]
        #grabs all td tags in this table row
        tds = tr.find_all("td")
        if len(tds) == 0:
            #if no td tags, search for th tags
            #can be found especially in wikipedia tables below the table
            ths = tr.find_all("th")
            for th in ths:
                cells.append(th.text.strip())
        else:
             #use reuglar td tags
            for td in tds:
                cells.append(td.text.strip())
        rows.append(cells)
    return rows


def create_pd(table):
 
    headers = get_table_headers(table)
    rows = get_table_rows(table)
    dataFrame =  pd.DataFrame(rows, columns=headers)
    return dataFrame

def add_column(dataFrame, attributeName, value):
    if(attributeName == "ETF"):
        df = dataFrame.assign(ETF = value)
    if(attributeName =='Date'):
        df = dataFrame.assign(Date = value)
    return df


def change_data_type(dataFrame, column, type):
    try:
        if(type =="currency"):
            dataFrame[column] = dataFrame[column].str.replace('[^.0-9]', '', regex=True).astype('float').astype(int)
            return dataFrame
        elif(type=="quantity"):
            dataFrame[column] = dataFrame[column].str.replace('[\$\,]|\.\d*', '', regex=True).astype(int)
            return dataFrame
        elif(type=="percentage"):
            dataFrame[column] = dataFrame[column].str.replace("%", '').astype(float)
            return dataFrame
        elif(type=="Date"):
            dataFrame[column] = dataFrame[column].astype('datetime64[ns]')
            return dataFrame
    except:
        print("Error converting Data: ", column, type )
        return dataFrame