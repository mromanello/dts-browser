from flask import Flask, Blueprint

from config import config

app_bp = Blueprint('app_bp', __name__, template_folder='templates', static_folder='static')


def create_app(config_name="dev"):
    """ Create the application """
    app = Flask( __name__)
    if not isinstance(config_name, str):
        app.config.from_object(config)
    else:
        app.config.from_object(config[config_name])

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    config[config_name].init_app(app)

    @app.template_filter('decode')
    def decode(s):
        return str(s)

    from app import routes

    app_bp.url_prefix = app.config["APP_URL_PREFIX"]
    app.register_blueprint(app_bp)

    return app
