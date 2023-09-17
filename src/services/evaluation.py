import logging
import numpy as np
from algorithm.basic_lstm import BasicLSTM
from config import CFG
from dto.option import Option
from repositories import StockPriceRepository
import util.algo_util as algo_util
import util.plot_util as plot_util


class EvaluationTask():
    def __init__(self, option: Option):
        self.option = option

    def evaluate(self):
        # fetch data from db
        prices = StockPriceRepository.find_all(self.option)
        if (len(prices) < CFG.num_time_steps):
            logging.error("Not enough data to train model on {}".format(
                self.option.ticker))
            return

        # normalize data
        prices_df = algo_util.create_df(prices)
        if CFG.enable_chart_generation:
            plot_util.plot_orig(self._get_path_figure_orig(),
                                prices_df.index,
                                prices_df[CFG.label_close],
                                'Original close price')
        x, scaler = algo_util.normalize(prices_df)

        # split data into train and test
        x_train, x_test, y_train, y_test = algo_util.prepare_eval_data(x)
        test_num = len(x_test)

        # train model
        algo = self._train_model(
            x_train=x_train, y_train=y_train, scaler=scaler)

        # evaluate
        x_test_date = prices_df.index[-test_num - CFG.num_future_time_steps:
                                      -CFG.num_future_time_steps]
        self._evaluate_model(algo, x_test_date, x_test, y_test)

        # evaluate all
        x_test_date_full = prices_df.index[CFG.num_time_steps:
                                           -CFG.num_future_time_steps]
        y_test_full = prices_df[CFG.num_time_steps:-
                                CFG.num_future_time_steps][CFG.label_close]
        self._evaluate_model_all(
            algo, x_train, x_test, x_test_date_full, y_test_full)

    def _get_path_figure_orig(self):
        return "{}/basic_lstm_{}.orig.png".format(CFG.evaluation_dir, self.option.ticker)

    def _get_path_figure_eval(self):
        return "{}/basic_lstm_{}.eval.png".format(CFG.evaluation_dir, self.option.ticker)

    def _get_path_figure_eval_all(self):
        return "{}/basic_lstm_{}.eval_full.png".format(CFG.evaluation_dir, self.option.ticker)

    def _train_model(self, x_train, y_train, scaler):
        algo = BasicLSTM(ticker=self.option.ticker, scaler=scaler)
        try:
            algo.load()
        except Exception as e:
            algo = BasicLSTM(ticker=self.option.ticker, scaler=scaler)
        algo.fit(x_train, y_train)
        return algo

    def _normalize_y(self, scaler, y):
        y = self._inverse_transform_first(scaler, y)
        if len(y.shape) > 1:
            y = y[:, 0]
        return y

    def _inverse_transform_first(self, scaler, y):
        y = y[:, 0]
        return algo_util.inverse_transform(scaler, y)

    def _evaluate_model(self, algo, x_test_date, x_test, y_test):
        y_pred = self._normalize_y(algo.scaler, algo.predict(x_test))
        y_true = self._inverse_transform_first(algo.scaler, y_test)
        algo.evaluate(y_true, y_pred)
        if CFG.enable_chart_generation:
            plot_util.plot_prediction(
                self._get_path_figure_eval(), x_test_date, y_true, y_pred)

    def _evaluate_model_all(self, algo, x_train, x_test, x_orig_full, y_orig_full):
        y_pred_train = self._normalize_y(algo.scaler, algo.predict(x_train))
        y_pred_test = self._normalize_y(algo.scaler, algo.predict(x_test))
        if CFG.enable_chart_generation:
            y_pred = np.append(y_pred_train, y_pred_test)
            plot_util.plot_prediction(
                self._get_path_figure_eval_all(), x_orig_full, y_orig_full, y_pred)


class EvaluationService():
    @staticmethod
    def evaluate(option: Option):
        logging.info("Evaluating model for ticker: {}".format(option))
        EvaluationTask(option).evaluate()
