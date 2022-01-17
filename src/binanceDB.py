import mysql.connector
import config

class BinanceDB():
    def __init__(self):

        self.conn = mysql.connector.connect(host=config.ENDPOINT, 
                                    user=config.USER, 
                                    passwd=config.AWS_RDS_TOKEN)
                                    # port=config.PORT, 
                                    # database=config.DBNAME)
        self.cursor = self.conn.cursor(buffered=True)
        # self.cursor.execute('''DROP DATABASE BINANCE''')
        # self.cursor.execute('''CREATE DATABASE BINANCE''')
        self.cursor.execute('''USE BINANCE''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS STOCKDATA(
                            timestamp BIGINT NOT NULL PRIMARY KEY,
                            open REAL, high REAL, low REAL, close REAL,
                            volume REAL,  macd REAL, rsi_6 REAL )''' )
                            # macdsignal REAL, macdhist REAL,  rsi_slowd REAL,
                            # n_trades INTEGER,obv REAL, atr REAL, ema200 REAL, sar REAL

        self.cursor.execute('''Select * from STOCKDATA''')
        headers = [i[0] for i in self.cursor.description]
        print(headers)

    def insert_data(self, timestamp:int, open:float, high:float, low:float, close:float, volume:float, macd:float, rsi_6:float):
        self.cursor.execute('''INSERT INTO STOCKDATA VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',(timestamp, open, high, low, close, volume, macd, rsi_6))
        return

    def getAllStocks(self):
        self.cursor.execute('''SELECT * FROM STOCKDATA''')
        result = self.cursor.fetchall()
        return result

    def deleteFirstRow(self):
        self.cursor.execute('''DELETE FROM STOCKDATA ORDER BY timestamp limit 1''')
    
    def commit(self):
        self.conn.commit()

    def __del__(self):
        self.conn.close()
        print("CONNCECTION CLOSED.")
