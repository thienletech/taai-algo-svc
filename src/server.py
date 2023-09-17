import os
import sys
from flask import Flask
from flask.blueprints import Blueprint

import config
import routes
from models import db

server = Flask(__name__)
if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    server = Flask(__name__, static_folder='static')

server.debug = config.CFG.debug
server.config["SQLALCHEMY_DATABASE_URI"] = config.CFG.db_url
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.CFG.db_track_modifications
server.config['TIMEOUT'] = config.CFG.request_timeout
db.init_app(server)
db.app = server

for blueprint in vars(routes).values():
    if isinstance(blueprint, Blueprint):
        server.register_blueprint(blueprint)

if __name__ == "__main__":
    server.run(host=config.CFG.app_host, port=config.CFG.app_port, debug=False)
