from . import db
from .base import BaseModel, MetaBaseModel


class StockAlgoModel(db.Model, BaseModel, metaclass=MetaBaseModel):
    __tablename__ = "stock_algo"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticker = db.Column(db.String(255))
    train_auto = db.Column(db.Integer)
    train_date = db.Column(db.Date)
    predict_auto = db.Column(db.Integer)
    predict_date = db.Column(db.Date)
    recommend_date = db.Column(db.Date)
    recommend_content = db.Column(db.String(8000))
    recommend_auto = db.Column(db.Integer)
    priority = db.Column(db.Integer)

