import logging
import sys
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from .database import db
from .config import Config


def create_app(config: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    # Structured logging
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            '{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(module)s", "message": "%(message)s"}'
        )
    )
    app.logger.handlers = [handler]
    app.logger.setLevel(logging.INFO)

    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})
    db.init_app(app)
    Migrate(app, db)

    from .routes.tasks import tasks_bp
    from .routes.tags import tags_bp
    from .routes.health import health_bp

    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")
    app.register_blueprint(tags_bp, url_prefix="/api/tags")
    app.register_blueprint(health_bp, url_prefix="/api")

    with app.app_context():
        from . import models  # noqa: F401 — ensure models are registered before create_all
        db.create_all()

    return app
