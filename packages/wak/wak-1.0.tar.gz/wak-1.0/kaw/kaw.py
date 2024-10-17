import requests
import pandas as pd
import listed_companies_info as lt
from bs4 import BeautifulSoup


################################################################################
############################## stock price history #############################

def get_stock_history(names, START, END):
    if isinstance(names, str): 
        names = [names] 

    all_data = []  

    for name in names:
        ISIN = lt.get_isin(company_name=name)

        url = f'https://medias24.com/content/api?method=getPriceHistory&ISIN={ISIN}&format=json&from={START}&to={END}'
        payload = {
            'api_key': '19c627bec7d7a1bc2f325aa4a2bcb299',
            'url': url
        }

        r = requests.get('https://api.scraperapi.com/', params=payload)
        data = r.json()

        stock = pd.DataFrame(data)
        stock = pd.concat([stock.drop(['result', 'message'], axis=1), stock['result'].apply(pd.Series)], axis=1)
        
        if len(names) == 1: 
            return stock  
        else:
            
            stock = stock[['date', 'value']].rename(columns={'value': name})
            all_data.append(stock)

   
    final_data = all_data[0]
    for df in all_data[1:]:
        final_data = pd.merge(final_data, df, on='date', how='outer')

    return final_data

############################################################################
############################## CARNET D'ORDRES #############################

def get_carnet_ordres(name):


    ISIN = lt.get_isin(company_name=name)

    url = f"https://ebourse.cihbank.ma/trader/market/{ISIN}/XCAS/ISIN"
    response = requests.get(url)

    src = response.content
    soup = BeautifulSoup(src, "lxml")

    span = soup.find('span', {'id': "pulldatagrid_0"})

    table = span.find_next('table')

    rows = table.find_all('tr')

    table_data = []

    for row in rows:
        cells = row.find_all('td')
        data = [cell.text.strip() for cell in cells]

        if data:  
            table_data.append(data)


    df = pd.DataFrame(table_data)

    df.columns = ['Ordres', 'Titres', 'Achat', 'Vente', 'Titres', 'Ordres'] 

    df['Achat'] = df['Achat'].str.replace('-', '').str.replace(' ', '').str.replace(',', '.')
    df['Vente'] = df['Vente'].str.replace('-', '').str.replace(' ', '').str.replace(',', '.')

    
    print(df)
    


#############################################################################################
######################################les Ratios#############################################


def get_ratios(name):
    URBC = lt.get_URBC(company_name=name)

    url = f"https://www.casablanca-bourse.com/fr/live-market/emetteurs/{URBC}?scrollTo=emetteur_publications#emetteur_capital"
    
    response = requests.get(url)

    if response.status_code == 200: 
        src = response.content
        soup = BeautifulSoup(src, "lxml")

        
        div = soup.find('div', {'id': "emetteur_ratio"})  
        if div:
            table = div.find_next('table')

            if table:
                rows = table.find_all('tr')

                table_data = []
                column_names = []

                
                header = rows[0]
                header_cells = header.find_all(['th', 'td']) 
                column_names = [cell.text.strip() for cell in header_cells]

                for row in rows[1:]:
                    cells = row.find_all('td')
                    data = [cell.text.strip() for cell in cells]

                    if data:
                        table_data.append(data)

                
                df = pd.DataFrame(table_data, columns=column_names)
                print(df)
            else:
                print("Table non trouvée")
        else:
            print("Div avec id 'emetteur_ratio' non trouvé")
    else:
        print(f"Erreur lors de la requête: {response.status_code}")





##############################################################################
##################################### les dividendes #########################

def get_dividendes(name):
    URBC = lt.get_URBC(company_name=name)

    url = f"https://www.casablanca-bourse.com/fr/live-market/emetteurs/{URBC}?scrollTo=emetteur_publications#emetteur_capital"
    
    response = requests.get(url)

    if response.status_code == 200: 
        src = response.content
        soup = BeautifulSoup(src, "lxml")

        
        div = soup.find('div', {'id': "emetteur_dividendes"})  
        if div:
            table = div.find_next('table')

            if table:
                rows = table.find_all('tr')

                table_data = []
                column_names = []

                
                header = rows[0]
                header_cells = header.find_all(['th', 'td']) 
                column_names = [cell.text.strip() for cell in header_cells]

                for row in rows[1:]:
                    cells = row.find_all('td')
                    data = [cell.text.strip() for cell in cells]

                    if data:
                        table_data.append(data)

                
                df = pd.DataFrame(table_data, columns=column_names)
                print(df)
            else:
                print("Table non trouvée")
        else:
            print("Div avec id 'emetteur_ratio' non trouvé")
    else:
        print(f"Erreur lors de la requête: {response.status_code}")





