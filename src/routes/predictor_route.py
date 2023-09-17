from flask import Blueprint
from flask_restful import Api
from routes.predictor_resource import PredictorResource

PREDICTOR_BLUEPRINT = Blueprint("predictor", __name__)
Api(PREDICTOR_BLUEPRINT).add_resource(
    PredictorResource.Training, "/predictors/basic/tickers/<string:ticker>/training"
)
Api(PREDICTOR_BLUEPRINT).add_resource(
    PredictorResource.Prediction, "/predictors/basic/tickers/<string:ticker>/prediction"
)
Api(PREDICTOR_BLUEPRINT).add_resource(
    PredictorResource.Evaluation, "/predictors/basic/tickers/<string:ticker>/evaluation"
)
Api(PREDICTOR_BLUEPRINT).add_resource(
    PredictorResource.TrainingAll, "/predictors/basic/training-all"
)
Api(PREDICTOR_BLUEPRINT).add_resource(
    PredictorResource.TrainingAuto, "/predictors/basic/training-auto"
)
Api(PREDICTOR_BLUEPRINT).add_resource(
    PredictorResource.PredictionAll, "/predictors/basic/prediction-all"
)
Api(PREDICTOR_BLUEPRINT).add_resource(
    PredictorResource.PredictionAuto, "/predictors/basic/prediction-auto"
)
Api(PREDICTOR_BLUEPRINT).add_resource(
    PredictorResource.PredictionAfterTrainAuto, "/predictors/basic/prediction-after-train-auto"
)
Api(PREDICTOR_BLUEPRINT).add_resource(
    PredictorResource.Recommendation, "/predictors/basic/tickers/<string:ticker>/recommendation"
)
Api(PREDICTOR_BLUEPRINT).add_resource(
    PredictorResource.RecommendationAuto, "/predictors/basic/recommendation-auto"
)
Api(PREDICTOR_BLUEPRINT).add_resource(
    PredictorResource.TrainPredictRecommendAuto, "/predictors/basic/run-auto"
)
Api(PREDICTOR_BLUEPRINT).add_resource(
    PredictorResource.HealthCheck, "/health"
)