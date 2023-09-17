import logging
from algorithm.basic_lstm import BasicLSTM
from config import CFG
from dto.option import Option
from repositories import StockPriceRepository, StockAlgoRepository
import util.algo_util as algo_util

class TrainingTask():
    def __init__(self, option: Option):
        self.option = option

    def train(self):
        # fetch data from db
        prices = StockPriceRepository.find_all(self.option)
        if (len(prices) < CFG.num_time_steps):
            logging.info("Not enough data to train model for {}".format(
                self.option.ticker))
            return False
        if self.option.train_date:
            if prices[-1].date <= self.option.train_date:
                logging.info("Already trained model for {} on {}".format(
                    self.option.ticker, self.option.train_date))
                return True
        # normalize data
        prices_df = algo_util.create_df(prices)
        x, scaler = algo_util.normalize(prices_df)

        # split data into train and test
        x_train, y_train = algo_util.prepare_train_data(x)

        # train model
        algo = self._train_model(
            x_train=x_train, y_train=y_train, scaler=scaler)
        algo.save()

        # update metadata
        self._save_algo_metadata(prices[-1].date)

        return True

    def _train_model(self, x_train, y_train, scaler):
        # load model
        algo = BasicLSTM(ticker=self.option.ticker, scaler=scaler)
        try:
            algo.load()
        except Exception as e:
            algo = BasicLSTM(ticker=self.option.ticker, scaler=scaler)
        algo.fit(x_train, y_train)
        return algo

    def _save_algo_metadata(self, date):
        ticker = self.option.ticker
        item = StockAlgoRepository.find_by_ticker(ticker)
        if not item:
            logging.warning(
                "Train on non configured algo for {}".format(self.option.ticker))
            return
        item.train_date = date
        StockAlgoRepository.save(item)


class TrainingService():
    @staticmethod
    def train(option: Option):
        logging.info("Training model for ticker: {}".format(option))
        TrainingTask(option).train()

    @staticmethod
    def train_all():
        tickers = StockAlgoRepository.find_all()
        logging.info("Training model for {} tickers".format(len(tickers)))
        for idx, ticker in tickers:
            option = Option(ticker=ticker.ticker, train_date=ticker.train_date)
            logging.info("Training model for ticker: {} {}".format(option, idx))
            TrainingTask(option).train()

    @staticmethod
    def train_auto():
        tickers = StockAlgoRepository.find_all_train_auto()
        logging.info("Training model for {} tickers".format(len(tickers)))
        if len(tickers) == 0:
            return
        idx = 0
        for ticker in tickers:
            idx += 1
            option = Option(ticker=ticker.ticker, train_date=ticker.train_date)
            logging.info("Training model for ticker: {} {}".format(option, idx))
            TrainingTask(option).train()
