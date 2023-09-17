import datetime
import logging
import numpy as np
from algorithm.basic_lstm import BasicLSTM
from config import CFG
from dto.option import Option
from models.stock_prediction import StockPredictionModel
from repositories import StockPriceRepository, StockPredictionRepository
from repositories.stock_algo import StockAlgoRepository
from services.recommendation import RecommendationService
from services.training import TrainingTask
import util.algo_util as algo_util


class PredictionTask:
    def __init__(self, option: Option):
        self.option = option

    def predict(self):
        # load model
        algo = BasicLSTM(ticker=self.option.ticker)
        try:
            algo.load()
        except Exception as e:
            logging.info("No model found for {}".format(self.option.ticker))
            return False

        # fetch data from db
        prices = StockPriceRepository.find_all(self.option)

        # validate request
        now = datetime.datetime.now().date()
        stock_algo = StockAlgoRepository.find_by_ticker(self.option.ticker)
        if not stock_algo or not stock_algo.train_date:
            logging.info(
                "Require train model before predicting for {}".format(
                    self.option.ticker
                )
            )
            return False
        if (
            self.option.predict_date
            and stock_algo.train_date <= self.option.predict_date
        ):
            logging.info(
                "Already predicted model for {} on {} trained on {}".format(
                    self.option.ticker, self.option.predict_date, stock_algo.train_date
                )
            )
            return True

        # predict
        x_next = self._create_df(prices)
        y_next = self._predict_next(algo, algo.scaler, x_next)

        # save prediction
        next_dates = self._get_next_n_dates(prices[-1].date, CFG.num_future_time_steps)
        self._save_prediction(next_dates, y_next)

        # save model
        algo.save()

        # save metadata
        self._save_algo_metadata(stock_algo.train_date)

        return True

    def _save_prediction(self, dates, y_next):
        for i in range(len(dates)):
            item = StockPredictionModel()
            item.date = dates[i]
            item.ticker = self.option.ticker
            item.close = y_next[i]
            StockPredictionRepository.save(item)

    def _get_next_n_dates(self, start_date, n):
        dates = []
        days_added = 0
        while len(dates) < n:
            current_date = start_date + datetime.timedelta(days=days_added)
            if current_date.weekday() < 5:
                dates.append(current_date)
            days_added += 1
        return dates

    def _create_df(self, stock_price_models):
        spms = stock_price_models[-CFG.num_time_steps :]
        return [[spm.open, spm.high, spm.low, spm.close, spm.volume] for spm in spms]

    def _predict_next(self, lstm, scaler, x_next):
        x_next = scaler.transform(x_next)
        x_next = x_next.reshape(1, CFG.num_time_steps, CFG.num_features)
        y_next = lstm.predict(x_next)
        y_next = algo_util.inverse_transform(scaler, y_next)
        return y_next

    def _save_algo_metadata(self, date):
        item = StockAlgoRepository.find_by_ticker(self.option.ticker)
        if not item:
            return
        item.predict_date = date
        StockAlgoRepository.save(item)


class PredictionService:
    @staticmethod
    def predict(option: Option):
        logging.info("Predicting ticker: {}".format(option))
        PredictionTask(option).predict()

    @staticmethod
    def predict_all():
        tickers = StockAlgoRepository.find_all()
        logging.info("Predicting {} tickers".format(len(tickers)))
        for idx, ticker in tickers:
            option = Option(ticker=ticker.ticker, predict_date=ticker.predict_date)
            logging.info("Predicting ticker: {} {}".format(option, idx))
            PredictionTask(option).predict()

    @staticmethod
    def predict_auto():
        tickers = StockAlgoRepository.find_all_predict_auto()
        logging.info("Predicting model for {} tickers".format(len(tickers)))
        idx = 0
        for ticker in tickers:
            idx += 1
            option = Option(ticker=ticker.ticker, predict_date=ticker.predict_date)
            logging.info("Predicting ticker: {} {}".format(option, idx))
            PredictionTask(option).predict()

    @staticmethod
    def train_and_predict_auto():
        tickers = StockAlgoRepository.find_all_predict_auto()
        logging.info("Train model an predict for {} tickers".format(len(tickers)))
        idx = 0
        for ticker in tickers:
            idx = idx + 1
            option = Option(ticker=ticker.ticker, predict_date=ticker.predict_date)
            logging.info("Train model ticker: {} {}".format(option, idx))
            try:
                trained = TrainingTask(option).train()
                if trained:
                    logging.info("Predict ticker: {}".format(option))
                    PredictionTask(option).predict()
            except Exception as e:
                logging.error(e)

    @staticmethod
    def run_auto():
        tickers = StockAlgoRepository.find_all_predict_auto()
        logging.info(
            "Train and predict and recommend for {} tickers".format(len(tickers))
        )
        idx = 0
        for ticker in tickers:
            idx = idx + 1
            option = Option(ticker=ticker.ticker, predict_date=ticker.predict_date)
            logging.info("Train ticker: {} {}".format(option, idx))
            try:
                trained = TrainingTask(option).train()
                if trained:
                    logging.info("Predict ticker: {}".format(option))
                    predicted = PredictionTask(option).predict()
                    if predicted:
                        RecommendationService.recommend(option.ticker)
            except Exception as e:
                logging.error(e)
