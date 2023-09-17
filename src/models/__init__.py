from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .stock_price import StockPriceModel
from .stock_prediction import StockPredictionModel
from .stock_algo import StockAlgoModel
