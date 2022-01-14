import config
# import pandas as pd
# import numpy as np
# from stockstats import StockDataFrame
import binanceDB
# import pymysql
from binance import Client
# from binance import ThreadedWebsocketManager
# from binance import ThreadedDepthCacheManager

binance_api_key = config.API_KEY
binance_api_secret = config.API_SECERT
binance_client = Client(binance_api_key, binance_api_secret)

BDB = binanceDB.BinanceDB()

BDB.insert_data(1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

results = BDB.getAllStocks()

print(results)

# klines = binance_client.get_historical_klines (
#                 config.SYMBOL,
#                 Client.KLINE_INTERVAL_30MINUTE,
#                 config.START_DATE,
#                 config.END_DATE)

# klines_np = np.array(klines).astype('float64')

# klines_df = pd.DataFrame(data={ "timestamp":klines_np[:,0],
#                                 "open":klines_np[:,1],
#                                 "close":klines_np[:,4],
#                                 "high":klines_np[:,2],
#                                 "low":klines_np[:,3],
#                                 "volume":klines_np[:,5],
#                                 "amount":klines_np[:,8] 
#                                })

# def main():

#     twm = ThreadedWebsocketManager(api_key=binance_api_key, api_secret=binance_api_secret)
#     # start is required to initialise its internal loop
#     twm.start()

#     def handle_socket_message(msg):
#         global klines_df
#         new_df = pd.DataFrame( [[ float(j) for i,j in msg['k'].items() if i in ['t', 'o','c','h','l','v'] ]],
#                              columns=["timestamp", "open", "close", "high", "low", "volume"])
#         klines_df = klines_df.iloc[1: , :]
#         klines_df.append(new_df, ignore_index=True)
#         stock = StockDataFrame.retype(klines_df)
#         new_df['macd'] = stock['macd'].iloc[-1]
#         new_df['rsi_6'] = stock['rsi_6'].iloc[-1]
#         print (new_df)
#         print ("-----")

#     twm.start_kline_socket(callback=handle_socket_message, symbol=config.SYMBOL)


#     twm.join()


# if __name__ == "__main__":
#    main()

