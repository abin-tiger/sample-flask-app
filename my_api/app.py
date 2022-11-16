from flask import Flask, request
from my_api.metrics import metrics
from my_api.routes import simple_api
from my_api._version import __version__
from my_api import app_name
import my_api.logger


def create_app():
    """
    Creating the flask app object
    """

    app = Flask(__name__)
    app.register_blueprint(simple_api)
    register_metrics(app)

    return app


def register_metrics(app):
    """
    Registers the flask prometheus exporter with the flask app.
    """

    metrics.init_app(app)
    # App information as metric
    metrics.info("flask_app_info", "Application info", version=__version__)

    # Registering a default gauge metric for all flask routes. It tracks the no. of active calls for the route.
    # Similary more default metrics can be added.
    with app.app_context():
        metrics.register_default(
            metrics.gauge(
                "flask_request_in_progress", "Request progress by request paths",
                labels={"path": lambda: request.path}
            )
        )
