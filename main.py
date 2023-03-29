from src.bigquery_crud_ops import BQtable, BQdataset
from src.xchange_rate_pull import ReadDataApi
from google.cloud import bigquery
import os
import time
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--google_cred_path", type=str, required=True)
parser.add_argument("--from_cur", type=str, required=True)
parser.add_argument("--to_cur", type=str, required=True)
parser.add_argument("--output_size", type=str, required=True)
parser.add_argument("--api_key", type=str, required=True)
args = parser.parse_args()


# using key to get into bigquery project
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = args.google_cred_path

# defining constants
# FINANCIAL DATA API CONSTANTS
FROM_CUR = args.from_cur
TO_CUR = args.to_cur
OUT_SIZE = args.output_size
API_KEY = args.api_key
TIME_SERIES_DATA_KEY_NAME = 'Time Series FX (Daily)'

# TABLE CONSTANTS
dataset = 'forex'
location = 'US'
table_name = f'table_{TO_CUR}_{FROM_CUR}'
schema = [
    bigquery.SchemaField("date", "DATE", mode="REQUIRED"),
    bigquery.SchemaField("upload_date", 'TIMESTAMP', mode="REQUIRED"),
    bigquery.SchemaField(
        "prices",
        "RECORD",
        mode="REPEATED",
        fields=[
            bigquery.SchemaField("open", "NUMERIC", mode="NULLABLE"),
            bigquery.SchemaField("high", "NUMERIC", mode="NULLABLE"),
            bigquery.SchemaField("low", "NUMERIC", mode="NULLABLE"),
            bigquery.SchemaField("close", "NUMERIC", mode="NULLABLE"),
        ],
    ),
]

# FIRE UP THE CLIENT
client = bigquery.Client()
# GET THE PROJECT NAME
project = client.project

# SET UP THE DATASET IN CASE IT IS MISSING
BQD = BQdataset(client)
if dataset in BQD.list_datasets():
    BQD.delete_dataset(dataset)
BQD.create_dataset(dataset, location)

# SET UP THE TABLE
BQT = BQtable(client, project, dataset)

table_id = BQT.create_table(table_name, schema)


# ADDING TIME FOR SERVER TO REGISTER NEW TABLES
# time.sleep(15)

# READ THE DATA API
RDA = ReadDataApi(FROM_CUR, TO_CUR, OUT_SIZE, API_KEY, TIME_SERIES_DATA_KEY_NAME)
row_generator, row_count = RDA.create_row_generator()

# INSERT DATA
# Need to add time for google cache to refresh
time.sleep(300)

BQT.insert_rows(table_id, row_generator)

