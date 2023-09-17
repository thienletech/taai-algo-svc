from sqlalchemy import and_
from models import StockAlgoModel


class StockAlgoRepository:
    @staticmethod
    def find_all():
        return StockAlgoModel.query \
            .order_by(StockAlgoModel.priority.asc(), StockAlgoModel.train_date.asc()) \
            .all()

    @staticmethod
    def find_all_train_auto():
        return StockAlgoModel.query \
            .filter_by(train_auto=1) \
            .order_by(StockAlgoModel.priority.asc(), StockAlgoModel.train_date.asc()) \
            .all()

    @staticmethod
    def find_all_predict_auto():
        return StockAlgoModel.query \
            .filter_by(predict_auto=1) \
            .order_by(StockAlgoModel.priority.asc(), StockAlgoModel.predict_date.asc()) \
            .all()

    @staticmethod
    def find_all_recommend_auto():
        return StockAlgoModel.query \
            .filter_by(recommend_auto=1) \
            .order_by(StockAlgoModel.priority.asc(), StockAlgoModel.recommend_date.asc()) \
            .all()

    @staticmethod
    def find_by_ticker(ticker):
        return StockAlgoModel.query \
            .filter_by(ticker=ticker) \
            .first()

    @staticmethod
    def save(item):
        return StockAlgoModel.save(item)
