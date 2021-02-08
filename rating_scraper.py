import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_into_df():
    
    df = pd.DataFrame(columns=['Name', 'Position', 'Rating', 'Height', 'Archetype'])
    
    URL = 'https://www.nba2kw.com/list/nba-2k21-all-player-ratings/'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    for row in rows[1:]:
        player_name = row.find('td', class_='data-name').text.strip()
        player_position = row.find('td', class_='data-position').text.strip()
        player_ovr = row.find('td', class_='data-ovr').text.strip()
        player_height = row.find('td', class_='data-height').text.strip()
        player_type = row.find('td', class_='data-type').text.strip()
        
        pd_row = {'Name': player_name, 'Position': player_position, 'Rating': player_ovr, 'Height': player_height, 'Archetype': player_type}
        row_to_add = pd.Series(pd_row)
        df = df.append(row_to_add, ignore_index=True)
        
    return df
    
    
if __name__ == "__main__":
    scrape_into_df()