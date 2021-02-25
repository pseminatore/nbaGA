import pandas as pd
import rating_scraper
import salary_scraper
from nbapy import game
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import keys




def create():
    ratings_df = rating_scraper.scrape_into_df()
    salary_df = salary_scraper.scrape_into_df()
    df = ratings_df.merge(salary_df, how='outer', on='Name')
    #with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    df = df.dropna()
    df.reset_index(inplace=True)
    print(df) 
    df.to_csv('data.csv')
    return df


def read():
    df = pd.read_csv('data.csv', index_col=0)
    df = df.dropna()
    df['Rating'] = df['Rating'].astype(int)
    print(df)
    return df

def upload_to_cosmos(df):
    container, database = create_connection()
    for index, row in df.iterrows():
        data_to_upload = row.to_dict()
        container.upsert_item(body=data_to_upload)

    
def create_connection():
    endpoint = keys.endpoint
    key = keys.key
    client = CosmosClient(endpoint, key)
    database_name = 'Ratings'
    database = client.create_database_if_not_exists(id=database_name)
    
    container_name = 'PlayerRatings'
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/Name"),
        offer_throughput=400
    )
    return container, database

def read_from_cosmos():
    container, database = create_connection()
    items = list(container.read_all_items())[1:]
    df = pd.DataFrame()
    for item in items:
        series = pd.Series(data=item)
        df = df.append(series, ignore_index=True)
    df = df.drop(labels=["id", "_rid", "_self", "_etag", "_attachments", "_ts", "index"], axis=1)
    return df

if __name__ == "__main__":
    #df = create()
    #upload_to_cosmos(df)
    df = read_from_cosmos()
    print(df)