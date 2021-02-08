import pandas as pd
import rating_scraper
import salary_scraper
from nbapy import game



def create():
    ratings_df = rating_scraper.scrape_into_df()
    salary_df = salary_scraper.scrape_into_df()
    df = ratings_df.merge(salary_df, how='outer', on='Name')
    #with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    df = df.dropna()
    df.reset_index(inplace=True)
    print(df) 
    return df
    
if __name__ == "__main__":
    create()