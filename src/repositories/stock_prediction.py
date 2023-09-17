from sqlalchemy import and_
from models import StockPredictionModel


class StockPredictionRepository:
    @staticmethod
    def find_all_by_ticker_and_date(ticker, date):
        return (
            StockPredictionModel.query.filter(
                and_(
                    StockPredictionModel.ticker == ticker,
                    StockPredictionModel.date == date,
                )
            )
            .order_by(StockPredictionModel.date.asc())
            .all()
        )

    @staticmethod
    def find_all_by_ticker_and_date_after(ticker, date):
        return (
            StockPredictionModel.query.filter(
                and_(
                    StockPredictionModel.ticker == ticker,
                    StockPredictionModel.date > date,
                )
            )
            .order_by(StockPredictionModel.date.asc())
            .all()
        )

    @staticmethod
    def save(item: StockPredictionModel):
        exists = StockPredictionRepository.find_all_by_ticker_and_date(
            item.ticker, item.date
        )
        if len(exists) > 0:
            for exist in exists:
                exist.close = item.close
                StockPredictionModel.save(exist)
        else:
            StockPredictionModel.save(item)
