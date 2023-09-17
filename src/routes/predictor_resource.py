from flask.json import jsonify
from flask_restful import Resource
from dto.option import Option
from services import TrainingService
from services.evaluation import EvaluationService
from services.prediction import PredictionService
from services.recommendation import RecommendationService


class PredictorResource(Resource):
    class Training(Resource):
        @staticmethod
        def post(ticker):
            TrainingService.train(Option(ticker))
            return jsonify({})

    class Prediction(Resource):
        @staticmethod
        def post(ticker):
            PredictionService.predict(Option(ticker))
            return jsonify({})

    class TrainingAll(Resource):
        @staticmethod
        def post():
            TrainingService.train_all()
            return jsonify({})

    class TrainingAuto(Resource):
        @staticmethod
        def post():
            TrainingService.train_auto()
            return jsonify({})

    class PredictionAll(Resource):
        @staticmethod
        def post():
            PredictionService.predict_all()
            return jsonify({})

    class PredictionAuto(Resource):
        @staticmethod
        def post():
            PredictionService.predict_auto()
            return jsonify({})
        
    class PredictionAfterTrainAuto(Resource):
        @staticmethod
        def post():
            PredictionService.train_and_predict_auto()
            return jsonify({})

    class Evaluation(Resource):
        @staticmethod
        def post(ticker):
            EvaluationService.evaluate(Option(ticker))
            return jsonify({})

    class Recommendation(Resource):
        @staticmethod
        def post(ticker):
            RecommendationService.recommend(ticker)
            return jsonify()

    class RecommendationAuto(Resource):
        @staticmethod
        def post():
            RecommendationService.recommend_auto()
            return jsonify()
        
    class TrainPredictRecommendAuto(Resource):
        @staticmethod
        def post():
            PredictionService.run_auto()
            return jsonify()
        
    class HealthCheck(Resource):
        @staticmethod
        def get():
            return 'alive'
