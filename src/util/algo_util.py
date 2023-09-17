from sklearn.preprocessing import MinMaxScaler
import logging
import numpy as np
import pandas as pd
from config import CFG


def create_df(stock_price_models):
    return pd.DataFrame(
        {
            "open": [spm.open for spm in stock_price_models],
            "high": [spm.high for spm in stock_price_models],
            "low": [spm.low for spm in stock_price_models],
            "close": [spm.close for spm in stock_price_models],
            "volume": [spm.volume for spm in stock_price_models],
        },
        index=[spm.date for spm in stock_price_models],
    )


def normalize(df: pd.DataFrame):
    ohlcv = df.iloc[:, 0:5].values
    scaler = MinMaxScaler().fit(ohlcv)
    scaler.transform(ohlcv)
    x = scaler.transform(ohlcv)
    return x, scaler


def prepare_train_data(x):
    x_samples, y_samples = [], []
    for i in range(CFG.num_time_steps, len(x) - CFG.num_future_time_steps):
        x_samples.append(x[i - CFG.num_time_steps : i])
        y_samples.append(x[i : i + CFG.num_future_time_steps, 3])

    # reshape data
    x_data = np.array(x_samples)
    x_data = x_data.reshape(x_data.shape[0], x_data.shape[1], x_data.shape[2])
    y_data = np.array(y_samples)

    return x_data, y_data


def prepare_eval_data(x):
    x_data, y_data = prepare_train_data(x)

    # split data
    total = x.shape[0] - CFG.num_time_steps - CFG.num_future_time_steps
    test_num = int(np.ceil(total * CFG.eval_perc_test_data))
    x_train = x_data[:-test_num]
    x_test = x_data[-test_num:]
    y_train = y_data[:-test_num]
    y_test = y_data[-test_num:]
    return x_train, x_test, y_train, y_test


def inverse_transform(scaler, y):
    y = y.reshape(-1, 1)
    y = np.concatenate(
        [
            np.zeros((y.shape[0], CFG.index_close)),
            y,
            np.zeros((y.shape[0], CFG.num_features - CFG.index_close - 1)),
        ],
        axis=1,
    )
    y = scaler.inverse_transform(y)
    y = y[:, CFG.index_close]
    return y
