from flask import Flask
from app.config import Config
from app.extensions import db, jwt


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.cards import cards_bp
    from app.routes.recognition import recognition_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(cards_bp)
    app.register_blueprint(recognition_bp)

    return app