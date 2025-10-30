from flask import Flask
from config import Config
from extensions import db, migrate, bcrypt, jwt
from flask_cors import CORS 
import cloudinary # ✅ new import
#from app import models  # import all models


def create_farm_link_app():
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)

    # ✅ Initialize extensions
    db.init_app(flask_app)
    migrate.init_app(flask_app, db)
    bcrypt.init_app(flask_app)
    jwt.init_app(flask_app)

    import app.models 
    
    cloudinary.config(
    cloud_name=flask_app.config["CLOUDINARY_CLOUD_NAME"],
    api_key=flask_app.config["CLOUDINARY_API_KEY"],
    api_secret=flask_app.config["CLOUDINARY_API_SECRET"]
) 
    
    # Ensure models are imported so that they are registered with SQLAlchemy

    # ✅ Enable CORS so frontend (React/PWA) can make requests
    
    CORS(flask_app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)
    # You can restrict later, for example:
    # CORS(app, origins=["http://localhost:3000", "https://yourfrontend.com"])

    # ✅ Register Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.crop_routes import crop_bp
    from app.routes.market_routes import market_bp
    from app.routes.livestock_routes import livestock_bp
    from app.routes.post_routes import post_bp
    from app.routes.weather_routess import weather_bp
    from app.routes.notification_routes import notification_bp
    from app.routes.gemini_routes import gemini_bp
    from app.routes.upload_routes import upload_bp

    
    flask_app.register_blueprint(auth_bp, url_prefix="/api/auth")
    flask_app.register_blueprint(crop_bp, url_prefix="/api/crop")
    flask_app.register_blueprint(market_bp, url_prefix="/api/market")
    flask_app.register_blueprint(livestock_bp, url_prefix="/api/livestock")
    flask_app.register_blueprint(post_bp, url_prefix='/api/post')
    flask_app.register_blueprint(weather_bp, url_prefix="/api/weather")
    flask_app.register_blueprint(notification_bp, url_prefix="/api/notification")
    flask_app.register_blueprint(gemini_bp, url_prefix='/api/gemini')
    flask_app.register_blueprint(upload_bp, url_prefix='/api/upload')

    return flask_app

create_app = create_farm_link_app



if __name__ == "__main__":
    app = create_farm_link_app()
    app.run(debug=True)
