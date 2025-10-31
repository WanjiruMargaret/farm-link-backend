from flask import Flask
from .extensions import db, bcrypt, migrate, jwt
from config import Config

# Blueprints
from .routes.auth_routes import auth_bp
from .routes.crop_routes import crop_bp
from .routes.livestock_routes import livestock_bp
from app.routes.market_routes import market_bp
from .routes.post_routes import post_bp
from .routes.notification_routes import notification_bp
from .routes.weather_routess import weather_bp
from .routes.gemini_routes import gemini_bp
from .routes.upload_routes import upload_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(crop_bp, url_prefix='/api/crops')
    app.register_blueprint(livestock_bp, url_prefix='/api/livestock')
    app.register_blueprint(market_bp, url_prefix='/api/market')
    app.register_blueprint(post_bp, url_prefix='/api/posts')
    app.register_blueprint(notification_bp, url_prefix='/api/notifications')
    app.register_blueprint(weather_bp, url_prefix='/api/weather')
    app.register_blueprint(gemini_bp, url_prefix='/api/gemini')
    app.register_blueprint(upload_bp, url_prefix='/api/upload')

    return app
