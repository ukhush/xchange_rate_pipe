from google.cloud import bigquery
from src.bigquery_crud_ops import BQdataset
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--google_cred_path", type=str, required=True)
args = parser.parse_args()

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = args.google_cred_path


def unit_test_class_dataset(dataset_name):

    bqdataset = BQdataset(client)
    bqdataset.create_dataset(dataset_name, 'US')
    bqdataset.get_dataset(dataset_name)

    bqdataset.delete_dataset(dataset_name)

    return print('PASSED')


# FIRE UP THE CLIENT
client = bigquery.Client()
# Test the func
unit_test_class_dataset('test1')