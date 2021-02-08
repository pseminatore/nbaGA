import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_into_df():
    df = pd.DataFrame(columns=['Name', 'Salary'])
    
    URL = 'https://www.basketball-reference.com/contracts/players.html'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    table = soup.find('table')
    body = table.find('tbody')
    rows = body.find_all('tr')
    
    for row in rows:
        
        if row.has_attr('class'):
            continue
        
        for data in row:
            
            if data.get('data-stat') == 'player':
                links = data.find_all('a')
                player_name = links[1].text.strip()
                
            if data.get('data-stat') == 'y1':
                player_salary = data.text.strip()[1:]
                
        pd_row = {'Name': player_name, 'Salary': player_salary}
        row_to_add = pd.Series(pd_row)
        df = df.append(row_to_add, ignore_index=True)
        
    return df
    
    
   
   
def not_header_row(tr):
    return tr and not tr.has_attr('class')
    
if __name__ == "__main__":
    scrape_into_df()