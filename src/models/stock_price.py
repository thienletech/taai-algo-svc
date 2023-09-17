
from . import db
from .base import BaseModel, MetaBaseModel


class StockPriceModel(db.Model, BaseModel, metaclass=MetaBaseModel):
    __tablename__ = "stock_price"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticker = db.Column(db.String(255))
    date = db.Column(db.Date)
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float)
    volume = db.Column(db.Float)
