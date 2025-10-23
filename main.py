from flask import Flask
from config import Config
from extensions import db, migrate, bcrypt, jwt
from flask_cors import CORS  # ✅ new import
#from app import models  # import all models


def create_farm_link_app():
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)

    # ✅ Initialize extensions
    db.init_app(flask_app)
    migrate.init_app(flask_app, db)
    bcrypt.init_app(flask_app)
    jwt.init_app(flask_app)

    import app.models  # Ensure models are imported so that they are registered with SQLAlchemy

    # ✅ Enable CORS so frontend (React/PWA) can make requests
    CORS(flask_app, origins="*")  
    # You can restrict later, for example:
    # CORS(app, origins=["http://localhost:3000", "https://yourfrontend.com"])

    # ✅ Register Blueprints
    from app.routes.auth_routes import auth_bp
    flask_app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return flask_app


if __name__ == "__main__":
    app = create_farm_link_app()
    app.run(debug=True)
