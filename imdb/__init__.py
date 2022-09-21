__author__ = 'Apurva A Kunkulol'

import os
from flask import Flask


def create_app(test_config=None):
    #create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'imdb.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        if not os.path.exists(app.instance_path):
            os.makedirs(app.instance_path)
    except OSError as osx:
        raise osx


    @app.route("/hello")
    def hello():
        return "<p>Hello World!</p>"

    @app.route("/")
    def index():
        return "<p>This is the index page.</p>"

    from . import db
    db.init_app(app)

    from . import authentication, movie_data
    app.register_blueprint(authentication.bp)
    app.register_blueprint(movie_data.bp)


    return app


