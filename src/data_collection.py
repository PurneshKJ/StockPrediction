import config
import pandas as pd
import numpy as np
import binanceDB
# import pymysql
from binance import Client
from binance import ThreadedWebsocketManager, AsyncClient
from stockstats import StockDataFrame
# from binance import ThreadedDepthCacheManager

klines_df = None
BDB = binanceDB.BinanceDB()

def get_historical_data(binance_client):
    global klines_df

    print ("Collecting historical data")
    klines = binance_client.get_historical_klines (
                    config.SYMBOL,
                    AsyncClient.KLINE_INTERVAL_30MINUTE,
                    config.START_DATE,
                    config.END_DATE)

    klines_np = np.array(klines).astype('float64')

    klines_df = pd.DataFrame(data={ "timestamp":klines_np[:,0],
                                    "open":klines_np[:,1],
                                    "close":klines_np[:,4],
                                    "high":klines_np[:,2],
                                    "low":klines_np[:,3],
                                    "volume":klines_np[:,5]})
    stock = StockDataFrame.retype(klines_df)
    add_history_db(stock)

def handle_socket_message(msg):
    global klines_df
    global BDB
    print ("handle")
    if msg['k']['x'] == True:
        print ("Adding new data to RDS")
        cur_df = pd.DataFrame( [[ float(j) for i,j in msg['k'].items() if i in ['t', 'o','c','h','l','v'] ]],
                                columns=["timestamp", "open", "close", "high", "low", "volume"])
        klines_df = klines_df.iloc[1:, :]
        klines_df.append(cur_df, ignore_index=True)
        stock = StockDataFrame.retype(klines_df)
        stock['macd']
        stock['rsi_6']
        cur_df['macd'] = stock['macd'].iloc[-1]
        cur_df['rsi_6'] = stock['rsi_6'].iloc[-1]
        BDB.insert_data(cur_df['timestamp'].iloc[0],
                        cur_df['open'].iloc[0],
                        cur_df['high'].iloc[0],
                        cur_df['low'].iloc[0],
                        cur_df['close'].iloc[0],
                        cur_df['volume'].iloc[0],
                        cur_df['macd'].iloc[0],
                        cur_df['rsi_6'].iloc[0])
        
        print("Added New data to RDS")
        BDB.deleteFirstRow()
        BDB.commit()

def add_history_db(stock):
    print ("Started: adding historical data")
    stock['macd']
    stock['rsi_6']
    for i, row in stock.iterrows():
        if row.isnull().any():
            continue
        BDB.insert_data(stock['timestamp'].iloc[i],
                        stock['open'].iloc[i],
                        stock['high'].iloc[i],
                        stock['low'].iloc[i],
                        stock['close'].iloc[i],
                        stock['volume'].iloc[i],
                        stock['macd'].iloc[i],
                        stock['rsi_6'].iloc[i])
    BDB.commit()
    print ("complated : Adding historical data (Added %s rows)" % (stock.size))

def main():
    global klines_df
    binance_api_key = config.API_KEY
    binance_api_secret = config.API_SECRET
    binance_client = Client(binance_api_key, binance_api_secret)

    get_historical_data(binance_client)

    twm = ThreadedWebsocketManager(api_key=binance_api_key, api_secret=binance_api_secret)
    # start is required to initialise its internal loop
    twm.start()

    twm.start_kline_socket(callback=handle_socket_message, symbol=config.SYMBOL, interval='30m')
    twm.join()


if __name__ == "__main__":
   main()

