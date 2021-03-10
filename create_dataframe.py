import pandas as pd
import rating_scraper
import salary_scraper
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import keys
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
from azure.cosmosdb.table.tablebatch import TableBatch
import math



##########################  Main Functions #####################################################
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

def create_storage():
    df = read_json()
    table_client = create_storage_connection()
    upload_to_storage(df, table_client)
    print(df)
    return df

##########################  Read File Functions ##################################################
def read():
    df = pd.read_csv('data.csv', index_col=0)
    df = df.dropna()
    df['Rating'] = df['Rating'].astype(int)
    print(df)
    return df

def read_json():
    df = pd.read_json('data.json')
    return df


##########################  Upload Functions ###################################################
def upload_to_cosmos(df):
    container, database = create_connection()
    for index, row in df.iterrows():
        data_to_upload = row.to_dict()
        container.upsert_item(body=data_to_upload)
        
def upload_to_storage(df, table_client):
    batches = prepare_batches(df)
    statuses = []
    for batch in batches:
        statuses.append(table_client.commit_batch('PlayerRatings', batch))
    pass

def prepare_batches(df):
    num_batches = math.ceil(len(df.index) / 100)
    batches = []
    for i in range(num_batches):
        batch = TableBatch()
        end_index = (i + 1) * 100
        if end_index > len(df.index):
            end_index = len(df.index)
        for index, row in df[i * 100 : end_index].iterrows():
            data = row.to_dict()
            data['PartitionKey'] = 'playerRatings'
            data['RowKey'] = str(index)
            data['Index'] = index
            batch.insert_or_merge_entity(data)
        batches.append(batch)
    return batches
        


##########################  Connection Functions ###############################################
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


def create_storage_connection():
    table_service = TableService(account_name=keys.account_name, account_key=keys.storage_key)
    return table_service


##########################  Retrieval Functions ###################################################
def read_from_cosmos():
    container, database = create_connection()
    items = list(container.read_all_items())[1:]
    df = pd.DataFrame()
    for item in items:
        series = pd.Series(data=item)
        df = df.append(series, ignore_index=True)
    df = df.drop(labels=["id", "_rid", "_self", "_etag", "_attachments", "_ts", "index"], axis=1)
    return df

def read_from_storage():
    table_client = create_storage_connection()
    response = table_client.query_entities('PlayerRatings', filter="PartitionKey eq 'playerRatings'")
    pass

if __name__ == "__main__":
    read_from_storage()
    #create_storage_connection()
    #df = create()
    #upload_to_cosmos(df)
    #df = read_from_cosmos()
    #print(df)