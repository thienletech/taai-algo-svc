from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
import logging
import pickle
from tensorflow import keras
from config import CFG


class BasicLSTM:
    def __init__(self, ticker, scaler=None):
        self.ticker = ticker
        self.scaler = scaler
        self.lstm = keras.models.Sequential()
        self.lstm.add(
            keras.layers.LSTM(
                units=30,
                activation="relu",
                input_shape=(CFG.num_time_steps, CFG.num_features),
                return_sequences=True,
            )
        )
        self.lstm.add(keras.layers.Dropout(0.2))
        self.lstm.add(
            keras.layers.LSTM(
                units=30,
                activation="relu",
                input_shape=(CFG.num_time_steps, CFG.num_features),
                return_sequences=True,
            )
        )
        self.lstm.add(keras.layers.Dropout(0.2))
        self.lstm.add(
            keras.layers.LSTM(
                units=30,
                activation="relu",
                input_shape=(CFG.num_time_steps, CFG.num_features),
                return_sequences=True,
            )
        )
        self.lstm.add(keras.layers.Dropout(0.2))
        self.lstm.add(
            keras.layers.LSTM(
                units=30,
                activation="relu",
                input_shape=(CFG.num_time_steps, CFG.num_features),
                return_sequences=True,
            )
        )
        self.lstm.add(keras.layers.Dropout(0.2))
        self.lstm.add(
            keras.layers.LSTM(units=5, activation="relu", return_sequences=False)
        )
        self.lstm.add(keras.layers.Dense(units=CFG.num_future_time_steps))
        self.lstm.compile(loss="mean_squared_error", optimizer="adam")
        # self.summary()

    def fit(self, x_train, y_train):
        self.lstm.fit(
            x_train,
            y_train,
            epochs=CFG.num_train_epochs,
            batch_size=7,
            verbose=0,
            shuffle=False,
        )

    def load(self):
        self.lstm = keras.models.load_model(self._get_path_model())
        self.scaler = pickle.load(open(self._get_path_scaler(), "rb"))

    def save(self):
        self.lstm.save(self._get_path_model())
        pickle.dump(self.scaler, open(self._get_path_scaler(), "wb"))

    def _get_path_model(self):
        return "{}/basic_lstm_{}.h5".format(CFG.model_dir, self.ticker)

    def _get_path_scaler(self):
        return "{}/basic_lstm_{}.pkl".format(CFG.model_dir, self.ticker)

    def summary(self):
        self.lstm.summary()

    def predict(self, x_test):
        return self.lstm.predict(x_test)

    def evaluate(self, y_real, y_pred):
        rmse = mean_squared_error(y_real, y_pred, squared=False)
        mape = mean_absolute_percentage_error(y_real, y_pred)
        logging.info("RMSE: " + str(rmse))
        logging.info("MAPE: " + str(mape))
        logging.info(
            "Accuracy: {0}".format(
                str(100 - (100 * (abs(y_real - y_pred) / y_real)).mean())
            )
        )
