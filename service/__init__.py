"""Application factory for the product catalog service."""
from flask import Flask

from service.models import db


def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, static_folder="static")
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///products.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if test_config:
        app.config.update(test_config)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    from service import routes

    app.register_blueprint(routes.api)
    return app


app = create_app()
