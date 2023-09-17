import logging
from api.gpt import GptApi, GptApiParams
from config import CFG
from dto.option import Option
from repositories import StockPriceRepository, StockPredictionRepository
from repositories.stock_algo import StockAlgoRepository
from util import time_util

class RecommendationService:
    @staticmethod
    def recommend(ticker):
        logging.info("Create recommendation for ticker: {}".format(ticker))
        from_date, to_date = time_util.get_date_range(
            CFG.recomendation_history_offset, 1
        )

        # validate
        stock_algo = StockAlgoRepository.find_by_ticker(ticker)
        if (
            not stock_algo
            or stock_algo.recommend_auto != 1
            or not stock_algo.train_date
            or not stock_algo.predict_date
        ):
            logging.error("algo not ready for recommendation on {}".format(ticker))
            return
        if stock_algo.recommend_date and (
            stock_algo.recommend_date >= stock_algo.train_date
            or stock_algo.recommend_date >= stock_algo.predict_date
        ):
            logging.error(
                "already created recommendation on {} upto {} {}".format(
                    ticker, stock_algo.train_date, stock_algo.predict_date
                )
            )
            return

        # fetch data from db
        options = Option(ticker=ticker)
        options.set_date_range(from_date=from_date, to_date=to_date)
        history_prices = StockPriceRepository.find_all(option=options)
        if len(history_prices) == 0:
            return

        current_date = history_prices[-1].date

        prediction_prices = StockPredictionRepository.find_all_by_ticker_and_date_after(
            ticker=ticker, date=current_date
        )
        if len(history_prices) == 0:
            return

        # create recommendation
        try:
            recommendation = GptApi.create_recommendation(
                params=GptApiParams(
                    ticker=ticker,
                    history_prices=history_prices,
                    prediction_prices=prediction_prices,
                )
            )
        except Exception as e:
            logging.error("Fail to recommend {} {}".format(ticker, e))
            return

        # save recommendation
        return RecommendationService._save_algo_metadata(
            ticker=ticker, date=current_date, recommendation=recommendation
        )

    @staticmethod
    def _save_algo_metadata(ticker, date, recommendation):
        item = StockAlgoRepository.find_by_ticker(ticker)
        if not item:
            logging.warning("Recommend on non configured algo for {}".format(ticker))
            return
        item.recommend_date = date
        item.recommend_content = recommendation
        return StockAlgoRepository.save(item)

    @staticmethod
    def recommend_auto():
        tickers = StockAlgoRepository.find_all_recommend_auto()
        logging.info("Recommending model for {} tickers".format(len(tickers)))
        idx = 0
        for ticker in tickers:
            idx += 1
            logging.info("Recommending ticker: {} {}".format(ticker.ticker, idx))
            RecommendationService.recommend(ticker.ticker)
