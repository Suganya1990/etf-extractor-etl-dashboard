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

def change_data_type(df, column, kind):
    try:
        if kind == "currency":
            # keep decimals
            df[column] = (df[column]
                          .str.replace('[^0-9.\-]', '', regex=True)
                          .astype(float))
        elif kind == "quantity":
            df[column] = (df[column]
                          .str.replace('[^0-9.\-]', '', regex=True)
                          .astype(float))  # or int if truly integral
        elif kind == "percentage":
            df[column] = df[column].str.replace("%", "", regex=False).astype(float)
        elif kind == "Date":
            df[column] = pd.to_datetime(df[column], errors="coerce").dt.date
        return df
    except Exception as e:
        print("Error converting Data:", column, kind, e)
        return df
    

def convert_data_types(df):
    df = change_data_type(df, "MarketValue", "currency")
    df = change_data_type(df, "Quantity", "quantity")
    df = change_data_type(df, "Weight", "percentage")
    df = change_data_type(df, "Date", "Date")
    # Replace NaN with None without blowing up datetime/date objects
    return df.where(pd.notnull(df), None)