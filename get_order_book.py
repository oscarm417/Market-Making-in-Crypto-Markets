import pandas as pd 
import numpy as np 
import ccxt 
import time



class Orderbook():
    def __init__(self,id,secret):
        self.phemex = ccxt.phemex({
        'enableRateLimit':True,
        'apiKey': id,
        'secret':secret})

    def get_orderbook_snapshot(self, symbol: str):
        ob = self.phemex.fetch_order_book(symbol)
        return ob 
    def get_ob_for_x_seconds(self, symbol:str, time_lapse: float):
        start = time.time()
        end =  time.time()
        order_book_requests = []
        while end - start < time_lapse:
            data = self.get_orderbook_snapshot(symbol)
            order_book_requests.append(data)
            end =  time.time()
        return order_book_requests
    def format_request_stream(self,ob_data):
        df = pd.DataFrame(ob_data)
        df[['bid','bid-size']] = df['bids'].apply(lambda x: x[0]).tolist()
        df[['ask','ask-size']] = df['asks'].apply(lambda x: x[0]).tolist()
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit = 'ms')
        df['datetime'] = pd.to_datetime(df['datetime'], infer_datetime_format= True)
        df['datetime'].dt.tz_convert("US/Eastern")
        df = df[['symbol','datetime','nonce','bid','bid-size','ask','ask-size']]
        df = df.drop_duplicates(subset=["nonce"],keep= "first")
        return df
    
    def get_level_two_ob(self,symbol:str,time_lapse: float )->pd.DataFrame:
        data = self.get_ob_for_x_seconds(symbol,time_lapse)
        data = self.format_request_stream(data)
        return data 
    
# config = open("config.txt","r")
# id, secret = open("config.txt","r").readlines()[0].replace("'","").split(",")
# config.close()