from google.cloud import bigquery
from src.bigquery_crud_ops import BQdataset
import os
import argparse
from google.oauth2 import service_account

parser = argparse.ArgumentParser()
parser.add_argument("--google_key", required=True)
args = parser.parse_args()

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = args.google_key

# Downloaded credentials in JSON format

gcp_sa_credentials = {
    "type": "service_account",
    "project_id": "ukhushn-proj2",
    "private_key_id": "6e68152d46b68cf112d4eaef094a322da32443fe",
    "private_key": "",
    "client_email": "ukhushn-try@ukhushn-proj2.iam.gserviceaccount.com",
    "client_id": "106069951904078738006",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/ukhushn-try%40ukhushn-proj2.iam.gserviceaccount.com"
}

gcp_sa_credentials["private_key"] = args.google_key

project_id = gcp_sa_credentials["project_id"]

credentials = service_account.Credentials.from_service_account_info(gcp_sa_credentials)
client = bigquery.Client(project=project_id, credentials=credentials)


def unit_test_class_dataset(dataset_name):

    bqdataset = BQdataset(client)
    bqdataset.create_dataset(dataset_name, 'US')
    bqdataset.get_dataset(dataset_name)

    bqdataset.delete_dataset(dataset_name)

    return print('PASSED')


# FIRE UP THE CLIENT
# client = bigquery.Client()
# Test the func
unit_test_class_dataset('test1')
