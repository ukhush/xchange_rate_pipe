from google.cloud import bigquery
from src.bigquery_crud_ops import BQdataset
import os
from google.oauth2 import service_account
import json
import unittest

class TESTSforDATASETclass(unittest.TestCase):


    def TEST1(self):
        bqdataset = BQdataset(client)
        project = bqdataset.project()
        outmsg = bqdataset.create_dataset('TEST_dataset', 'US')
        test_msg = f"Created dataset {project}.TEST_dataset"
        self.assertEqual(outmsg, test_msg, msg=outmsg)

    def TEST2(self):
        bqdataset = BQdataset(client)
        outmsg = bqdataset.delete_dataset('TEST_dataset')
        test_msg = "Deleted dataset TEST_dataset"
        self.assertEqual(outmsg, test_msg, msg=outmsg)

if __name__ == '__main__':

    google_key = os.environ.get('BQGkey')

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

    print(google_key)
    gcp_sa_credentials["private_key"] = json.loads(google_key)

    project_id = gcp_sa_credentials["project_id"]
    credentials = service_account.Credentials.from_service_account_info(gcp_sa_credentials)
    client = bigquery.Client(project=project_id, credentials=credentials)


    unittest.main()



