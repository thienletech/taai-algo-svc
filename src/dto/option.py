import logging
import util.time_util as time_util
from config import CFG


class Option:
    def __init__(self, ticker, train_date=None, predict_date=None):
        from_date, to_date = time_util.get_date_range(CFG.num_data_points, 1)
        self.from_date = from_date
        self.to_date = to_date
        self.ticker = ticker
        self.train_date = train_date
        self.predict_date = predict_date
        pass

    def set_date_range(self, from_date, to_date):
        self.from_date = from_date
        self.to_date = to_date

    def __str__(self) -> str:
        return "{0} {1} {2} {3} {4}".format(
            self.ticker,
            self.from_date,
            self.to_date,
            self.train_date,
            self.predict_date,
        )
