from flask import Flask
import click
import config
from dto.option import Option
from models import db
from services.evaluation import EvaluationService
from services.prediction import PredictionService
from services.recommendation import RecommendationService
from services.training import TrainingService

server = Flask(__name__)
server.debug = config.CFG.debug
server.config["SQLALCHEMY_DATABASE_URI"] = config.CFG.db_url
db.init_app(server)


@server.cli.command("training")
@click.argument("ticker")
def train(ticker):
    # /predictors/basic/tickers/<string:ticker>/training
    TrainingService.train(Option(ticker))


@server.cli.command("prediction")
@click.argument("ticker")
def predict(ticker):
    # /predictors/basic/tickers/<string:ticker>/prediction
    PredictionService.predict(Option(ticker))


@server.cli.command("evaluation")
@click.argument("ticker")
def evaluate(ticker):
    # /predictors/basic/tickers/<string:ticker>/evaluation
    EvaluationService.evaluate(Option(ticker))


@server.cli.command("training-all")
def train_all():
    # /predictors/basic/training-all
    TrainingService.train_all()


@server.cli.command("training-auto")
def train_auto():
    # /predictors/basic/training-auto
    TrainingService.train_auto()


@server.cli.command("prediction-all")
def predict_all():
    # /predictors/basic/prediction-all
    PredictionService.predict_all()


@server.cli.command("prediction-auto")
def predict_auto():
    # /predictors/basic/prediction-auto
    PredictionService.predict_auto()


@server.cli.command("prediction-after-train-auto")
def train_and_predict_auto():
    # /predictors/basic/prediction-after-train-auto
    PredictionService.train_and_predict_auto()


@server.cli.command("recommendation")
@click.argument("ticker")
def recommend(ticker):
    # /predictors/basic/tickers/<string:ticker>/recommendation
    RecommendationService.recommend(ticker=ticker)


@server.cli.command("recommendation-auto")
def recommend_auto():
    # /predictors/basic/recommendation-auto
    RecommendationService.recommend_auto()


@server.cli.command("run-auto")
def run_auto():
    # /predictors/basic/run-auto
    PredictionService.run_auto()


@server.cli.command("health")
def health():
    # /health
    print("alive")
