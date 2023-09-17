from sqlalchemy import and_
from dto.option import Option
from models import StockPriceModel


class StockPriceRepository:

    @staticmethod
    def find_all(option: Option):
        return StockPriceModel.query.filter(
            and_(
                StockPriceModel.ticker == option.ticker,
                StockPriceModel.date >= option.from_date,
                StockPriceModel.date <= option.to_date,
            )
        ).order_by(StockPriceModel.date.asc()).all()
