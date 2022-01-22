import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense, Dropout
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
import seaborn as sns

import binanceDB

BDB = binanceDB.BinanceDB()

data = BDB.getAllStocks()

data_df = pd.DataFrame(data)

#Variables for training
cols = list(data_df)[1:7]
#Date and volume columns are not used in training. 
print(cols) #['Open', 'High', 'Low', 'Close', 'vol', 'macd', 'rsi']

#New dataframe with only training data - 5 columns
df_for_training = data_df[cols].astype(float)

scaler = StandardScaler()
scaler = scaler.fit(df_for_training)
df_for_training_scaled = scaler.transform(df_for_training)

print(df_for_training.head(5))

# trainX = []
# trainY = []

# n_future = 1   # Number of days we want to look into the future based on the past days.
# n_past = 14  # Number of past days we want to use to predict the future.


# for i in range(n_past, len(df_for_training_scaled) - n_future +1):
#     trainX.append(df_for_training_scaled[i - n_past:i, 0:df_for_training.shape[1]])
#     trainY.append(df_for_training_scaled[i + n_future - 1:i + n_future, 0])


# trainX, trainY = np.array(trainX), np.array(trainY)

# print('trainX shape == {}.'.format(trainX.shape))
# print('trainY shape == {}.'.format(trainY.shape))


# model = Sequential()
# model.add(LSTM(64, activation='relu', input_shape=(trainX.shape[1], trainX.shape[2]), return_sequences=True))
# model.add(LSTM(32, activation='relu', return_sequences=False))
# model.add(Dropout(0.2))
# model.add(Dense(trainY.shape[1]))

# model.compile(optimizer='adam', loss='mse')
# model.summary()


# # fit the model
# history = model.fit(trainX, trainY, epochs=5, batch_size=16, validation_split=0.1, verbose=1)

# plt.plot(history.history['loss'], label='Training loss')
# plt.plot(history.history['val_loss'], label='Validation loss')
# plt.legend()