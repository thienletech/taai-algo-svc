import logging
import os
import openai

from util import time_util
import config


class GptApiParams:
    def __init__(self, ticker, history_prices, prediction_prices):
        self.ticker = ticker
        self.history_prices = history_prices
        self.prediction_prices = prediction_prices
        pass

    def __str__(self) -> str:
        return "{0} {1} {2}".format(
            self.ticker, len(self.history_prices), len(self.prediction_prices)
        )


class GptApi:
    _prompt_format = """
        Forget all your previous instructions. Pretend you are an expert stock analyst. 
        I will give you a stock name, stock price data history of the past few days, 
        stock price data prediction of the next few days that are generated by my AI model. 
        You will give me an analysis report which should includes but not limited to: 
        detail insights on historical data, detail insights on prediction data, 
        what should i watch out for on the next day which is the first day of the prediction. 
        I might already has some of that stock for selling or might not have any stock yet. 
        Mention technical analysis techniques that is suitable for this particular data if possible, 
        do not mention fundamental analysis indicators. Write in professinal, appealing, fanstastic, 
        motivated style so that i can display on my website, use single word TAAI when refer to the one 
        who create the report. Write in Vietnamese. Answer length should fit in sql varchar(8000) data type. 
        Do not mention the stock price data format of this prompt.
        Stock name is: {ticker}.
        Model name is: TAAI.
        Next is stock price data in format of <YYYYmmdd>,<close price>;<YYYYmmdd>,<close price>;...;
        Stock price data history: {history_prices}.
        Stock price data prediction: {prediction_prices}.
        At the end, show one famous quote on stock invest together with author, format it as "<quote> - <author>" in separated paragraph, example: 
            "An investment in knowledge pays the best interest." - Benjamin Franklin
    """

    @staticmethod
    def create_recommendation(params: GptApiParams):
        if not config.CFG.gpt_api_key:
            raise Exception("Missing api key")

        history_prices = ""
        for d in params.history_prices:
            history_prices += "{0},{1:.2};".format(
                time_util.format_date(d.date, "%Y%m%d"), d.close
            )
        prediction_prices = ""
        for d in params.prediction_prices:
            prediction_prices += "{0},{1:.2};".format(
                time_util.format_date(d.date, "%Y%m%d"), d.close
            )
        prompt = GptApi._prompt_format.format(
            ticker=params.ticker,
            history_prices=history_prices,
            prediction_prices=prediction_prices,
        )

        openai.api_key = config.CFG.gpt_api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
        )

        logging.info("chat gpt response on {0}: {1}".format(params.ticker, response))

        if response["choices"][0]["finish_reason"] == "stop":
            return response["choices"][0]["message"]["content"]
        else:
            raise Exception("Gpt API response error")
