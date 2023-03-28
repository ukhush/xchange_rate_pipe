from google.cloud import bigquery


class BQtable:

    def __init__(self, client, project, dataset):
        self.client = client
        self.project = project
        self.dataset = dataset

    def create_table(self, table_name, tschema):

        tables = [f"{table.table_id}" for table in self.client.list_tables(self.dataset)]
        print(tables)
        table_id = bigquery.Table.from_string(f"{self.project}.{self.dataset}.{table_name}")
        if table_name not in tables:
            table = bigquery.Table(table_id, schema=tschema)
            table = self.client.create_table(table)
            print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")

        return table_id

    def insert_rows(self, table_name, data):

        errors = self.client.insert_rows_json(table_name, json_rows=data)  # Make an API request.
        if not errors:
            pass
        else:
            print(f"Encountered errors while inserting rows: {errors}")
        return None

    def delete_table(self, table_id):
        self.client.delete_table(table_id, not_found_ok=True)
        print(f"Deleted table '{table_id}'.")
        return None


class BQdataset:

    def __init__(self, client):
        self.project = client.project
        self.client = client

    def create_dataset(self, dataset_id, location):

        if dataset_id not in self.list_datasets(stroutput=False):
            dataset_ref = bigquery.DatasetReference.from_string(dataset_id, default_project=self.project)
            dataset = bigquery.Dataset(dataset_ref)
            dataset.location = location
            dataset = self.client.create_dataset(dataset)
            print(f"Created dataset {self.project}.{dataset.dataset_id}")
            datasets = list(self.client.list_datasets())
            print(f"New dataset list {[d.dataset_id for d in datasets]}")

        else:
            print("Dataset already there")
        return None

    def list_datasets(self, stroutput=True):
        datasets = list(self.client.list_datasets())  # Make an API request.
        project = self.project

        if stroutput:
            if datasets:
                print(f"Datasets in project {project}:{[d.dataset_id for d in datasets]}")
            else:
                print(f"{project} project does not contain any datasets.")

        return [d.dataset_id for d in datasets]

    def get_dataset(self, dataset_id):
        dataset = self.client.get_dataset(dataset_id)  # Make an API request.
        full_dataset_id = "{}.{}".format(dataset.project, dataset.dataset_id)
        print(f"Got dataset {full_dataset_id}.")
        return None

    def delete_dataset(self, dataset_id):
        self.client.delete_dataset(dataset_id, delete_contents=True, not_found_ok=True)
        print(f"Deleted dataset {dataset_id}")
        return None
