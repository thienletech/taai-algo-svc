import logging
import os

from dotenv import load_dotenv

from util.path_util import mkdirs

load_dotenv()

_APP_DIR = os.getenv("APP_DIR", ".")


def _initAppDirs(rootDir):
    print("APP_DIR: " + _APP_DIR)
    mkdirs(rootDir)
    mkdirs(os.path.join(rootDir, "log"))
    mkdirs(os.path.join(rootDir, "model"))
    mkdirs(os.path.join(rootDir, "evaluation"))


_initAppDirs(_APP_DIR)

_DB_POSTGRES = {
    "user": os.getenv("DB_POSTGRES_USER"),
    "pw": os.getenv("DB_POSTGRES_PW"),
    "host": os.getenv("DB_POSTGRES_HOST"),
    "port": os.getenv("DB_POSTGRES_PORT"),
    "db": os.getenv("DB_POSTGRES_DB"),
}


class CFG:
    # general configuration
    debug = os.getenv("ENVIRONEMENT", "DEV") == "DEV"
    app_dir = _APP_DIR

    enable_chart_generation = True

    request_timeout = None

    # file storage
    model_dir = "{0}/model".format(app_dir)
    evaluation_dir = "{0}/evaluation".format(app_dir)

    # log configuration
    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_file = "{0}/log/app.log".format(app_dir)

    # app configuration
    app_host = os.getenv("APP_HOST", "0.0.0.0")
    app_port = int(os.getenv("APP_PORT", "5001"))
    app_root = os.getenv("APP_ROOT", "/")

    # db configuraion
    db_track_modifications = False
    db_url = "postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s" % _DB_POSTGRES

    # model configuration
    num_features = 5
    num_time_steps = 15
    num_future_time_steps = 10
    num_train_epochs = 100
    num_data_points = 60

    # evaluation configuration
    eval_perc_test_data = 0.25

    # data frame index
    label_close = "close"
    index_close = 3

    # api
    gpt_api_key = os.getenv("OPENAI_API_KEY", None)

    # recomendation
    recomendation_history_offset = 14


logging.basicConfig(
    level=CFG.log_level,
    format="%(levelname)s: %(asctime)s \
        pid:%(process)s module:%(module)s %(message)s",
    datefmt="%d/%m/%y %H:%M:%S",
)
