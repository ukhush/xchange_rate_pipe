import datetime as dt
import requests


class ReadDataApi:

    def __init__(self, from_cur, to_cur, out_size, api_key, time_series_key_name):
        """this class reads the exchange rate api"""

        self.from_cur = from_cur
        self.to_cur = to_cur
        self.url = f"""https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={from_cur}&to_symbol={to_cur}&apikey={api_key}&outputsize={out_size}"""
        print(self.url)
        self.time_series_key_name = time_series_key_name

        self.price_keys = ['open', 'high', 'low', 'close']

    def get_data(self):
        """this function gets json data and drops meta data sent by the api"""

        data = requests.get(self.url)
        data = data.json()

        if 'Error Message' in data.keys():
            return data['Error Message']

        return data[self.time_series_key_name], len(data[self.time_series_key_name])

    def create_row_data(self, date, prices):
        """this function takes in data and creates a row that matches the table schema"""

        row = dict()
        row['date'] = date
        row['upload_date'] = dt.datetime.today().isoformat()
        row['prices'] = [{k: v for k, v in zip(self.price_keys, prices.values())}]

        return row

    def create_row_generator(self):
        """this function creates a row generator and also returns row_count"""

        raw_data, row_count = self.get_data()
        transformed_data = (self.create_row_data(date, prices) for date, prices in raw_data.items())
        return transformed_data, row_count







