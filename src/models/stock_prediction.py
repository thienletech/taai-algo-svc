from . import db
from .base import BaseModel, MetaBaseModel


class StockPredictionModel(db.Model, BaseModel, metaclass=MetaBaseModel):
    __tablename__ = "stock_prediction"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticker = db.Column(db.String(255))
    date = db.Column(db.Date)
    close = db.Column(db.Float)
